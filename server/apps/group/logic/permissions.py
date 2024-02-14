from rest_framework import permissions


class GroupPermissions(permissions.BasePermission):
    """Permissions for Group viewset."""

    def has_permission(self, request, view):
        """Check permissions for Group viewset."""

        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        """Check permissions for Group viewset object."""

        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        return request.user == obj.owner
