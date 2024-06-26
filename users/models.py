from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', **NULLABLE)
    token = models.CharField(max_length=10, verbose_name='Токен верификации', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email} - {self.phone}'

    class Meta:
        permissions = [
            ('view_all_users', 'Can view all users'),
            ('block_user', 'Can block users'),
        ]
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
