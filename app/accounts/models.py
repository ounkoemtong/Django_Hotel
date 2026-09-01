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