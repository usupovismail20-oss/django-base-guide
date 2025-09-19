from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse


class BanCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Проверяем только аутентифицированных пользователей
        if request.user.is_authenticated and request.user.is_banned:
            # Исключаем страницы входа, выхода и регистрации
            if not request.path.startswith('/accounts/'):
                messages.error(request, f'Ваш аккаунт заблокирован. Причина: {request.user.ban_reason or "Не указана"}')
                return redirect('accounts:login')
        
        response = self.get_response(request)
        return response
