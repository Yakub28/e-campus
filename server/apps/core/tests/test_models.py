from unittest import mock

from django.db import connection
from django.db.models.base import ModelBase
from django.test import TransactionTestCase
from django.utils import timezone

from server.apps.core.models import BaseModel


class BaseModelTest(TransactionTestCase):
    """Test BaseModel."""

    mixin = BaseModel
    model = ModelBase(
        "TestModel_" + mixin.__name__,
        (mixin,),
        {"__module__": mixin.__module__},
    )

    @classmethod
    def setUpTestData(self) -> None:
        """Set up test."""

        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(self.model)

        super().setUpClass()

    @classmethod
    def tearDownClass(self) -> None:
        super().tearDownClass()

        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(self.model)

    def test_model_name(self):
        """Test if model name is correct."""
        self.assertEqual(self.model.__name__, "TestModel_BaseModel")

    def test_model_is_subclass_of_mixin(self):
        """Test if model is subclass of mixin."""
        self.assertTrue(issubclass(self.model, self.mixin))

    def test_mixin_is_abstract(self):
        """Test if mixin model is abstract."""
        self.assertTrue(self.mixin._meta.abstract)

    def test_model_is_not_abstract(self):
        """Test if model is not abstract."""
        self.assertFalse(self.model._meta.abstract)

    def test_created_at(self):
        """Test if created_at is in model."""
        self.assertTrue(hasattr(self.model, "created_at"))

    def test_created_at_sets_on_creation(self):
        """Test if created_at sets on creation."""
        obj = self.model.objects.create()
        self.assertIsNotNone(obj.created_at)

    def test_created_at_is_not_updated_on_save(self):
        """Test if created_at is not updated on save."""
        obj = self.model.objects.create()
        created_at = obj.created_at

        obj.save()
        self.assertEqual(obj.created_at, created_at)

    def test_updated_at(self):
        """Test if updated_at is in model."""
        self.assertTrue(hasattr(self.model, "updated_at"))

    def test_updated_at_sets_on_creation(self):
        """Test if updated_at sets on creation."""
        obj = self.model.objects.create()
        self.assertIsNotNone(obj.updated_at)

    def test_updated_at_updates_on_save(self):
        """Test if updated_at updates on save."""
        instance = self.model.objects.create()
        updated_at = instance.updated_at

        with mock.patch(
            "django.utils.timezone.now",
            return_value=timezone.now() + timezone.timedelta(days=1),
        ):
            instance.save()

        self.assertGreater(instance.updated_at, updated_at)
        self.assertNotEqual(instance.updated_at, instance.created_at)

    def test_ordering(self):
        """Test if the ordering is correct."""
        self.model.objects.create()

        with mock.patch(
            "django.utils.timezone.now",
            return_value=timezone.now() + timezone.timedelta(days=1),
        ):
            self.model.objects.create()

        objects = self.model.objects.all()
        self.assertGreater(objects[0].updated_at, objects[1].updated_at)
