from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """إدارة المستخدمين المخصصة"""
    
    list_display = ('phone', 'first_name', 'last_name', 'city', 'birth_year', 'is_admin', 'is_active', 'created_at')
    list_filter = ('is_admin', 'is_active', 'city', 'birth_year', 'created_at')
    search_fields = ('phone', 'first_name', 'last_name', 'city')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('المعلومات الشخصية', {'fields': ('first_name', 'last_name', 'email', 'birth_year', 'city')}),
        ('الصلاحيات', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin', 'groups', 'user_permissions')}),
        ('التواريخ المهمة', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'first_name', 'last_name', 'password1', 'password2', 'birth_year', 'city'),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'date_joined')

