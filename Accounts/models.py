from django.db import models
from django.contrib.auth.models import User, Group
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


class BaseProfile(models.Model):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, blank=True, null=True
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
            )
        ],
    )
    dob = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user.username} - {self.__class__.__name__}"


class Patient(BaseProfile):
    pass


class Doctor(BaseProfile):
    specialty = models.CharField(max_length=100, blank=True, null=True)


class Review(models.Model):
    doctor = models.ForeignKey(Doctor, related_name="reviews", on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.doctor.user.username} by {self.patient.user.username}"


# Signal to create/update groups when a new user is created
@receiver(post_save, sender=User)
def create_user_groups(sender, instance, created, **kwargs):
    if created:
        # Create groups if they don't exist
        doctor_group, _ = Group.objects.get_or_create(name="Doctors")
        patient_group, _ = Group.objects.get_or_create(name="Patients")

        # Check if user is a doctor or patient and add to appropriate group
        try:
            if Doctor.objects.filter(user=instance).exists():
                instance.groups.add(doctor_group)
            elif Patient.objects.filter(user=instance).exists():
                instance.groups.add(patient_group)
        except:
            pass  # Handle case where profile might not be created yet
