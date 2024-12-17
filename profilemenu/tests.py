from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages import get_messages
from Accounts.models import Patient, Doctor

class ProfileMenuTests(TestCase):

    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='testuser', password='password123'
        )
        self.client.login(username='testuser', password='password123')

    def test_profile_update_valid_data(self):
        # Simulate POST request to update profile
        response = self.client.post(reverse('profilemenu'), {
            'username': 'newusername',
            'email': 'newemail@example.com',
            'gender': 'Male',
            'address': '123 New Street',
            'phonenumber': '1234567890',
            'dob': '1990-01-01',
        })
        
        # Check if the user data is updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')
        self.assertEqual(self.user.email, 'newemail@example.com')

        # Check the success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Profile updated successfully!")
# Create your tests here.
