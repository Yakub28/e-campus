from django.contrib.auth import get_user_model
from django.test import TransactionTestCase

from server.apps.group.models import Group
from server.apps.topic.models import Topic

from ..models import Comment, CommentActivity

User = get_user_model()


class CommentModelTest(TransactionTestCase):
    """Test Comment Model."""

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

        self.topic1 = Topic.objects.create(
            title="Test Topic 1",
            description="Test Topic 1 description",
            author=self.user1,
            group=self.group1,
        )

        self.topic2 = Topic.objects.create(
            title="Test Topic 2",
            description="Sample Topic 2 description",
            author=self.user2,
            group=self.group2,
        )

        self.comment = Comment.objects.create(
            user=self.user1,
            topic=self.topic1,
            text="Sample comment",
        )

    def test_fields(self):
        """Test Comment Model fields."""
        self.assertTrue(hasattr(Comment, "user"))
        self.assertTrue(hasattr(Comment, "topic"))
        self.assertTrue(hasattr(Comment, "text"))

    def test_comment_str_method(self):
        """Test Comment Model str method."""
        expected_str = f"Comment by {self.user1.username} on {self.topic1.title}"

        self.assertEqual(str(self.comment), expected_str)

    def test_comment_creation(self):
        """Test Comment instance creation."""
        self.assertTrue(isinstance(self.comment, Comment))
        self.assertEqual(self.comment.user, self.user1)
        self.assertEqual(self.comment.topic, self.topic1)
        self.assertEqual(self.comment.text, "Sample comment")

    def test_comment_update(self):
        """Test Comment instance update."""
        self.comment.user = self.user2
        self.comment.topic = self.topic2
        self.comment.text = "Updated text"

        self.comment.save()

        self.assertEqual(self.comment.user, self.user2)
        self.assertEqual(self.comment.topic, self.topic2)
        self.assertEqual(self.comment.text, "Updated text")

    def test_comment_delete(self):
        """Test Comment instance delete."""
        self.comment.delete()

        self.assertEqual(Comment.objects.count(), 0)

    def test_comment_user_relationship(self):
        """Test Comment and User Relationship."""
        self.assertEqual(self.user1.comments.count(), 1)
        self.assertEqual(self.user1.comments.first(), self.comment)

    def test_comment_topic_relationship(self):
        """Test Comment and Topic Relationship."""
        self.assertEqual(self.topic1.comments.count(), 1)
        self.assertEqual(self.topic1.comments.first(), self.comment)


class CommentActivityModelTest(TransactionTestCase):
    """Test CommentActivity Model."""

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

        self.topic1 = Topic.objects.create(
            title="Test Topic",
            description="Test Topic description",
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
            text="Test comment 1",
        )
        self.comment2 = Comment.objects.create(
            user=self.user2,
            topic=self.topic2,
            text="Test comment 2",
        )

        self.commentActivity = CommentActivity.objects.create(
            activity=True,
            comment=self.comment1,
            user=self.user1,
        )

    def test_fields(self):
        """Test CommentActivity Model fields."""
        self.assertTrue(hasattr(CommentActivity, "activity"))
        self.assertTrue(hasattr(CommentActivity, "comment"))
        self.assertTrue(hasattr(CommentActivity, "user"))

    def test_comment_str_method(self):
        """Test CommentActivity Model str method."""
        expected_str = self.commentActivity.get_activity_display()

        self.assertEqual(self.commentActivity.__str__(), expected_str)

    def test_comment_activity_creation(self):
        """Test CommentActivity instance creation."""
        self.assertTrue(isinstance(self.commentActivity, CommentActivity))
        self.assertEqual(self.commentActivity.activity, True)
        self.assertEqual(self.commentActivity.get_activity_display(), "Upvote")
        self.assertEqual(self.commentActivity.comment, self.comment1)
        self.assertEqual(self.commentActivity.user, self.user1)

    def test_comment_activity_update(self):
        """Test CommentActivity instance update."""
        self.commentActivity.activity = False
        self.commentActivity.comment = self.comment2
        self.commentActivity.user = self.user2

        self.commentActivity.save()

        self.assertEqual(self.commentActivity.activity, False)
        self.assertEqual(self.commentActivity.get_activity_display(), "Downvote")
        self.assertEqual(self.commentActivity.comment, self.comment2)
        self.assertEqual(self.commentActivity.user, self.user2)

    def test_comment_activity_delete(self):
        """Test CommentActivity instance delete."""
        self.commentActivity.delete()

        self.assertEqual(CommentActivity.objects.count(), 0)

    def test_comment_acitivity_comment_relationship(self):
        """Test CommentActivity and Comment Relationship."""
        self.assertEqual(self.comment1.activities.count(), 1)
        self.assertEqual(self.comment1.activities.first(), self.commentActivity)

    def test_comment_activity_user_relationship(self):
        """Test CommentActivity and User Relationship."""
        self.assertEqual(self.user1.comment_activities.count(), 1)
        self.assertEqual(self.user1.comment_activities.first(), self.commentActivity)
