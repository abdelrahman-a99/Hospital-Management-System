from django.test import TestCase
from django.urls import reverse
from .models import Department, Service, Testimonial, News, About, ContactSubmission

# Create your tests here.

class PublicViewsTestCase(TestCase):
    def setUp(self):
        # Create minimal objects for detail pages
        self.department = Department.objects.create(
            name="Cardiology",
            description="Heart care department",
            icon="fa-heart"
        )
        self.service = Service.objects.create(
            name="ECG",
            description="Electrocardiogram",
            department=self.department,
            icon="fa-wave-square"
        )
        self.testimonial = Testimonial.objects.create(
            name="John Doe",
            role="Patient",
            content="Great service!",
            rating=5
        )
        self.news = News.objects.create(
            title="New MRI Machine",
            content="We have a new MRI machine.",
            author="Admin"
        )
        self.about = About.objects.create(
            icon="fa-hospital",
            title="About Nile's Care",
            description="Best hospital in the region."
        )

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_departments_view(self):
        response = self.client.get(reverse('departments'))
        self.assertEqual(response.status_code, 200)

    def test_department_detail_view(self):
        response = self.client.get(reverse('department_detail', args=[self.department.id]))
        self.assertEqual(response.status_code, 200)

    def test_services_view(self):
        response = self.client.get(reverse('services'))
        self.assertEqual(response.status_code, 200)

    def test_service_detail_view(self):
        response = self.client.get(reverse('service_detail', args=[self.service.id]))
        self.assertEqual(response.status_code, 200)

    def test_testimonials_view(self):
        response = self.client.get(reverse('testimonials'))
        self.assertEqual(response.status_code, 200)

    def test_news_view(self):
        response = self.client.get(reverse('news'))
        self.assertEqual(response.status_code, 200)

    def test_news_detail_view(self):
        response = self.client.get(reverse('news_detail', args=[self.news.id]))
        self.assertEqual(response.status_code, 200)

    def test_contact_view_get(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_contact_view_post_invalid(self):
        # Invalid name (too short)
        response = self.client.post(reverse('contact'), {
            'name': 'A',
            'email': 'test@example.com',
            'message': 'Hello world! This is a test message.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a valid name.")

    def test_contact_view_post_valid(self):
        response = self.client.post(reverse('contact'), {
            'name': 'Alice',
            'email': 'alice@example.com',
            'message': 'Hello world! This is a test message.'
        })
        # Should redirect to index on success
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
