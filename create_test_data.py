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
from django.utils import timezone

User = get_user_model()

def create_test_data():
    print("Создание тестовых данных...")
    
    # Создаем категории
    categories_data = [
        {'name': 'Смартфоны', 'slug': 'smartphones'},
        {'name': 'Ноутбуки', 'slug': 'laptops'},
        {'name': 'Планшеты', 'slug': 'tablets'},
        {'name': 'Наушники', 'slug': 'headphones'},
        {'name': 'Аксессуары', 'slug': 'accessories'},
    ]
    
    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={'name': cat_data['name']}
        )
        categories.append(category)
        if created:
            print(f"Создана категория: {category.name}")
    
    # Создаем тестовых пользователей
    users_data = [
        {'username': 'admin', 'email': 'admin@shop.ru', 'is_staff': True, 'is_superuser': True},
        {'username': 'user1', 'email': 'user1@shop.ru'},
        {'username': 'user2', 'email': 'user2@shop.ru'},
        {'username': 'user3', 'email': 'user3@shop.ru'},
        {'username': 'banned_user', 'email': 'banned@shop.ru', 'is_banned': True, 'ban_reason': 'Нарушение правил'},
    ]
    
    users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'is_staff': user_data.get('is_staff', False),
                'is_superuser': user_data.get('is_superuser', False),
                'is_banned': user_data.get('is_banned', False),
                'ban_reason': user_data.get('ban_reason', ''),
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"Создан пользователь: {user.username}")
        users.append(user)
    
    # Создаем товары
    products_data = [
        {
            'name': 'iPhone 15 Pro',
            'slug': 'iphone-15-pro',
            'description': 'Новейший смартфон от Apple с титановым корпусом и чипом A17 Pro',
            'price': 99990.00,
            'category': categories[0]
        },
        {
            'name': 'Samsung Galaxy S24 Ultra',
            'slug': 'samsung-galaxy-s24-ultra',
            'description': 'Флагманский смартфон Samsung с S Pen и камерой 200 МП',
            'price': 89990.00,
            'category': categories[0]
        },
        {
            'name': 'MacBook Pro 16" M3',
            'slug': 'macbook-pro-16-m3',
            'description': 'Мощный ноутбук для профессионалов с чипом M3',
            'price': 249990.00,
            'category': categories[1]
        },
        {
            'name': 'Dell XPS 15',
            'slug': 'dell-xps-15',
            'description': 'Премиальный ноутбук с безрамочным дисплеем',
            'price': 159990.00,
            'category': categories[1]
        },
        {
            'name': 'iPad Pro 12.9"',
            'slug': 'ipad-pro-12-9',
            'description': 'Профессиональный планшет с дисплеем Liquid Retina XDR',
            'price': 89990.00,
            'category': categories[2]
        },
        {
            'name': 'AirPods Pro 2',
            'slug': 'airpods-pro-2',
            'description': 'Беспроводные наушники с активным шумоподавлением',
            'price': 24990.00,
            'category': categories[3]
        },
        {
            'name': 'Sony WH-1000XM5',
            'slug': 'sony-wh-1000xm5',
            'description': 'Премиальные наушники с лучшим в мире шумоподавлением',
            'price': 39990.00,
            'category': categories[3]
        },
        {
            'name': 'Чехол для iPhone 15',
            'slug': 'case-iphone-15',
            'description': 'Защитный чехол из силикона для iPhone 15',
            'price': 2990.00,
            'category': categories[4]
        },
    ]
    
    products = []
    for prod_data in products_data:
        product, created = Product.objects.get_or_create(
            slug=prod_data['slug'],
            defaults={
                'name': prod_data['name'],
                'description': prod_data['description'],
                'price': prod_data['price'],
                'category': prod_data['category'],
                'available': True
            }
        )
        if created:
            print(f"Создан товар: {product.name}")
        products.append(product)
    
    # Создаем отзывы
    reviews_data = [
        {
            'product': products[0],  # iPhone 15 Pro
            'user': users[1],  # user1
            'rating': 5,
            'title': 'Отличный телефон!',
            'comment': 'Очень доволен покупкой. Камера просто потрясающая, а производительность на высоте.',
            'is_approved': True
        },
        {
            'product': products[0],  # iPhone 15 Pro
            'user': users[2],  # user2
            'rating': 4,
            'title': 'Хорошо, но дорого',
            'comment': 'Качество отличное, но цена кусается. В целом доволен.',
            'is_approved': True
        },
        {
            'product': products[1],  # Samsung Galaxy S24 Ultra
            'user': users[1],  # user1
            'rating': 5,
            'title': 'Лучший Android смартфон',
            'comment': 'S Pen очень удобен для заметок. Камера с 200 МП делает невероятные снимки.',
            'is_approved': True
        },
        {
            'product': products[2],  # MacBook Pro 16"
            'user': users[2],  # user2
            'rating': 5,
            'title': 'Мощная машина',
            'comment': 'Идеально подходит для работы с видео и графикой. Батарея держит весь день.',
            'is_approved': True
        },
        {
            'product': products[3],  # Dell XPS 15
            'user': users[3],  # user3
            'rating': 4,
            'title': 'Красивый дизайн',
            'comment': 'Очень стильный ноутбук. Дисплей безрамочный, смотрится круто.',
            'is_approved': True
        },
        {
            'product': products[4],  # iPad Pro
            'user': users[1],  # user1
            'rating': 5,
            'title': 'Лучший планшет',
            'comment': 'Идеально подходит для рисования и работы с документами.',
            'is_approved': True
        },
        {
            'product': products[5],  # AirPods Pro 2
            'user': users[2],  # user2
            'rating': 4,
            'title': 'Хорошие наушники',
            'comment': 'Шумоподавление работает отлично. Звук чистый и четкий.',
            'is_approved': True
        },
        {
            'product': products[6],  # Sony WH-1000XM5
            'user': users[3],  # user3
            'rating': 5,
            'title': 'Топовые наушники',
            'comment': 'Лучшее шумоподавление из всех, что пробовал. Очень комфортные.',
            'is_approved': True
        },
        {
            'product': products[0],  # iPhone 15 Pro
            'user': users[3],  # user3
            'rating': 3,
            'title': 'Нормально',
            'comment': 'Хороший телефон, но ожидал большего за такую цену.',
            'is_approved': False  # Не одобрен для демонстрации модерации
        },
    ]
    
    for review_data in reviews_data:
        review, created = Review.objects.get_or_create(
            product=review_data['product'],
            user=review_data['user'],
            defaults={
                'rating': review_data['rating'],
                'title': review_data['title'],
                'comment': review_data['comment'],
                'is_approved': review_data['is_approved'],
                'created': timezone.now()
            }
        )
        if created:
            print(f"Создан отзыв: {review.title}")
    
    print("\n✅ Тестовые данные успешно созданы!")
    print(f"📊 Статистика:")
    print(f"   - Пользователей: {User.objects.count()}")
    print(f"   - Категорий: {Category.objects.count()}")
    print(f"   - Товаров: {Product.objects.count()}")
    print(f"   - Отзывов: {Review.objects.count()}")
    print(f"   - Одобренных отзывов: {Review.objects.filter(is_approved=True).count()}")
    print(f"\n🔑 Данные для входа:")
    print(f"   - Админ: admin / password123")
    print(f"   - Пользователь: user1 / password123")
    print(f"   - Забаненный: banned_user / password123")

if __name__ == '__main__':
    create_test_data()