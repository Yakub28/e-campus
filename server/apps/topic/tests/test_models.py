from django.contrib.auth import get_user_model
from django.test import TransactionTestCase

from server.apps.group.models import Group

from ..models import Topic, TopicActivity

User = get_user_model()


class TopicModelTest(TransactionTestCase):
    """Test Topic Model."""

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

        self.group1 = Group.objects.create(
            name="Test Group 1",
            description="Test Group 1 Description",
            owner=self.user1,
            join_code="123456",
        )

        self.group2 = Group.objects.create(
            name="Test Group 2",
            description="Test Group 2 Description",
            owner=self.user2,
            join_code="123123",
        )

        self.topic = Topic.objects.create(
            title="Test Topic",
            description="Test Topic Description",
            author=self.user1,
            group=self.group1,
        )

    def test_fields(self):
        """Test Topic Model fields."""
        self.assertTrue(hasattr(Topic, "title"))
        self.assertTrue(hasattr(Topic, "description"))
        self.assertTrue(hasattr(Topic, "author"))
        self.assertTrue(hasattr(Topic, "group"))

    def test_topic_str_method(self):
        """Test Topic Model str method."""
        expected_str = self.topic.title

        self.assertEqual(self.topic.__str__(), expected_str)

    def test_topic_creation(self):
        """Test Topic Model instance creation."""
        self.assertTrue(isinstance(self.topic, Topic))
        self.assertEqual(self.topic.title, "Test Topic")
        self.assertEqual(self.topic.description, "Test Topic Description")
        self.assertEqual(self.topic.author, self.user1)
        self.assertEqual(self.topic.group, self.group1)

    def test_topic_update(self):
        """Test Topic Model instance update."""
        self.topic.title = "Topic Title Updated"
        self.topic.description = "Description Updated"
        self.topic.author = self.user2
        self.topic.group = self.group2

        self.topic.save()

        self.assertEqual(self.topic.title, "Topic Title Updated")
        self.assertEqual(self.topic.description, "Description Updated")
        self.assertEqual(self.topic.author, self.user2)
        self.assertEqual(self.topic.group, self.group2)

    def test_topic_delete(self):
        """Test Topic Model instance delete."""
        self.topic.delete()

        self.assertEqual(Topic.objects.count(), 0)

    def test_topic_user_relationship(self):
        """Test Topic and User Relationship"""
        self.assertEqual(self.user1.topics.count(), 1)
        self.assertEqual(self.user1.topics.first(), self.topic)

    def test_topic_group_relationship(self):
        """Test Topic and Group Relationship"""
        self.assertEqual(self.group1.topics.count(), 1)
        self.assertEqual(self.group1.topics.first(), self.topic)


class TopicActivityModelTest(TransactionTestCase):
    """Test TopicActivity Model."""

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
            name="Test Group 1",
            description="Test Group 1 Description",
            owner=self.user1,
            join_code="123456",
        )

        self.topic1 = Topic.objects.create(
            title="Test Topic 1",
            description="Test Topic 1 description",
            author=self.user1,
            group=self.group,
        )

        self.topic2 = Topic.objects.create(
            title="Test Topic 2",
            description="Test Topic 2 description2",
            author=self.user2,
            group=self.group,
        )

        self.topicActivity = TopicActivity.objects.create(
            activity=True,
            topic=self.topic1,
            user=self.user1,
        )

    def test_fields(self):
        """Test TopicActivity Model fields."""
        self.assertTrue(hasattr(TopicActivity, "activity"))
        self.assertTrue(hasattr(TopicActivity, "topic"))
        self.assertTrue(hasattr(TopicActivity, "user"))

    def test_topic_activity_str_method(self):
        """Test TopicActivity Model str method."""
        expected_str = self.topicActivity.get_activity_display()

        self.assertEqual(self.topicActivity.__str__(), expected_str)

    def test_topic_activity_creation(self):
        """Test TopicActivity instance creation."""
        self.assertTrue(isinstance(self.topicActivity, TopicActivity))
        self.assertEqual(self.topicActivity.activity, True)
        self.assertEqual(self.topicActivity.get_activity_display(), "Upvote")
        self.assertEqual(self.topicActivity.topic, self.topic1)
        self.assertEqual(self.topicActivity.user, self.user1)

    def test_topic_activity_update(self):
        """Test TopicActivity instance update."""
        self.topicActivity.activity = 0
        self.topicActivity.topic = self.topic2
        self.topicActivity.user = self.user2

        self.topicActivity.save()

        self.assertEqual(self.topicActivity.activity, 0)
        self.assertEqual(self.topicActivity.get_activity_display(), "Downvote")
        self.assertEqual(self.topicActivity.topic, self.topic2)
        self.assertEqual(self.topicActivity.user, self.user2)

    def test_topic_activity_delete(self):
        """Test TopicActivity instance delete."""
        self.topicActivity.delete()

        self.assertEqual(TopicActivity.objects.count(), 0)

    def test_topic_acitivity_topic_relationship(self):
        """Test TopicActivity and Topic Relationship"""
        self.assertEqual(self.topic1.activities.count(), 1)
        self.assertEqual(self.topic1.activities.first(), self.topicActivity)

    def test_topic_acitivity_user_relationship(self):
        """Test TopicActivity and User Relationship"""
        self.assertEqual(self.user1.topic_activities.count(), 1)
        self.assertEqual(self.user1.topic_activities.first(), self.topicActivity)
