from django.db import models
from django.conf import settings  # Use settings.AUTH_USER_MODEL for the custom user model
from Accounts.models import Doctor, Patient
from django.contrib.auth import get_user_model
from django.utils.timezone import now
User = get_user_model()
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Appointment with {self.doctor.user.username} on {self.date} at {self.time}"
    
class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sent_messages',
        on_delete=models.CASCADE,
        null=True,  # Allow null in case of system-generated messages
        blank=True
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='received_messages',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Ensure a default value is provided
    appointment = models.ForeignKey(
        'Appointment',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Message from {self.sender.username if self.sender else 'System'} to {self.receiver.username}"
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.content}"