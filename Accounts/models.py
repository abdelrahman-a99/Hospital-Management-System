from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name="customuser_groups",  # Add unique related_name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="customuser_permissions",  # Add unique related_name
        blank=True,
    )

User = get_user_model()

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    dob = models.DateField()

    def __str__(self):
        return f"{self.user.username} - Patient"

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    dob = models.DateField()
    specialty = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - Doctor"