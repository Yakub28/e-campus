from django_filters import rest_framework as filters

from server.apps.comment.models import Comment


class CommentFilter(filters.FilterSet):
    topic = filters.CharFilter(field_name="topic__id", required=True)

    class Meta:
        model = Comment
        fields = ["topic"]
