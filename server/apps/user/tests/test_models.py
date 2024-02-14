import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings, TransactionTestCase

from server.apps.user.models import User

TEMP_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class UserModelTestCase(TransactionTestCase):
    """Test the User model."""

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)  # delete the temp dir
        super().tearDownClass()

    def test_create_user_without_photo(self):
        """Test creating a user without a photo."""
        user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.photo, None)

    def test_create_user_with_photo(self):
        """Test creating a user with a photo."""
        user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            photo=SimpleUploadedFile("test.jpg", b"whatevercontentsyouwant"),
        )

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.photo.name, "users/test.jpg")

    def test_photo_name_unique(self):
        """Test is Photo name changes if it is the same with different users."""
        user1 = User.objects.create_user(
            username="testuser1",
            password="testpassword1",
            photo=SimpleUploadedFile("test.jpg", b"whatevercontentsyouwant"),
        )

        user2 = User.objects.create_user(
            username="testuser2",
            password="testpassword2",
            photo=SimpleUploadedFile("test.jpg", b"whatevercontentsyouwant"),
        )

        self.assertNotEqual(user1.photo.name, user2.photo.name)
