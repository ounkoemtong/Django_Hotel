from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Room
from .serializers import RoomSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def room_dashboard_api(request):
    status_filter = request.GET.get("status", "")
    type_filter = request.GET.get("type", "")

    rooms = Room.objects.select_related("room_type").prefetch_related(
        "room_type__amenities"
    )

    if status_filter:
        rooms = rooms.filter(status=status_filter)
    if type_filter:
        rooms = rooms.filter(room_type__id=type_filter)

    stats = {
        "total": Room.objects.count(),
        "available": Room.objects.filter(
            status=Room.RoomStatus.AVAILABLE
        ).count(),
        "occupied": Room.objects.filter(
            status=Room.RoomStatus.OCCUPIED
        ).count(),
        "cleaning": Room.objects.filter(
            status=Room.RoomStatus.CLEANING
        ).count(),
        "maintenance": Room.objects.filter(
            status=Room.RoomStatus.MAINTENANCE
        ).count(),
    }

    serializer = RoomSerializer(rooms, many=True)

    return Response(
        {
            "stats": stats,
            "rooms": serializer.data,
        },
        status=status.HTTP_200_OK,
    )

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Room
from .serializers import RoomSerializer


class UpdateRoomStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    serializer_class = RoomSerializer  # ប្រាប់ DRF ឱ្យបង្កើត HTML Form តាម Serializer នេះ

    def patch(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        # partial=True អនុញ្ញាតឱ្យកែប្រែតែ field status មួយក៏បាន
        serializer = RoomSerializer(room, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": f"room  {room.room_number} already change to  {room.status}!",
                    "room": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # បើចង់ឱ្យប្រើ method POST បានដែរ
    def post(self, request, room_id):
        return self.patch(request, room_id)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_room_api(request, room_id):
    # ស្វែងរកបន្ទប់តាម id បើគ្មានទេនឹង return 404
    room = get_object_or_404(Room, id=room_id)
    
    room_number = room.room_number
    room.delete()  # លុបចេញពី Database

    return Response(
        {"message": f"Your {room_number} has been delete successfully bro  !"},
        status=status.HTTP_200_OK  # ឬ status.HTTP_204_NO_CONTENT
    )    