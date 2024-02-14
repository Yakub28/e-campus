from django.contrib.auth import get_user_model
from django.db import models

from server.apps.core.constants import ACTIVITY_CHOICES
from server.apps.core.models import BaseModel
from server.apps.topic.models import Topic

User = get_user_model()


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"Comment by {self.user.username} on {self.topic.title}"


class CommentActivity(BaseModel):
    activity = models.BooleanField(choices=ACTIVITY_CHOICES)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="activities")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_activities")

    class Meta:
        """Meta definition for CommentActivity."""

        verbose_name = "CommentActivity"
        verbose_name_plural = "CommentActivities"

    def __str__(self) -> str:
        return self.get_activity_display()
