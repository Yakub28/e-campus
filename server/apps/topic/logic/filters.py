from django_filters import rest_framework as filters

from server.apps.comment.models import Topic


class TopicFilter(filters.FilterSet):
    group = filters.CharFilter(field_name="group__id", required=True)

    class Meta:
        model = Topic
        fields = ["group"]
