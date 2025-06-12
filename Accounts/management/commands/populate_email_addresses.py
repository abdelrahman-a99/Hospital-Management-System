from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates allauth EmailAddress objects for existing users.'

    def handle(self, *args, **options):
        users = User.objects.all()
        self.stdout.write(f'Found {users.count()} users.')
        count = 0
        for user in users:
            if user.email and not EmailAddress.objects.filter(user=user, email=user.email).exists():
                EmailAddress.objects.create(
                    user=user,
                    email=user.email,
                    primary=True,
                    verified=True
                )
                self.stdout.write(f'Successfully created EmailAddress for {user.email}')
                count += 1
            elif user.email:
                self.stdout.write(f'EmailAddress for {user.email} already exists.')
        self.stdout.write(self.style.SUCCESS(f'Successfully populated {count} email addresses.')) 