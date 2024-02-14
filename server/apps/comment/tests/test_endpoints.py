from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from server.apps.comment.models import Comment
from server.apps.group.models import Group
from server.apps.topic.models import Topic

User = get_user_model()


class TestCommentEndpoints(APITestCase):
    """Test Comment Endpoints."""

    def setUp(self):
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

        self.group1 = Group.objects.create(
            name="Test Group",
            description="Test Group Description",
            owner=self.user1,
        )

        self.group2 = Group.objects.create(
            name="Test Group 2",
            description="Test Group 2 Description",
            owner=self.user2,
        )

        self.group1.members.add(self.user1)

        self.topic1 = Topic.objects.create(
            title="Test Topic 1",
            description="Test Topic 1 description",
            author=self.user1,
            group=self.group1,
        )

        self.topic2 = Topic.objects.create(
            title="Test Topic 2",
            description="Test Topic 2 description",
            author=self.user2,
            group=self.group2,
        )

        self.comment1 = Comment.objects.create(
            user=self.user1,
            topic=self.topic1,
            text="Sample comment by user1",
        )

        self.comment2 = Comment.objects.create(
            user=self.user2,
            topic=self.topic1,
            text="Sample comment by user2",
        )

    def test_comment_list(self):
        """Test Comment List Endpoint"""
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(f"/api/comments/?topic={self.topic1.id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        self.client.force_authenticate(user=self.user2)

        response = self.client.get(f"/api/comments/?topic={self.topic1.id}")

        self.assertEqual(response.status_code, 403)

    def test_comment_create(self):
        """Test Comment Create Endpoint."""

        self.client.force_authenticate(user=self.user1)

        response = self.client.post(
            "/api/comments/",
            {
                "topic": self.topic1.id,
                "text": "New Comment",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_comment_retrieve(self):
        """Test Comment Retrieve Endpoint."""
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(f"/api/comments/{self.comment1.id}/")

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data["text"], "Sample comment by user1")
        self.assertEqual(response.data["user"]["id"], self.user1.id)

    def test_comment_update(self):
        """Test Comment Update Endpoint."""

        self.client.force_authenticate(user=self.user1)

        response = self.client.put(
            f"/api/comments/{self.comment1.id}/",
            {
                "topic": self.topic1.id,
                "text": "text comment Updated",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data["text"], "text comment Updated")
        self.assertEqual(response.data["id"], self.topic1.id)

    def test_comment_delete(self):
        """Test comment delete Endpoint"""

        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f"/api/comments/{self.comment1.id}/", data={"topic": self.topic1.id})

        self.assertEqual(response.status_code, 204)
        response = self.client.get(f"/api/comments/{self.comment1.id}/", data={"topic": self.topic1.id})

        self.assertEqual(response.status_code, 404)

    def test_comment_list_filter(self):
        """Test Comment list action filter."""
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(f"/api/comments/?topic={self.topic1.id}")

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data), 2)

        response = self.client.get(f"/api/comments/?topic={self.topic2.id}")

        self.assertEqual(response.status_code, 403)
