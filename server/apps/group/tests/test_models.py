from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TransactionTestCase

from ..models import Group

User = get_user_model()


class GroupModelTest(TransactionTestCase):
    """Test Group model."""

    def setUp(self) -> None:
        """Setup Example Data for the Test Class."""
        self.user1 = User.objects.create(
            username="testuser1",
            password="testpassword",
        )

        self.user2 = User.objects.create(
            username="testuser2",
            password="testpassword",
        )

        self.group = Group.objects.create(
            name="Test Group",
            description="Test Group Description",
            owner=self.user1,
            join_code="123456",
        )

    def test_fields(self):
        """Test Group Model fields."""
        self.assertTrue(hasattr(Group, "name"))
        self.assertTrue(hasattr(Group, "description"))
        self.assertTrue(hasattr(Group, "owner"))
        self.assertTrue(hasattr(Group, "members"))
        self.assertTrue(hasattr(Group, "join_code"))

    def test_group_str_method(self):
        """Test Group Model str method."""
        expected_str = self.group.name

        self.assertEqual(self.group.__str__(), expected_str)

    def test_group_creation(self):
        """Test Group Model instance creation."""
        self.assertTrue(isinstance(self.group, Group))
        self.assertEqual(self.group.name, "Test Group")
        self.assertEqual(self.group.description, "Test Group Description")
        self.assertEqual(self.group.owner, self.user1)
        self.assertEqual(self.group.members.count(), 1)
        self.assertEqual(self.group.join_code, "123456")

    def test_group_update(self):
        """Test Group model update."""
        self.group.name = "Test Group Updated"
        self.group.description = "Description Updated"
        self.group.owner = self.user2
        self.group.join_code = "654321"

        self.group.save()

        self.assertEqual(self.group.name, "Test Group Updated")
        self.assertEqual(self.group.description, "Description Updated")
        self.assertEqual(self.group.owner, self.user2)
        self.assertEqual(self.group.join_code, "654321")

    def test_group_delete(self):
        """Test Group model delete."""
        self.group.delete()
        self.assertEqual(Group.objects.count(), 0)

    def test_group_delete_with_members(self):
        """Test Group model delete with existing members."""
        self.group.members.add(self.user2)
        self.group.delete()

        self.assertEqual(Group.objects.count(), 0)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(self.user1.owned_groups.count(), 0)
        self.assertEqual(self.user2.belonged_groups.count(), 0)

    def test_group_owner_relationship(self):
        """Test Group and User owner relationship."""
        self.assertEqual(self.user1.owned_groups.count(), 1)
        self.assertEqual(self.user1.owned_groups.first(), self.group)

    def test_group_members_relationship(self):
        """Test Group members."""
        self.group.members.add(self.user1)
        self.group.members.add(self.user2)

        self.assertEqual(self.group.members.count(), 2)
        self.assertEqual(self.group.members.first(), self.user1)
        self.assertEqual(self.group.members.last(), self.user2)

    def test_group_join_code_unique(self):
        """Test Group join code unique."""
        with self.assertRaises(IntegrityError):
            Group.objects.create(
                name="Test Group 2",
                description="Test Group Description 2",
                owner=self.user2,
                join_code="123456",
            )
