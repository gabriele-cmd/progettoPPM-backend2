from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    is_banned = models.BooleanField(
        default=False,
        verbose_name="Ban",
        help_text="Removes access from the website."
    )

    def __str__(self):
        return self.username
