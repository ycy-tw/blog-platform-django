from re import T
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
import os
import secrets


class CustomAccountManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """

        user = self.create_user(
            email=email,
            password=password,
            username=secrets.token_urlsafe(12),
        )
        if not email:
            raise ValueError('Users must have an email address')

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{instance.username}.{ext}'
    return os.path.join('images/profile_img/', filename)


def random_username():
    return secrets.token_urlsafe(6)


class Account(AbstractBaseUser):

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        max_length=255,
        unique=True,
        primary_key=True,
        default=random_username
    )
    profile_img = models.ImageField(
        null=True,
        upload_to=content_file_name,
        default='default_user_img.jpg'
    )
    name = models.CharField(max_length=255, null=False)
    intro = models.CharField(max_length=255, default=_("Tell me more about you."))
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'{self.username}'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
