from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        RECEPTIONIST = 'RECEPTIONIST', 'Receptionist'
        HOUSEKEEPER = 'HOUSEKEEPER', 'Housekeeper'
        GUEST = 'GUEST', 'Guest'

    role = models.CharField(max_length=15, choices=Role.choices, default=Role.GUEST)
    phone = models.CharField(max_length=20, blank=True, null=True)
    national_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"



class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    id_proof = models.ImageField(
        upload_to="id_proofs/", blank=True, null=True
    )  # or FileField
    avatar = models.ImageField(
        upload_to="avatars/", default="avatars/default.png", blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"    