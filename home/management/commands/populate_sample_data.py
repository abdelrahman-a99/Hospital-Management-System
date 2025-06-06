from django.core.management.base import BaseCommand
from home.models import Department, Service, Testimonial, News


class Command(BaseCommand):
    help = 'Populates the database with sample data for the home app'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')
        
        # Create Departments
        departments_data = [
            {
                'name': 'Cardiology',
                'description': 'Specialized in heart and cardiovascular system treatment.',
                'icon': 'fa-heartbeat',
            },
            {
                'name': 'Neurology',
                'description': 'Expert care for brain and nervous system disorders.',
                'icon': 'fa-brain',
            },
            {
                'name': 'Pediatrics',
                'description': 'Comprehensive care for children from birth to adolescence.',
                'icon': 'fa-baby',
            },
            {
                'name': 'Orthopedics',
                'description': 'Specialized in musculoskeletal system and sports injuries.',
                'icon': 'fa-bone',
            },
            {
                'name': 'Dermatology',
                'description': 'Expert care for skin, hair, and nail conditions.',
                'icon': 'fa-allergies',
            },
        ]

        departments = []
        for dept_data in departments_data:
            dept = Department.objects.create(
                name=dept_data['name'],
                description=dept_data['description'],
                icon=dept_data['icon'],
                is_active=True
            )
            departments.append(dept)
            self.stdout.write(f'Created department: {dept.name}')

        # Create Services for each Department
        services_data = {
            'Cardiology': [
                {'name': 'Heart Check-up', 'price': 150.00, 'duration': '1 hour'},
                {'name': 'ECG Test', 'price': 75.00, 'duration': '30 minutes'},
                {'name': 'Stress Test', 'price': 200.00, 'duration': '1.5 hours'},
            ],
            'Neurology': [
                {'name': 'Brain MRI', 'price': 500.00, 'duration': '45 minutes'},
                {'name': 'Neurological Consultation', 'price': 180.00, 'duration': '1 hour'},
                {'name': 'Sleep Study', 'price': 350.00, 'duration': '8 hours'},
            ],
            'Pediatrics': [
                {'name': 'Child Wellness Check', 'price': 100.00, 'duration': '45 minutes'},
                {'name': 'Vaccination', 'price': 50.00, 'duration': '30 minutes'},
                {'name': 'Growth Monitoring', 'price': 80.00, 'duration': '1 hour'},
            ],
            'Orthopedics': [
                {'name': 'Joint Pain Consultation', 'price': 120.00, 'duration': '1 hour'},
                {'name': 'Sports Injury Treatment', 'price': 200.00, 'duration': '1.5 hours'},
                {'name': 'Physical Therapy', 'price': 90.00, 'duration': '1 hour'},
            ],
            'Dermatology': [
                {'name': 'Skin Consultation', 'price': 100.00, 'duration': '45 minutes'},
                {'name': 'Acne Treatment', 'price': 150.00, 'duration': '1 hour'},
                {'name': 'Skin Allergy Test', 'price': 200.00, 'duration': '1.5 hours'},
            ],
        }

        for dept in departments:
            for service_data in services_data[dept.name]:
                service = Service.objects.create(
                    name=service_data['name'],
                    department=dept,
                    description=f'Professional {service_data["name"].lower()} service in our {dept.name} department.',
                    icon='fa-stethoscope',
                    price=service_data['price'],
                    duration=service_data['duration'],
                    is_active=True
                )
                self.stdout.write(f'Created service: {service.name} for {dept.name}')

        # Create Testimonials
        testimonials_data = [
            {
                'name': 'John Smith',
                'role': 'Patient',
                'content': 'The cardiology department provided excellent care during my heart surgery. The staff was professional and caring.',
                'rating': 5,
            },
            {
                'name': 'Sarah Johnson',
                'role': 'Patient',
                'content': 'The pediatric team was amazing with my child. They made the hospital stay comfortable and stress-free.',
                'rating': 5,
            },
            {
                'name': 'Michael Brown',
                'role': 'Family Member',
                'content': 'The neurology department\'s expertise and care helped my father recover from his stroke. We\'re grateful for their support.',
                'rating': 4,
            },
            {
                'name': 'Emily Davis',
                'role': 'Patient',
                'content': 'The dermatology team helped me overcome my skin condition. Their treatment was effective and the follow-up care was excellent.',
                'rating': 5,
            },
            {
                'name': 'Robert Wilson',
                'role': 'Patient',
                'content': 'The orthopedic team helped me recover from my sports injury. Their rehabilitation program was well-structured and effective.',
                'rating': 4,
            },
        ]

        for testimonial_data in testimonials_data:
            testimonial = Testimonial.objects.create(
                name=testimonial_data['name'],
                role=testimonial_data['role'],
                content=testimonial_data['content'],
                rating=testimonial_data['rating'],
                is_active=True
            )
            self.stdout.write(f'Created testimonial from: {testimonial.name}')

        # Create News
        news_data = [
            {
                'title': 'New Cardiology Wing Opening',
                'content': 'We are excited to announce the opening of our new state-of-the-art cardiology wing, equipped with the latest technology.',
                'author': 'Dr. James Wilson',
                'is_featured': True,
            },
            {
                'title': 'COVID-19 Safety Measures Update',
                'content': 'Our hospital continues to maintain strict COVID-19 safety protocols to ensure the safety of our patients and staff.',
                'author': 'Hospital Administration',
                'is_featured': True,
            },
            {
                'title': 'New Pediatric Specialist Joins Our Team',
                'content': 'We welcome Dr. Sarah Thompson, a renowned pediatric specialist, to our team. She brings 15 years of experience.',
                'author': 'HR Department',
                'is_featured': False,
            },
            {
                'title': 'Hospital Receives Excellence Award',
                'content': 'Our hospital has been recognized for excellence in patient care and medical innovation.',
                'author': 'Public Relations',
                'is_featured': True,
            },
            {
                'title': 'New Medical Technology Implementation',
                'content': 'We have implemented new medical technology to improve patient care and treatment outcomes.',
                'author': 'Technical Department',
                'is_featured': False,
            },
        ]

        for news_data in news_data:
            news = News.objects.create(
                title=news_data['title'],
                content=news_data['content'],
                author=news_data['author'],
                is_active=True,
                is_featured=news_data['is_featured']
            )
            self.stdout.write(f'Created news: {news.title}')

        self.stdout.write(self.style.SUCCESS('Successfully created sample data')) 