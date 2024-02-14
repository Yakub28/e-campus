from django.db import models


class BaseModel(models.Model):
    """Base model for all models in the project."""

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta class."""

        abstract = True
        ordering = ["-updated_at"]
