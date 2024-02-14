from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "user",
        "topic",
        "score",
        "updated_at",
        "created_at",
    )

    def score(self, obj):
        return obj.activities.filter(activity=1).count() - obj.activities.filter(activity=0).count()
