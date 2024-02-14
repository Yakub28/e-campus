from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .logic.filters import TopicFilter
from .logic.permissions import TopicPermissions
from .logic.serializers import TopicSerializer
from .models import Topic


class TopicViewSet(viewsets.ModelViewSet):
    """ViewSet for Topic model"""

    model = Topic
    queryset = Topic.objects.all()

    serializer_class = TopicSerializer

    permission_classes = [TopicPermissions]

    filter_backends = [DjangoFilterBackend]
    filterset_class = TopicFilter

    def filter_queryset(self, queryset):
        """Use Filter class if it is list action"""
        if self.action != "list":
            self.filterset_class = None
        return super().filter_queryset(queryset)
