from rest_framework import permissions

from server.apps.group.models import Group


class TopicPermissions(permissions.BasePermission):
    """Permissions for Topic viewset."""

    def has_permission(self, request, view):
        """Check permissions for Topic viewset."""
        if view.action not in ["list", "create"]:
            return True

        group_id = request.data.get("group") or request.query_params.get("group")

        if not group_id or not Group.objects.filter(id=group_id).exists():
            return False

        group = Group.objects.get(id=group_id)

        if request.method in permissions.SAFE_METHODS:
            return group.has_member(request.user) and request.user.is_authenticated

        return group.has_member(request.user) and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Check permissions for Topic viewset object."""
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated and obj.group.has_member(request.user)

        return request.user == obj.author or request.user == obj.group.owner
