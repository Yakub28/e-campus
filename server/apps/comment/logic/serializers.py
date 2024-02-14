from rest_framework import serializers

from server.apps.user.logic.serializers import UserSerializer

from ..models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ("id", "user", "topic", "text", "updated_at", "created_at")
        read_only_fields = ("id", "user", "updated_at", "created_at")

    def to_representation(self, instance):
        """Convert instance to representation"""
        data = super().to_representation(instance)

        data["user"] = UserSerializer(instance.user).data

        return data
