from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from Accounts.models import CustomUser
from Accounts.models import Patient,Doctor
# class CustomUser(AbstractUser):
#     is_doctor = models.BooleanField(default=False)
#     is_patient = models.BooleanField(default=False)
#     def __str__(self):
#         return self.username
#     groups = models.ManyToManyField(
#         Group,
#         related_name="accounts_customuser_groups",  # Unique related_name
#         blank=True
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name="accounts_customuser_permissions",  # Unique related_name
#         blank=True
#     )
# User = get_user_model()



# class Patient(models.Model):
#     user = models.OneToOneField(
#         CustomUser, 
#         on_delete=models.CASCADE, 
#         related_name="accounts_patient"  # Unique related_name
#     )
#     gender = models.CharField(max_length=10)
#     address = models.CharField(max_length=255)
#     phone_number = models.CharField(max_length=15)
#     dob = models.DateField()

#     def __str__(self):
#         return f"{self.user.username} - Patient"


# class Doctor(models.Model):
#     user = models.OneToOneField(
#         CustomUser, 
#         on_delete=models.CASCADE, 
#         related_name="accounts_doctor"  # Unique related_name
#     )
#     gender = models.CharField(max_length=10)
#     address = models.CharField(max_length=255)
#     phone_number = models.CharField(max_length=15)
#     dob = models.DateField()
#     specialty = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.user.username} - Doctor"
class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"
