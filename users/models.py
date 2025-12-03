from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

#  1. Создаем менеджер (он учит Django работать без username)
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Создает и сохраняет пользователя с email и паролем."""
        if not email:
            raise ValueError('Email должен быть указан')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создает и сохраняет суперпользователя."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


#  2. Твоя модель пользователя
class User(AbstractUser):
    username = None  # Убираем поле username
    email = models.EmailField(unique=True, verbose_name='Email')

    phone = models.CharField(max_length=35, verbose_name='Телефон', blank=True, null=True)
    country = models.CharField(max_length=50, verbose_name='Страна', blank=True, null=True)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    #  3. Подключаем наш менеджер
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email