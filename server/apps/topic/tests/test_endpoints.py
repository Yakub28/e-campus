from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from server.apps.group.models import Group
from server.apps.topic.models import Topic

User = get_user_model()


class TestTopicEndpoints(APITestCase):
    """Test Topic Endpoints."""

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
            is_staff=True,
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
            owner=self.user3,
        )

        self.topic1 = Topic.objects.create(
            title="Test Topic",
            description="Test Topic Description",
            author=self.user1,
            group=self.group1,
        )

        self.topic2 = Topic.objects.create(
            title="Test Topic 2",
            description="Test Topic 2 Description",
            author=self.user2,
            group=self.group1,
        )

        self.topic3 = Topic.objects.create(
            title="Test Topic 3",
            description="Test Topic 3 Description",
            author=self.user3,
            group=self.group2,
        )

    def test_topic_list(self):
        """Test Topic List Endpoint."""

        self.client.force_authenticate(user=self.user1)

        response = self.client.get(f"/api/topics/?group={self.group1.id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        # --------------------------------------- #
        self.client.force_authenticate(user=self.user2)

        response = self.client.get(f"/api/topics/?group={self.group1.id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        # --------------------------------------- #
        self.client.force_authenticate(user=self.user3)

        response = self.client.get(f"/api/topics/?group={self.group2.id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        # --------------------------------------- #
        self.client.force_authenticate(user=self.user3)

        response = self.client.get(f"/api/topics/?group={self.group1.id}")

        self.assertEqual(response.status_code, 403)

    def test_topic_create(self):
        """Test Topic Create Endpoint."""

        self.client.force_authenticate(user=self.user1)

        response = self.client.post(
            "/api/topics/",
            {
                "title": "Test Topic 4",
                "description": "Test Topic 4 Description",
                "group": self.group1.id,
            },
        )

        self.assertEqual(response.status_code, 201)

        self.assertEqual(response.data["title"], "Test Topic 4")
        self.assertEqual(response.data["description"], "Test Topic 4 Description")
        self.assertEqual(response.data["author"]["id"], self.user1.id)

        response = self.client.get(f"/api/topics/?group={self.group1.id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        # -------------------------------------------#
        self.client.force_authenticate(user=self.user1)

        response = self.client.post(
            "/api/topics/",
            {
                "title": "Test Topic 4",
                "description": "Test Topic 4 Description",
                "group": self.group2.id,
            },
        )

        self.assertEqual(response.status_code, 403)

    def test_topic_retrieve(self):
        """Test Topic Retrieve Endpoint."""

        self.client.force_authenticate(user=self.user1)

        response = self.client.get(f"/api/topics/{self.topic1.id}/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/api/topics/100/")
        self.assertEqual(response.status_code, 404)

    def test_topic_update(self):
        """Test Topic Update Endpoint."""

        self.client.force_authenticate(user=self.user1)

        response = self.client.put(
            f"/api/topics/{self.topic1.id}/?group={self.group1.id}",
            {"title": "Topic Name Updated", "description": "Topic Description Updated", "group": self.group1.id},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Topic Name Updated")
        self.assertEqual(response.data["description"], "Topic Description Updated")
        self.assertEqual(response.data["author"]["id"], self.user1.id)
        self.assertEqual(response.data["group"]["id"], self.group1.id)

    def test_topic_delete(self):
        """Test Group Delete Endpoint."""

        self.client.force_authenticate(user=self.user1)

        response = self.client.delete(f"/api/topics/{self.topic1.id}/")
        self.assertEqual(response.status_code, 204)

        response = self.client.get(f"/api/topics/{self.topic1.id}/")
        self.assertEqual(response.status_code, 404)

        response = self.client.delete(f"/api/topics/{self.topic2.id}/")
        self.assertEqual(response.status_code, 204)

        response = self.client.delete(f"/api/topics/{self.topic3.id}/")
        self.assertEqual(response.status_code, 403)

    def test_topic_list_filter(self):
        """Test Topic list action filter."""

        self.client.force_authenticate(user=self.user1)

        self.group2.members.add(self.user1)

        responseFirstGroup = self.client.get(f"/api/topics/?group={self.group1.id}")

        responseSecondGroup = self.client.get(f"/api/topics/?group={self.group2.id}")

        self.assertEqual(responseFirstGroup.status_code, 200)
        self.assertEqual(responseSecondGroup.status_code, 200)

        self.assertEqual(len(responseFirstGroup.data), 2)
        self.assertEqual(len(responseSecondGroup.data), 1)
