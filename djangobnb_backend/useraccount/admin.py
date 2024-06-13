from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, Permission
from .models import User
from property.models import Property, Reservation

class UserAdmin(BaseUserAdmin):
    list_display = ('name', 'email', 'is_staff', 'is_superuser', 'favorite_properties')
    ordering = ('email',)
    search_fields = ('email', 'name',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'avatar',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        
    )

    def favorite_properties(self, obj):
        favorites = obj.favorites.all()  # Assuming 'favorites' is the related_name for the ManyToManyField
        return ', '.join([property.name for property in favorites])

    favorite_properties.short_description = 'Favorite Properties'

admin.site.register(User, UserAdmin)


# Optionally unregister the Group model from the admin if not needed
# admin.site.unregister(Group)
