from django_filters import rest_framework as filters
from rest_framework import viewsets

from .logic.filters import CommentFilter
from .logic.permissions import CommentPermissions
from .logic.serializers import CommentSerializer
from .models import Comment


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for Comment model"""

    model = Comment
    queryset = Comment.objects.all()

    serializer_class = CommentSerializer
    permission_classes = [
        CommentPermissions,
    ]
    filter_backends = [
        filters.DjangoFilterBackend,
    ]
    filterset_class = CommentFilter

    def filter_queryset(self, queryset):
        """Use Filter class if it is list action"""
        if self.action != "list":
            self.filterset_class = None
        return super().filter_queryset(queryset)
