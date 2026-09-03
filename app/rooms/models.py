from django.db import models


class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(
        max_length=50, blank=True, null=True, help_text="FontAwesome class"
    )
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Amenities"

    def __str__(self):
        return self.name


class RoomType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField(default=2)
    image = models.ImageField(upload_to="room_types/", blank=True, null=True)
    # ManyToMany ជាមួយ Amenity ក្នុង app តែមួយ
    amenities = models.ManyToManyField(
        Amenity, related_name="room_types", blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - ${self.base_price}/night"


class Room(models.Model):
    class RoomStatus(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Available"
        OCCUPIED = "OCCUPIED", "Occupied"
        MAINTENANCE = "MAINTENANCE", "Under Maintenance"
        CLEANING = "CLEANING", "Cleaning"

    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.ForeignKey(
        RoomType, on_delete=models.CASCADE, related_name="rooms"
    )
    status = models.CharField(
        max_length=20, choices=RoomStatus.choices, default=RoomStatus.AVAILABLE
    )

    def __str__(self):
        return f"Room {self.room_number} ({self.room_type.name})"