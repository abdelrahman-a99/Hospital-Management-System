from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from Accounts.models import Patient, Doctor
from django.contrib.auth.models import User, Group
from datetime import datetime, timedelta
from django.core import mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

User = get_user_model()


class SignupTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse("signup")
        # Create required groups
        Group.objects.create(name="Patients")
        Group.objects.create(name="Doctors")

    def test_valid_patient_signup(self):
        data = {
            "email": "test@example.com",
            "password": "Test@123",
            "confirm_password": "Test@123",
            "first_name": "John",
            "last_name": "Doe",
            "user_type": "patient",
            "gender": "Male",
            "phone_number": "+1234567890",
            "address": "123 Test St",
            "date_of_birth": (datetime.now() - timedelta(days=365 * 20)).strftime("%Y-%m-%d"),
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(User.objects.filter(email="test@example.com").exists())
        self.assertTrue(Patient.objects.filter(user__email="test@example.com").exists())

    def test_valid_doctor_signup(self):
        data = {
            "email": "doctor@example.com",
            "password": "Test@123",
            "confirm_password": "Test@123",
            "first_name": "Jane",
            "last_name": "Smith",
            "user_type": "doctor",
            "gender": "Female",
            "phone_number": "+1234567890",
            "address": "456 Test Ave",
            "date_of_birth": (datetime.now() - timedelta(days=365 * 30)).strftime("%Y-%m-%d"),
            "specialty": "Cardiology",
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email="doctor@example.com").exists())
        self.assertTrue(Doctor.objects.filter(user__email="doctor@example.com").exists())

    def test_invalid_first_name(self):
        data = {
            "email": "test@example.com",
            "password": "Test@123",
            "confirm_password": "Test@123",
            "first_name": "J",  # Too short
            "last_name": "Doe",
            "user_type": "patient",
            "gender": "Male",
            "phone_number": "+1234567890",
            "address": "123 Test St",
            "date_of_birth": (datetime.now() - timedelta(days=365 * 20)).strftime("%Y-%m-%d"),
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("First name should be between 3 and 50 characters", messages)

    def test_invalid_email(self):
        data = {
            "email": "invalid-email",
            "password": "Test@123",
            "confirm_password": "Test@123",
            "first_name": "John",
            "last_name": "Doe",
            "user_type": "patient",
            "gender": "Male",
            "phone_number": "+1234567890",
            "address": "123 Test St",
            "date_of_birth": (datetime.now() - timedelta(days=365 * 20)).strftime("%Y-%m-%d"),
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Invalid email format", messages)

    def test_duplicate_email(self):
        # Create a user first
        User.objects.create_user(
            username="existing", email="existing@example.com", password="Test@123"
        )

        data = {
            "email": "existing@example.com",
            "password": "Test@123",
            "confirm_password": "Test@123",
            "first_name": "John",
            "last_name": "Doe",
            "user_type": "patient",
            "gender": "Male",
            "phone_number": "+1234567890",
            "address": "123 Test St",
            "date_of_birth": (datetime.now() - timedelta(days=365 * 20)).strftime("%Y-%m-%d"),
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Email already exists", messages)

    def test_invalid_password(self):
        data = {
            "email": "test@example.com",
            "password": "weak",  # Too weak
            "confirm_password": "weak",
            "first_name": "John",
            "last_name": "Doe",
            "user_type": "patient",
            "gender": "Male",
            "phone_number": "+1234567890",
            "address": "123 Test St",
            "date_of_birth": (datetime.now() - timedelta(days=365 * 20)).strftime("%Y-%m-%d"),
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Password must be at least 8 characters long", messages)

    def test_underage_user(self):
        data = {
            "email": "test@example.com",
            "password": "Test@123",
            "confirm_password": "Test@123",
            "first_name": "John",
            "last_name": "Doe",
            "user_type": "patient",
            "gender": "Male",
            "phone_number": "+1234567890",
            "address": "123 Test St",
            "date_of_birth": (datetime.now() - timedelta(days=365 * 10)).strftime("%Y-%m-%d"),  # 10 years old
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("You must be at least 12 years old to register", messages)

    def test_password_mismatch(self):
        data = {
            "email": "test@example.com",
            "password": "Test@123",
            "confirm_password": "Different@123",  # Different password
            "first_name": "John",
            "last_name": "Doe",
            "user_type": "patient",
            "gender": "Male",
            "phone_number": "+1234567890",
            "address": "123 Test St",
            "date_of_birth": (datetime.now() - timedelta(days=365 * 20)).strftime("%Y-%m-%d"),
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Passwords do not match", messages)

    def test_login_validation(self):
        # First create a test user
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="Test@123",
            first_name="John",
            last_name="Doe",
        )
        Patient.objects.create(
            user=user,
            gender="Male",
            phone_number="+1234567890",
            address="123 Test St",
            dob=datetime.now().date() - timedelta(days=365 * 20),
        )
        user.groups.add(Group.objects.get(name="Patients"))

        # Test valid login
        login_data = {"email": "test@example.com", "password": "Test@123"}
        response = self.client.post(reverse("login"), login_data)
        self.assertEqual(response.status_code, 302)  # Redirect on success

        # Test invalid password
        login_data["password"] = "WrongPassword"
        response = self.client.post(reverse("login"), login_data)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Invalid email or password. Please try again.", messages)

        # Test non-existent email
        login_data = {"email": "nonexistent@example.com", "password": "Test@123"}
        response = self.client.post(reverse("login"), login_data)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Invalid email or password. Please try again.", messages)


class LoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse("login")
        # Create required groups
        Group.objects.create(name="Patients")
        Group.objects.create(name="Doctors")

        # Create a test patient user
        self.patient_user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="Test@123",
            first_name="John",
            last_name="Doe",
        )
        Patient.objects.create(
            user=self.patient_user,
            gender="Male",
            phone_number="+1234567890",
            address="123 Test St",
            dob=datetime.now().date() - timedelta(days=365 * 20),
        )
        self.patient_user.groups.add(Group.objects.get(name="Patients"))

        # Create a test doctor user
        self.doctor_user = User.objects.create_user(
            username="testdoctor",
            email="doctor@example.com",
            password="Test@123",
            first_name="Jane",
            last_name="Smith",
        )
        Doctor.objects.create(
            user=self.doctor_user,
            gender="Female",
            phone_number="+1234567890",
            address="456 Test Ave",
            dob=datetime.now().date() - timedelta(days=365 * 30),
            specialty="Cardiology",
        )
        self.doctor_user.groups.add(Group.objects.get(name="Doctors"))

    def test_valid_login(self):
        login_data = {"email": "test@example.com", "password": "Test@123"}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 302)  # Redirect on success

    def test_invalid_password(self):
        login_data = {"email": "test@example.com", "password": "WrongPassword"}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Invalid email or password. Please try again.", messages)

    def test_nonexistent_email(self):
        login_data = {"email": "nonexistent@example.com", "password": "Test@123"}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Invalid email or password. Please try again.", messages)

    def test_logout(self):
        # First login
        self.client.login(email="test@example.com", password="Test@123")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)  # Redirect on success
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("You have been logged out successfully.", messages)

    def test_invalid_access_doctor_page(self):
        # Try to access doctor page as a patient
        self.client.login(email="test@example.com", password="Test@123")
        response = self.client.get(reverse("doctor_page"))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_invalid_access_patient_page(self):
        # Try to access patient page as a doctor
        self.client.login(email="doctor@example.com", password="Test@123")
        response = self.client.get(reverse("patient_page"))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_remember_me_checked(self):
        login_data = {"email": "test@example.com", "password": "Test@123", "remember": "on"}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 302)
        session = self.client.session
        # Should NOT expire at browser close
        self.assertFalse(session.get_expire_at_browser_close())
        # Should be about 2 weeks (1209600 seconds)
        self.assertGreaterEqual(session.get_expiry_age(), 1209600 - 10)
        self.assertLessEqual(session.get_expiry_age(), 1209600 + 10)

    def test_remember_me_unchecked(self):
        login_data = {"email": "test@example.com", "password": "Test@123"}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 302)
        session = self.client.session
        # Should expire at browser close
        self.assertTrue(session.get_expire_at_browser_close())


class PasswordResetTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123!',
            first_name='Test',
            last_name='User'
        )
        self.patient = Patient.objects.create(
            user=self.user,
            gender='male',
            phone_number='+1234567890',
            address='123 Test St',
            dob='1990-01-01'
        )

    def test_password_reset_request_page_loads(self):
        """Test that password reset request page loads correctly"""
        response = self.client.get(reverse('password_reset_request'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reset Password')

    def test_password_reset_request_with_valid_email(self):
        """Test password reset request with valid email"""
        response = self.client.post(reverse('password_reset_request'), {
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Password Reset Request', mail.outbox[0].subject)

    def test_password_reset_request_with_invalid_email(self):
        """Test password reset request with invalid email"""
        response = self.client.post(reverse('password_reset_request'), {
            'email': 'nonexistent@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    def test_password_reset_confirm_with_valid_token(self):
        """Test password reset confirmation with valid token"""
        # Generate token
        token = default_token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))

        # Test GET request
        response = self.client.get(reverse('password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        }))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Set New Password')

    def test_password_reset_confirm_with_invalid_token(self):
        """Test password reset confirmation with invalid token"""
        response = self.client.get(reverse('password_reset_confirm', kwargs={
            'uidb64': 'invalid',
            'token': 'invalid'
        }))
        self.assertEqual(response.status_code, 302)  # Redirects to password_reset_request

    def test_password_reset_confirm_post_with_valid_data(self):
        """Test password reset confirmation POST with valid data"""
        token = default_token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))

        response = self.client.post(reverse('password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        }), {
            'password1': 'newpass123!',
            'password2': 'newpass123!'
        })
        self.assertEqual(response.status_code, 302)  # Redirects to login

        # Verify password was changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass123!'))

    def test_password_reset_confirm_post_with_mismatched_passwords(self):
        """Test password reset confirmation POST with mismatched passwords"""
        token = default_token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))

        response = self.client.post(reverse('password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        }), {
            'password1': 'newpass123!',
            'password2': 'differentpass123!'
        })
        self.assertEqual(response.status_code, 200)  # Stays on same page
        self.assertContains(response, 'Passwords do not match')

    def test_password_reset_confirm_post_with_weak_password(self):
        """Test password reset confirmation POST with weak password"""
        token = default_token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))

        response = self.client.post(reverse('password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        }), {
            'password1': 'weak',
            'password2': 'weak'
        })
        self.assertEqual(response.status_code, 200)  # Stays on same page
        self.assertContains(response, 'Password must be at least 8 characters long')

    def test_password_reset_done_page(self):
        """Test password reset done page"""
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Password Reset Complete')