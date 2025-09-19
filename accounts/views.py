from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import UserRegistrationForm, UserLoginForm

User = get_user_model()


def register_view(request):
    if request.user.is_authenticated:
        return redirect('main:product_list')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('main:product_list')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('main:product_list')
    
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_banned:
                messages.error(request, f'Ваш аккаунт заблокирован. Причина: {user.ban_reason or "Не указана"}')
                return render(request, 'accounts/login.html', {'form': form})
            
            login(request, user)
            messages.success(request, 'Вход выполнен успешно!')
            return redirect('main:product_list')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('main:product_list')
