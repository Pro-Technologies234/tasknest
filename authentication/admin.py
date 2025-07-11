from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'gender', 'is_staff', 'is_superuser', 'created_at')
    list_filter = ('gender', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username')
    ordering = ('email',)
    readonly_fields = ('created_at', 'updated_at')  # ✅ Important for auto fields

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'gender', 'birthdate', 'profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2',
                'username', 'gender', 'birthdate', 'profile_image'
            ),
        }),
    )
