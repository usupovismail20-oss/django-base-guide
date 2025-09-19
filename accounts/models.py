from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_banned = models.BooleanField(default=False, verbose_name='Забанен')
    ban_reason = models.TextField(blank=True, null=True, verbose_name='Причина бана')
    banned_at = models.DateTimeField(blank=True, null=True, verbose_name='Дата бана')
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.username
