from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from Accounts.models import Doctor, Patient, Review

class Command(BaseCommand):
    help = 'Sets up initial groups and permissions for the hospital system'

    def handle(self, *args, **kwargs):
        # Create groups
        doctor_group, created = Group.objects.get_or_create(name='Doctors')
        patient_group, created = Group.objects.get_or_create(name='Patients')

        # Get content types
        doctor_ct = ContentType.objects.get_for_model(Doctor)
        patient_ct = ContentType.objects.get_for_model(Patient)
        review_ct = ContentType.objects.get_for_model(Review)

        # Doctor permissions
        doctor_permissions = [
            Permission.objects.get_or_create(
                codename='view_patient',
                name='Can view patient profiles',
                content_type=patient_ct,
            )[0],
            Permission.objects.get_or_create(
                codename='view_review',
                name='Can view reviews',
                content_type=review_ct,
            )[0],
        ]

        # Patient permissions
        patient_permissions = [
            Permission.objects.get_or_create(
                codename='view_doctor',
                name='Can view doctor profiles',
                content_type=doctor_ct,
            )[0],
            Permission.objects.get_or_create(
                codename='add_review',
                name='Can add reviews',
                content_type=review_ct,
            )[0],
        ]

        # Assign permissions to groups
        doctor_group.permissions.set(doctor_permissions)
        patient_group.permissions.set(patient_permissions)

        self.stdout.write(self.style.SUCCESS('Successfully set up groups and permissions')) 