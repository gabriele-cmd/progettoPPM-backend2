from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from users.models import CustomUser


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)


@receiver(post_save, sender=CustomUser)
def assign_default_group(sender, instance, created, **kwargs):
    if created:
        group_name = "moderator" if instance.is_staff else "user"
        group, _ = Group.objects.get_or_create(name=group_name)
        instance.groups.add(group)