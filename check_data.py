#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
django.setup()

from django.contrib.auth import get_user_model
from main.models import Category, Product
from reviews.models import Review

User = get_user_model()

def check_database():
    print("🔍 Проверка данных в базе данных...")
    print("=" * 50)
    
    # Проверяем пользователей
    print(f"👥 Пользователи ({User.objects.count()}):")
    for user in User.objects.all():
        status = "🔴 ЗАБАНЕН" if user.is_banned else "🟢 АКТИВЕН"
        print(f"   - {user.username} ({user.email}) - {status}")
        if user.is_banned and user.ban_reason:
            print(f"     Причина бана: {user.ban_reason}")
    print()
    
    # Проверяем категории
    print(f"📂 Категории ({Category.objects.count()}):")
    for category in Category.objects.all():
        print(f"   - {category.name} (товаров: {category.products.count()})")
    print()
    
    # Проверяем товары
    print(f"🛍️ Товары ({Product.objects.count()}):")
    for product in Product.objects.all():
        reviews_count = product.reviews.count()
        approved_reviews = product.reviews.filter(is_approved=True).count()
        print(f"   - {product.name} - {product.price} руб. (отзывов: {approved_reviews}/{reviews_count})")
    print()
    
    # Проверяем отзывы
    print(f"⭐ Отзывы ({Review.objects.count()}):")
    for review in Review.objects.all()[:5]:  # Показываем первые 5
        status = "✅ Одобрен" if review.is_approved else "⏳ На модерации"
        print(f"   - {review.user.username} о {review.product.name}")
        print(f"     Рейтинг: {review.rating}/5 - {review.title} - {status}")
    print()
    
    # Статистика по рейтингам
    print("📊 Статистика отзывов:")
    for rating in range(1, 6):
        count = Review.objects.filter(rating=rating, is_approved=True).count()
        stars = "★" * rating + "☆" * (5 - rating)
        print(f"   {stars} - {count} отзывов")
    
    print("\n✅ Проверка завершена!")

if __name__ == '__main__':
    check_database()
