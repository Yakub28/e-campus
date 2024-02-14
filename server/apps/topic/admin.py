from django.contrib import admin

from .models import Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "group",
        "author",
        "comments",
        "score",
        "updated_at",
        "created_at",
    )

    def comments(self, obj):
        return obj.comments.count()

    def score(self, obj):
        return obj.activities.filter(activity=1).count() - obj.activities.filter(activity=0).count()
