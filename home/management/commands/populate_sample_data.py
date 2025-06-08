from django.core.management.base import BaseCommand
from home.models import About


class Command(BaseCommand):
    help = 'Populates the database with sample data for the home app'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        # Create About sections
        about_data = [
            {
                'icon': 'fas fa-hospital',
                'title': 'Modern Healthcare',
                'description': 'State-of-the-art facilities and cutting-edge medical technology to provide the best care for our patients.'
            },
            {
                'icon': 'fas fa-user-md',
                'title': 'Expert Doctors',
                'description': 'Our team consists of highly qualified and experienced medical professionals dedicated to your health.'
            },
            {
                'icon': 'fas fa-heart',
                'title': 'Patient Care',
                'description': 'We prioritize patient comfort and well-being, ensuring a supportive and caring environment throughout your treatment.'
            },
            {
                'icon': 'fas fa-clock',
                'title': '24/7 Service',
                'description': 'Round-the-clock medical services and emergency care to ensure you receive attention whenever you need it.'
            }
        ]

        for about_item in about_data:
            about = About.objects.create(
                icon=about_item['icon'],
                title=about_item['title'],
                description=about_item['description']
            )
            self.stdout.write(f'Created about section: {about.title}')

        self.stdout.write(self.style.SUCCESS('Successfully created sample data')) 