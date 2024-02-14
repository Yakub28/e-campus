from django.contrib.auth import get_user_model
from django.db import models

from server.apps.core.constants import ACTIVITY_CHOICES
from server.apps.core.models import BaseModel
from server.apps.group.models import Group

User = get_user_model()


class Topic(BaseModel):
    """Model definition for Group."""

    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="topics")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="topics")

    class Meta:
        """Meta definition for Topic."""

        verbose_name = "Topic"
        verbose_name_plural = "Topics"

    def __str__(self) -> str:
        """Unicode representation of Topic"""
        return self.title


class TopicActivity(BaseModel):
    """Model definition for TopicActivity."""

    activity = models.BooleanField(choices=ACTIVITY_CHOICES)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="activities")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="topic_activities")

    class Meta:
        """Meta definition for TopicActivity."""

        verbose_name = "TopicActivity"
        verbose_name_plural = "TopicActivities"

    def __str__(self) -> str:
        return self.get_activity_display()
