from django.contrib.auth import get_user_model
from django.db import models
from django.utils.crypto import get_random_string

from server.apps.core.models import BaseModel

User = get_user_model()


class Group(BaseModel):
    """Model definition for Group."""

    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_groups")
    members = models.ManyToManyField(User, related_name="belonged_groups")
    join_code = models.CharField(max_length=8, unique=True)

    class Meta:
        """Meta definition for Group."""

        verbose_name = "Group"
        verbose_name_plural = "Groups"

    def __str__(self) -> str:
        """Unicode representation of Group."""
        return self.name

    def has_member(self, user: User) -> bool:
        """Check if user is a member of this group"""

        return self.members.filter(id=user.id).exists()

    def save(self, *args, **kwargs):
        """Save instance"""

        isNew = self.pk is None

        if not self.join_code:
            self.join_code = self.generate_join_code()

        super().save(*args, **kwargs)

        if isNew:
            self.members.add(self.owner)

    @classmethod
    def generate_join_code(self) -> str:
        """Generate join code"""

        join_code = get_random_string(length=8)

        while self.objects.filter(join_code=join_code).exists():
            join_code = get_random_string(length=8)

        return join_code
