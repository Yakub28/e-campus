from rest_framework import permissions

from server.apps.topic.models import Topic


class CommentPermissions(permissions.BasePermission):
    """Permissions for Comment viewset."""

    def has_permission(self, request, view):
        """Permission for Comment viewset."""

        if view.action not in ["list", "create"]:
            return True

        topic_id = request.data.get("topic") or request.query_params.get("topic")

        if not topic_id or not Topic.objects.filter(id=topic_id).exists():
            return False

        topic = Topic.objects.get(id=topic_id)

        return topic.group.has_member(request.user)

    def has_object_permission(self, request, view, obj):
        """Permission for Comment viewset object."""
        if request.method in permissions.SAFE_METHODS:
            return obj.topic.group.has_member(request.user)

        return request.user == obj.user or request.user == obj.topic.group.owner
