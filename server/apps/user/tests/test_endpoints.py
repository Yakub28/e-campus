import pathlib
import shutil
import tempfile

from django.test import override_settings
from PIL import Image
from rest_framework.test import APITestCase

from server.apps.user.models import User

TEMP_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestRegister(APITestCase):
    """Test the register endpoint."""

    endpoint = "/api/auth/register/"

    def setUp(self):
        self.data = {
            "first_name": "Test",
            "last_name": "Test",
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "password_confirmation": "testpassword",
        }

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)  # delete the temp dir
        super().tearDownClass()

    def test_with_no_data(self):
        """Test with no data."""
        response = self.client.post(self.endpoint, {})

        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            set(response.data.keys()),
            set(["first_name", "last_name", "username", "email", "password", "password_confirmation"]),
        )

    def test_required_fields(self):
        """Test with required fields only."""
        response = self.client.post(self.endpoint, self.data)

        self.assertEqual(response.status_code, 201)

        self.assertEqual(response.data["photo"], None)

        self.assertEqual(response.data["first_name"], self.data["first_name"])
        self.assertEqual(response.data["last_name"], self.data["last_name"])
        self.assertEqual(response.data["username"], self.data["username"])
        self.assertEqual(response.data["email"], self.data["email"])

        self.assertFalse("password" in response.data)
        self.assertFalse("password_confirmation" in response.data)

        self.assertEqual(User.objects.count(), 1)

    def test_photo_field(self):
        """Test with photo field."""
        image = Image.new("RGB", (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(tmp_file)
        tmp_file.seek(0)

        self.data["photo"] = tmp_file

        filename = pathlib.Path(tmp_file.name).name

        response = self.client.post(self.endpoint, self.data, format="multipart")

        self.assertEqual(response.status_code, 201)

        self.assertEqual(response.data["photo"], f"/media/users/{filename}")

        self.assertEqual(User.objects.count(), 1)

    def test_passwords_mismatch(self):
        """Test with passwords mismatch."""
        self.data["password_confirmation"] = "mismatch"

        response = self.client.post(self.endpoint, self.data)

        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.data.keys(), set(["password_confirmation"]))

        self.assertEqual(User.objects.count(), 0)


class TestLogin(APITestCase):
    """Test the login endpoint."""

    endpoint = "/api/auth/login/"

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )

    def test_with_no_data(self):
        """Test with no data."""
        response = self.client.post(self.endpoint, {})

        self.assertEqual(response.status_code, 400)

        self.assertEqual(set(response.data.keys()), set(["username_email", "password"]))

    def test_with_username(self):
        """Test with username."""
        data = {
            "username_email": "testuser",
            "password": "testpassword",
        }

        response = self.client.post(self.endpoint, data)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(set(response.data.keys()), set(["access", "refresh"]))

    def test_with_email(self):
        """Test with email."""
        data = {
            "username_email": "test@example.com",
            "password": "testpassword",
        }

        response = self.client.post(self.endpoint, data)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(set(response.data.keys()), set(["access", "refresh"]))

    def test_with_wrong_password(self):
        """Test with wrong password."""
        data = {
            "username_email": "testuser",
            "password": "wrongpassword",
        }

        response = self.client.post(self.endpoint, data)

        self.assertEqual(response.status_code, 401)

        self.assertEqual(set(response.data.keys()), set(["detail"]))

    def test_with_wrong_username(self):
        """Test with wrong username."""
        data = {
            "username_email": "wronguser",
            "password": "testpassword",
        }

        response = self.client.post(self.endpoint, data)

        self.assertEqual(response.status_code, 401)

        self.assertEqual(set(response.data.keys()), set(["detail"]))

    def test_with_wrong_email(self):
        """Test with wrong email."""
        data = {
            "username_email": "wrong.email@example.com",
            "password": "testpassword",
        }

        response = self.client.post(self.endpoint, data)

        self.assertEqual(response.status_code, 401)

        self.assertEqual(set(response.data.keys()), set(["detail"]))


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestProfile(APITestCase):
    """Test the profile endpoint."""

    endpoint = "/api/auth/profile/"

    def setUp(self):
        self.user = User.objects.create_user(
            first_name="Test",
            last_name="Test",
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
        )

    def test_get_with_no_auth(self):
        """Test GET request with no auth."""
        response = self.client.get(self.endpoint)

        self.assertEqual(response.status_code, 401)

    def test_get_with_auth(self):
        """Test GET request with auth."""
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.endpoint)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            set(response.data.keys()),
            set(["id", "photo", "first_name", "last_name", "username", "email", "is_staff"]),
        )

    def test_put_with_no_auth(self):
        """Test PUT request with no auth."""
        response = self.client.put(self.endpoint, {})

        self.assertEqual(response.status_code, 401)

    def test_put_with_auth(self):
        """Test PUT request with auth."""
        self.client.force_authenticate(user=self.user)

        data = {
            "first_name": "New Test",
            "last_name": "New Test",
            "username": "newtestuser",
            "email": "newtestuser@example.com",
        }

        response = self.client.put(self.endpoint, data)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data["photo"], None)

        self.assertEqual(response.data["first_name"], data["first_name"])
        self.assertEqual(response.data["last_name"], data["last_name"])
        self.assertEqual(response.data["username"], data["username"])
        self.assertEqual(response.data["email"], data["email"])

        self.assertEqual(User.objects.count(), 1)

    def test_patch_with_photo(self):
        """Test PATCH request with photo."""
        self.client.force_authenticate(user=self.user)

        image = Image.new("RGB", (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(tmp_file)
        tmp_file.seek(0)

        data = {
            "photo": tmp_file,
        }

        filename = pathlib.Path(tmp_file.name).name

        response = self.client.put(self.endpoint, data, format="multipart")

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data["photo"], f"/media/users/{filename}")

        self.assertEqual(User.objects.count(), 1)
