import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from accounts.models import Profile
from .models import PostMedia

DEFAULT_AVATAR = "avatars/default_avatar.jpg"


def delete_old_avatar(instance):
    if instance.avatar and instance.avatar.name != DEFAULT_AVATAR:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)


@receiver(post_delete, sender=Profile)
def delete_avatar_on_profile_delete(sender, instance, **kwargs):
    delete_old_avatar(instance)


@receiver(post_delete, sender=PostMedia)
def delete_post_media_files(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)