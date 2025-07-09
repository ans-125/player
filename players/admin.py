from django.contrib import admin
from .models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    """إدارة اللاعبين"""
    
    list_display = ('name', 'position', 'birth_year', 'city', 'nationality', 'user', 'is_active', 'created_at')
    list_filter = ('position', 'birth_year', 'city', 'nationality', 'is_active', 'created_at')
    search_fields = ('name', 'phone', 'user__phone', 'user__first_name', 'description')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('معلومات اللاعب', {
            'fields': ('user', 'name', 'position', 'birth_year', 'city', 'nationality', 'phone')
        }),
        ('معلومات إضافية', {
            'fields': ('previous_clubs', 'description', 'video'),
            'classes': ('collapse',)
        }),
        ('إعدادات النظام', {
            'fields': ('is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        """تخصيص الاستعلام بناءً على صلاحيات المستخدم"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # إذا لم يكن مدير عام، اعرض فقط إعلانات المستخدم الحالي
        return qs.filter(user=request.user)
    
    def save_model(self, request, obj, form, change):
        """تعيين المستخدم الحالي كمالك للإعلان إذا لم يكن محدداً"""
        if not change and not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)

