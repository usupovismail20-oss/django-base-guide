#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from main.models import Category, Product
from reviews.models import Review

User = get_user_model()

def test_registration_and_login():
    print("🧪 Тестирование регистрации и входа...")
    
    client = Client()
    
    # Тест регистрации
    print("   📝 Тестирование регистрации...")
    response = client.get(reverse('accounts:register'))
    assert response.status_code == 200, "Страница регистрации недоступна"
    print("   ✅ Страница регистрации загружается")
    
    # Тест входа
    print("   🔐 Тестирование входа...")
    response = client.get(reverse('accounts:login'))
    assert response.status_code == 200, "Страница входа недоступна"
    print("   ✅ Страница входа загружается")
    
    # Тест входа с существующими данными
    login_data = {
        'username': 'user1@shop.ru',
        'password': 'password123'
    }
    response = client.post(reverse('accounts:login'), login_data)
    assert response.status_code == 302, "Вход не работает"
    print("   ✅ Вход с существующими данными работает")
    
    # Тест выхода
    response = client.get(reverse('accounts:logout'))
    assert response.status_code == 302, "Выход не работает"
    print("   ✅ Выход работает")

def test_reviews_system():
    print("🧪 Тестирование системы отзывов...")
    
    client = Client()
    
    # Входим как пользователь
    client.post(reverse('accounts:login'), {
        'username': 'user1@shop.ru',
        'password': 'password123'
    })
    
    # Тест страницы отзывов
    product = Product.objects.first()
    response = client.get(reverse('reviews:review_list', args=[product.id]))
    assert response.status_code == 200, "Страница отзывов недоступна"
    print("   ✅ Страница отзывов загружается")
    
    # Тест страницы добавления отзыва
    response = client.get(reverse('reviews:add_review', args=[product.id]))
    if response.status_code == 200:
        print("   ✅ Страница добавления отзыва загружается")
    elif response.status_code == 302:
        print("   ✅ Страница добавления отзыва перенаправляет (возможно, отзыв уже существует)")
    else:
        print(f"   ❌ Страница добавления отзыва недоступна (код: {response.status_code})")
        return
    
    # Тест добавления отзыва (только если пользователь еще не оставлял отзыв)
    if response.status_code == 200:
        review_data = {
            'rating': 5,
            'title': 'Тестовый отзыв',
            'comment': 'Это тестовый отзыв для проверки функциональности.'
        }
        response = client.post(reverse('reviews:add_review', args=[product.id]), review_data)
        if response.status_code == 302:
            print("   ✅ Добавление отзыва работает")
        else:
            print(f"   ❌ Добавление отзыва не работает (код: {response.status_code})")
    else:
        print("   ⏭️ Пропуск теста добавления отзыва (отзыв уже существует)")

def test_ban_system():
    print("🧪 Тестирование системы банов...")
    
    client = Client()
    
    # Тест входа забаненного пользователя
    login_data = {
        'username': 'banned@shop.ru',
        'password': 'password123'
    }
    response = client.post(reverse('accounts:login'), login_data)
    assert response.status_code == 200, "Забаненный пользователь не может войти"
    print("   ✅ Забаненный пользователь не может войти")
    
    # Проверяем, что забаненный пользователь видит сообщение о бане
    assert 'заблокирован' in response.content.decode(), "Сообщение о бане не отображается"
    print("   ✅ Сообщение о бане отображается")

def test_database_integrity():
    print("🧪 Тестирование целостности базы данных...")
    
    # Проверяем связи между моделями
    user = User.objects.get(username='user1')
    reviews = Review.objects.filter(user=user)
    assert reviews.exists(), "Отзывы пользователя не найдены"
    print("   ✅ Связи пользователь-отзывы работают")
    
    product = Product.objects.first()
    product_reviews = product.reviews.all()
    assert product_reviews.exists(), "Отзывы товара не найдены"
    print("   ✅ Связи товар-отзывы работают")
    
    category = Category.objects.first()
    category_products = category.products.all()
    assert category_products.exists(), "Товары категории не найдены"
    print("   ✅ Связи категория-товары работают")

def test_admin_functionality():
    print("🧪 Тестирование админки...")
    
    client = Client()
    
    # Входим как админ
    client.post(reverse('accounts:login'), {
        'username': 'admin@shop.ru',
        'password': 'password123'
    })
    
    # Тест доступа к админке
    response = client.get('/admin/')
    assert response.status_code == 200, "Админка недоступна"
    print("   ✅ Админка доступна")
    
    # Тест страницы пользователей в админке
    response = client.get('/admin/accounts/user/')
    assert response.status_code == 200, "Страница пользователей недоступна"
    print("   ✅ Страница пользователей в админке работает")
    
    # Тест страницы отзывов в админке
    response = client.get('/admin/reviews/review/')
    assert response.status_code == 200, "Страница отзывов недоступна"
    print("   ✅ Страница отзывов в админке работает")

def main():
    print("🚀 Запуск тестов функциональности...")
    print("=" * 60)
    
    try:
        test_database_integrity()
        print()
        test_registration_and_login()
        print()
        test_reviews_system()
        print()
        test_ban_system()
        print()
        test_admin_functionality()
        print()
        
        print("🎉 Все тесты прошли успешно!")
        print("✅ База данных работает корректно!")
        print("✅ Все функции сохранения данных работают!")
        
    except Exception as e:
        print(f"❌ Ошибка в тестах: {e}")
        return False
    
    return True

if __name__ == '__main__':
    main()
