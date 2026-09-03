from rest_framework import serializers
from .models import Room, RoomType


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    room_type_detail = RoomTypeSerializer(source="room_type", read_only=True)

    class Meta:
        model = Room
        fields = [
            "id",
            "room_number",
            "status",
            "room_type",
            "room_type_detail",
        ]