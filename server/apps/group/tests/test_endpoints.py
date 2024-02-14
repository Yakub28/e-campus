from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from server.apps.group.models import Group

User = get_user_model()


class TestGroupEndpoints(APITestCase):
    """Test Group Endpoints."""

    def setUp(self):
        """Setup Example Data for the Test Class."""

        self.user1 = User.objects.create(
            username="testuser1",
            password="testpassword",
            is_staff=True,
        )

        self.user2 = User.objects.create(
            username="testuser2",
            password="testpassword",
            is_staff=True,
        )

        self.user3 = User.objects.create(
            username="testuser3",
            password="testpassword",
            is_staff=False,
        )

        self.group1 = Group.objects.create(
            name="Test Group",
            description="Test Group Description",
            owner=self.user1,
        )

        self.group1.members.add(self.user2)

        self.group2 = Group.objects.create(
            name="Test Group 2",
            description="Test Group 2 Description",
            owner=self.user2,
        )

    def test_group_list(self):
        """Test Group List Endpoint."""

        self.client.force_authenticate(user=self.user1)

        response = self.client.get("/api/groups/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        self.client.force_authenticate(user=self.user2)

        response = self.client.get("/api/groups/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_group_create(self):
        """Test Group Create Endpoint."""

        self.client.force_authenticate(user=self.user1)

        response = self.client.post(
            "/api/groups/",
            {
                "name": "Test Group 3",
                "description": "Test Group 3 Description",
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "Test Group 3")
        self.assertEqual(response.data["description"], "Test Group 3 Description")
        self.assertEqual(response.data["owner"]["id"], self.user1.id)
        self.assertEqual(len(response.data["members"]), 1)

        self.client.force_authenticate(user=self.user3)

        response = self.client.post(
            "/api/groups/",
            {
                "name": "Test Group 4",
                "description": "Test Group 4 Description",
            },
        )

        self.assertEqual(response.status_code, 403)

    def test_group_retrieve(self):
        """Test Group Retrieve Endpoint."""

        self.client.force_authenticate(user=self.user1)

        response = self.client.get(f"/api/groups/{self.group1.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Test Group")
        self.assertEqual(response.data["description"], "Test Group Description")
        self.assertEqual(response.data["owner"]["id"], self.user1.id)
        self.assertEqual(len(response.data["members"]), 2)

    def test_group_update(self):
        """Test Group Update Endpoint."""

        self.client.force_authenticate(user=self.user1)

        response = self.client.put(
            f"/api/groups/{self.group1.id}/",
            {
                "name": "Group Name Updated",
                "description": "Group Description Updated",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Group Name Updated")
        self.assertEqual(response.data["description"], "Group Description Updated")
        self.assertEqual(response.data["owner"]["id"], self.user1.id)
        self.assertEqual(len(response.data["members"]), 2)

    def test_group_delete(self):
        """Test Group Delete Endpoint."""

        self.client.force_authenticate(user=self.user1)

        response = self.client.delete(f"/api/groups/{self.group1.id}/")

        self.assertEqual(response.status_code, 204)

        response = self.client.get(f"/api/groups/{self.group1.id}/")

        self.assertEqual(response.status_code, 404)

    def test_group_join(self):
        """Test Group Join Endpoint."""

        self.client.force_authenticate(user=self.user3)

        response = self.client.get(f"/api/groups/join/?join_code={self.group1.join_code}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["detail"], "Joined group")

        response = self.client.get("/api/groups/join/?join_code=invalidjoincode")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["detail"], "Group not found")
