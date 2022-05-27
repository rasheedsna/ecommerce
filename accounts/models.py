import uuid
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class Role(models.Model):
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.role


class UserManager(BaseUserManager):
    def _create_user(self, password, is_staff, is_superuser, **extra_fields):
        # if not phone:
        #     raise ValueError("phone is not valid")
        user = self.model(is_active=True, is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, password, **extra_fields):
        return self._create_user(password, is_staff=False, is_superuser=False, **extra_fields)

    def create_superuser(self, password, **extra_fields):
        return self._create_user(password, is_staff=True, is_superuser=True, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=250, unique=True, null=True, blank=True)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    phone = models.CharField(max_length=16, unique=True)
    image = models.ImageField(blank=True, null=True, upload_to='profile_images')
    updatedAt = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    joiningDate = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='users', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'

    def __str__(self):
        field_name = self.name
        if not field_name:
            field_name = self.phone

        return field_name

