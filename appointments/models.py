from django.db import models

class Appointment(models.Model):
    patient_name = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=50, default='Reserved')

    def __str__(self):
        return f'{self.patient_name} - {self.date} at {self.time}'
class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.specialty})"