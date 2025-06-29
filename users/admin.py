from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'is_banned',
            'groups',
            'user_permissions'
        )}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_banned'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []

        # Se è staff, ma non superuser
        if request.user.is_staff:
            readonly = [
                'password',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
                'last_login',
                'date_joined',
            ]
            return readonly

        return super().get_readonly_fields(request, obj)

    def get_fieldsets(self, request, obj=None):
        return super().get_fieldsets(request, obj)

#admin.site.unregister(CustomUser)
admin.site.register(CustomUser, CustomUserAdmin)