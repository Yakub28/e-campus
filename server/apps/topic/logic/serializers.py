from rest_framework import serializers

from server.apps.group.logic.serializers import GroupSerializer
from server.apps.user.logic.serializers import UserSerializer

from ..models import Topic


class TopicSerializer(serializers.ModelSerializer):
    """Serializer for Group model"""

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Topic
        fields = (
            "id",
            "title",
            "description",
            "author",
            "group",
            "updated_at",
            "created_at",
        )
        read_only_fields = ("id", "author", "updated_at", "created_at")

    def to_representation(self, instance):
        """Convert instance to representation"""
        data = super().to_representation(instance)

        data["author"] = UserSerializer(instance.author).data

        data["group"] = GroupSerializer(instance.group, context=self.context).data

        return data
