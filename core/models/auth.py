from django.apps import apps
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, login: str, password: str, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        user = self.model(login=login, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, login: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        return self._create_user(login, password, **extra_fields)

    def create_superuser(self, login: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_premium", True)
        return self._create_user(login, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    login = models.CharField('Логин', max_length=20, unique=True)
    balance = models.DecimalField('Баланс', max_digits=10, decimal_places=2, blank=True, default=0.00)
    is_premium = models.BooleanField('Премиум', default=False)
    premium_expiration_date = models.DateField(blank=True, null=True, default=None)

    objects = UserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['balance']  # дополнительные не уникальные поля запрашиваемые при авторизации суперпользователя

    class Meta:
        pass  # Сделать ограничение

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.login
