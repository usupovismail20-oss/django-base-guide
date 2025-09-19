from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_banned', 'is_staff', 'date_joined')
    list_filter = ('is_banned', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email')}),
        ('Разрешения', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Статус бана', {
            'fields': ('is_banned', 'ban_reason', 'banned_at'),
            'classes': ('collapse',),
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
    
    def ban_user(self, request, queryset):
        from django.utils import timezone
        queryset.update(is_banned=True, banned_at=timezone.now())
        self.message_user(request, f"Забанено пользователей: {queryset.count()}")
    
    def unban_user(self, request, queryset):
        queryset.update(is_banned=False, ban_reason=None, banned_at=None)
        self.message_user(request, f"Разбанено пользователей: {queryset.count()}")
    
    ban_user.short_description = "Забанить выбранных пользователей"
    unban_user.short_description = "Разбанить выбранных пользователей"
    
    actions = [ban_user, unban_user]
