# app/accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, User


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        # Ensures existing profiles stay synced without crashing if not yet created
        if hasattr(instance, "profile"):
            instance.profile.save()