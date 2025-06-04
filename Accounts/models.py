from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Patient"

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    specialty = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Doctor"

class Review(models.Model):
    doctor = models.ForeignKey(Doctor, related_name='reviews', on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.doctor.user.username} by {self.patient.user.username}"
