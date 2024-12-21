from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from Accounts.models import Patient, Doctor

class ProfileMenuViewTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='sherif',
            email='testuser@example.com',
            password='testpassword'
        )
        self.client = Client()
        self.client.login(username='sherif', password='testpassword')
        self.profilemenu_url = reverse('profilemenu')  # Ensure the URL name matches your project setup

    def test_profilemenu_get(self):
        # Test GET request
        response = self.client.get(self.profilemenu_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profilemenu/profilemenu-page.html')
        self.assertContains(response, 'sherif')  # Check if username is displayed

    def test_profilemenu_update_username(self):
        # Test updating the username
        response = self.client.post(self.profilemenu_url, {
            'username': 'newusername'
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')
        self.assertRedirects(response, self.profilemenu_url)
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn('Profile updated successfully!', messages)

    def test_profilemenu_update_password(self):
        # Test updating the password
        response = self.client.post(self.profilemenu_url, {
            'password': 'newsecurepassword123',
            'confirm_password': 'newsecurepassword123'
        })
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newsecurepassword123'))
        self.assertRedirects(response, self.profilemenu_url)
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn('Password updated successfully!', messages)

    def test_profilemenu_delete_account(self):
        # Test deleting the account
        response = self.client.post(self.profilemenu_url, {
            'delete_account': 'true'
        })
        self.assertFalse(get_user_model().objects.filter(username='testuser').exists())
        self.assertRedirects(response, reverse('index'))
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn('Your account has been deleted successfully.', messages)