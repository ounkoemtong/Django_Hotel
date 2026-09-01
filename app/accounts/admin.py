from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'phone', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Info', {'fields': ('role', 'phone', 'national_id')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Info', {'fields': ('role', 'phone', 'national_id')}),
    )

    # CREATE: Only superuser can add new users
    def has_add_permission(self, request):
        return request.user.is_superuser

    # READ: Only superuser can view users in admin
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    # UPDATE: Only superuser can edit users
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    # DELETE: Only superuser can delete users
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser