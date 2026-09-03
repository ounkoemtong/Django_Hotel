# app/urls.py
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('app.accounts.urls')),
    path('rooms/', include('app.rooms.urls')),
    # path('bookings/', include('app.bookings.urls')),
    # path('billings/', include('app.billings.urls')),
    # path('operations/', include('app.operations.urls')),

]

