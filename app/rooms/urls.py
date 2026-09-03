from django.urls import path
from . import views
from .views import UpdateRoomStatusAPIView

app_name = "rooms"

urlpatterns = [
    path("dashboard/", views.room_dashboard_api, name="room_dashboard_api"),
    path(
        "update-status/<int:room_id>/",
        UpdateRoomStatusAPIView.as_view(),
        name="update_room_status_api",
    ),
    path("delete/<int:room_id>/",views.delete_room_api,name='delete_room_api')

]