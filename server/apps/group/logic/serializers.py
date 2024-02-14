from rest_framework import serializers

from server.apps.user.logic.serializers import UserSerializer

from ..models import Group


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for Group model"""

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    members = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = [
            "id",
            "name",
            "description",
            "members",
            "owner",
            "join_code",
            "updated_at",
            "created_at",
        ]
        read_only_fields = ("id", "members", "join_code", "updated_at", "created_at")

    def to_representation(self, instance):
        """Convert instance to representation"""
        data = super().to_representation(instance)

        data["owner"] = UserSerializer(instance.owner).data

        if self.context.get("request").user != instance.owner:
            data.pop("join_code")

        return data

    def get_members(self, obj):
        """Get members"""
        return UserSerializer(obj.members.all(), many=True).data


class JoinSerializer(serializers.Serializer):
    """Serializer for join group"""

    join_code = serializers.CharField(required=True)
