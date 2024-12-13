from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)

class Appointment(models.Model):
    patient_name = models.CharField(max_length=100)
    patient_email = models.EmailField()
    patient_contact = models.CharField(max_length=15)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, default='Scheduled')  # e.g., Scheduled, Cancelled
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.patient_name} with {self.doctor.name} on {self.date} at {self.time}"
