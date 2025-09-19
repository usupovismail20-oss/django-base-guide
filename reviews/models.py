from django.db import models
from django.contrib.auth import get_user_model
from main.models import Product

User = get_user_model()


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 звезда'),
        (2, '2 звезды'),
        (3, '3 звезды'),
        (4, '4 звезды'),
        (5, '5 звезд'),
    ]
    
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE, verbose_name='Товар')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name='Рейтинг')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    comment = models.TextField(verbose_name='Комментарий')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    is_approved = models.BooleanField(default=False, verbose_name='Одобрен')
    
    class Meta:
        ordering = ('-created',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('product', 'user')
    
    def __str__(self):
        return f'{self.user.username} - {self.product.name} ({self.rating} звезд)'
    
    def get_stars(self):
        return '★' * self.rating + '☆' * (5 - self.rating)