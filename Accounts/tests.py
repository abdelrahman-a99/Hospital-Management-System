from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from Accounts.models import Patient, Doctor

User = get_user_model()

class UserTests(TestCase):
    
    def test_signup_valid_patient(self):
        
        # Test the signup process for a patient with valid data.
        data = {
            "username": "testpatient",
            "email": "testpatient@example.com",
            "password": "Testpassword123",
            "confirm_password": "Testpassword123",
            "gender": "Male",
            "address": "123 Street",
            "phonenumber": "01012345678",
            "dob": "2010-05-15",
            "user_type": "patient"
        }
        
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(User.objects.filter(username="testpatient").exists())
        self.assertTrue(Patient.objects.filter(user__username="testpatient").exists())
    
    def test_signup_valid_doctor(self):
        # Test the signup process for a doctor with valid data.# 
        data = {
            "username": "testdoctor",
            "email": "testdoctor@example.com",
            "password": "Testpassword123",
            "confirm_password": "Testpassword123",
            "gender": "Female",
            "address": "456 Avenue",
            "phonenumber": "01087654321",
            "dob": "1985-08-25",
            "user_type": "doctor",
            "specialty": "Cardiology"
        }

        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(User.objects.filter(username="testdoctor").exists())
        self.assertTrue(Doctor.objects.filter(user__username="testdoctor").exists())
    
    def test_signup_password_mismatch(self):
        # Test the signup process when passwords don't match.# 
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "Testpassword123",
            "confirm_password": "Differentpassword123",
            "gender": "Male",
            "address": "123 Street",
            "phonenumber": "01012345678",
            "dob": "2010-05-15",
            "user_type": "patient"
        }
        
        response = self.client.post(reverse('signup'), data)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Your password and confirm password are not the same.", messages)

    def test_signup_invalid_email(self):
        # Test the signup process when an invalid email is provided.# 
        data = {
            "username": "testuser",
            "email": "invalid-email",
            "password": "Testpassword123",
            "confirm_password": "Testpassword123",
            "gender": "Male",
            "address": "123 Street",
            "phonenumber": "01012345678",
            "dob": "2010-05-15",
            "user_type": "patient"
        }
        
        response = self.client.post(reverse('signup'), data)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Please enter a valid email address.", messages)
    
    def test_login_valid_user(self):
        
        # Test login functionality with valid credentials for a patient.# 
        user = User.objects.create_user(
            username="testpatient",
            email="testpatient@example.com",
            password="Testpassword123"
        )
        Patient.objects.create(user=user, gender="Male", address="123 Street", phone_number="01012345678", dob="2010-05-15")
        
        response = self.client.post(reverse('login'), {
            'email': "testpatient@example.com",
            'password': "Testpassword123"
        })
    
    def test_login_invalid_user(self):
        # Test login functionality with invalid credentials.#
        response = self.client.post(reverse('login'), {
            'email': "wrongemail@example.com",
            'password': "Wrongpassword123"
        })
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Email or Password is incorrect!!!", messages)
    
    def test_invalid_access_doctor_page(self):
        
        # Test invalid access to doctor page by a patient.# 
        patient_user = User.objects.create_user(
            username="testpatient",
            email="testpatient@example.com",
            password="Testpassword123"
        )
        Patient.objects.create(user=patient_user, gender="Male", address="123 Street", phone_number="01012345678", dob="2010-05-15")
        
        self.client.login(username="testpatient", password="Testpassword123")
        response = self.client.get(reverse('doctor_page'))
        self.assertEqual(response.status_code, 403)
    
    # def test_logout(self):

    #     # Test logout functionality.# 
    #     user = User.objects.create_user(
    #         username="testuser",
    #         email="testuser@example.com",
    #         password="Testpassword123"
    #     )
    #     self.client.login(username="testuser", password="Testpassword123")
        
    #     response = self.client.get(reverse('logout'))
    #     self.assertRedirects(response, reverse('index'))
