from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = 'Пользователи'
    
    def ready(self):
        from django.contrib import admin
        from django.utils.translation import gettext_lazy as _
        
        # Настройка заголовков админки
        admin.site.site_header = _('Администрирование магазина')
        admin.site.site_title = _('Админка магазина')
        admin.site.index_title = _('Панель управления')
        admin.site.site_url = '/'
