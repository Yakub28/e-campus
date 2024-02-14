from django.contrib import admin

from .models import Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "owner",
        "member_count",
        "topic_count",
        "join_code",
        "updated_at",
        "created_at",
    )

    def member_count(self, obj):
        return obj.members.count()

    def topic_count(self, obj):
        return obj.topics.count()
