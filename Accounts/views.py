from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout as auth_logout, get_user_model)
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .models import Patient, Doctor
from datetime import datetime
import re

User = get_user_model()


# Helper function to render the signup form with current input data and error messages
def render_signup_form(request, error_message=None, **kwargs):
    if error_message:
        messages.error(request, error_message)

    return render(request, "Accounts/signup.html", kwargs)


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        user_type = request.POST.get('user_type')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        date_of_birth = request.POST.get('date_of_birth')
        specialty = request.POST.get('specialty')

        # Validate first name
        if not first_name:
            messages.error(request, 'First name is required')
            return render_signup_form(request, first_name=first_name, last_name=last_name, email=email)
        if not first_name.replace(' ', '').isalpha():
            messages.error(request, 'First name should contain only letters')
            return render_signup_form(request, first_name=first_name, last_name=last_name, email=email)
        if len(first_name) < 3 or len(first_name) > 50:
            messages.error(request, 'First name should be between 3 and 50 characters')
            return render_signup_form(request, first_name=first_name, last_name=last_name, email=email)

        # Validate last name
        if not last_name:
            messages.error(request, 'Last name is required')
            return render_signup_form(request, first_name=first_name, last_name=last_name, email=email)
        if not last_name.replace(' ', '').isalpha():
            messages.error(request, 'Last name should contain only letters')
            return render_signup_form(request, first_name=first_name, last_name=last_name, email=email)
        if len(last_name) < 3 or len(last_name) > 50:
            messages.error(request, 'Last name should be between 3 and 50 characters')
            return render_signup_form(request, first_name=first_name, last_name=last_name, email=email)

        # Validate email
        if not email:
            messages.error(request, 'Email is required')
            return render_signup_form(request, first_name=first_name, last_name=last_name)
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render_signup_form(request, first_name=first_name, last_name=last_name)
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messages.error(request, 'Invalid email format')
            return render_signup_form(request, first_name=first_name, last_name=last_name)

        # Validate password
        if not password:
            messages.error(request, 'Password is required')
            return render_signup_form(request, first_name=first_name, last_name=last_name, email=email)
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
            return render_signup_form(request, first_name=first_name, last_name=last_name, email=email)
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password):
            messages.error(request, 'Password must contain at least one letter, one number, and one special character')
            return render_signup_form(request, first_name=first_name, last_name=last_name, email=email)
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render_signup_form(request, first_name=first_name, last_name=last_name, email=email)

        # Validate user type
        if not user_type:
            messages.error(request, 'User type is required')
            return render_signup_form(request, first_name=first_name, last_name=last_name, email=email)
        if user_type not in ['patient', 'doctor']:
            messages.error(request, 'Invalid user type')
            return render_signup_form(request, first_name=first_name, last_name=last_name, email=email)

        # Validate gender
        if not gender:
            messages.error(request, 'Gender is required')
            return render_signup_form(request, first_name=first_name, last_name=last_name, email=email)
        if gender not in ['male', 'female']:
            messages.error(request, 'Invalid gender')
            return render_signup_form(request, first_name=first_name, last_name=last_name, email=email)

        # Validate phone number
        if not phone_number:
            messages.error(request, 'Phone number is required')
            return render_signup_form(request, first_name=first_name, last_name=last_name, email=email)
        if not re.match(r'^\+?1?\d{9,15}$', phone_number):
            messages.error(request, 'Invalid phone number format')
            return render_signup_form(request, first_name=first_name, last_name=last_name, email=email)

        # Validate address
        if not address:
            messages.error(request, 'Address is required')
            return render_signup_form(request, first_name=first_name, last_name=last_name, email=email)
        if len(address) < 3 or len(address) > 200:
            messages.error(request, 'Address should be between 3 and 200 characters')
            return render_signup_form(request, first_name=first_name, last_name=last_name, email=email)

        # Validate date of birth
        if not date_of_birth:
            messages.error(request, 'Date of birth is required')
            return render_signup_form(request, first_name=first_name, last_name=last_name, email=email)
        try:
            dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            age = (datetime.now().date() - dob).days / 365.25
            if age < 12:
                messages.error(request, 'You must be at least 12 years old to register')
                return render_signup_form(request, first_name=first_name, last_name=last_name, email=email)
        except ValueError:
            messages.error(request, 'Invalid date format')
            return render_signup_form(request, first_name=first_name, last_name=last_name, email=email)

        # Validate specialty for doctors
        if user_type == 'doctor' and not specialty:
            messages.error(request, 'Specialty is required for doctors')
            return render_signup_form(request, first_name=first_name, last_name=last_name, email=email)

        # Generate username from email
        username = email.split('@')[0]
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Create profile based on user type
        if user_type == 'patient':
            Patient.objects.create(
                user=user,
                gender=gender,
                phone_number=phone_number,
                address=address,
                dob=dob
            )
            user.groups.add(Group.objects.get(name='Patients'))
        else:
            Doctor.objects.create(
                user=user,
                gender=gender,
                phone_number=phone_number,
                address=address,
                dob=dob,
                specialty=specialty
            )
            user.groups.add(Group.objects.get(name='Doctors'))

        # Show success message and redirect to login
        messages.success(request, 'Registration successful! Please login to continue.')
        return redirect('login')

    return render(request, 'Accounts/signup.html')


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate using email and password
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Set the backend before logging in
            user.backend = 'Accounts.backends.EmailBackend'
            login(request, user)

            # Check if user is a doctor or patient
            try:
                doctor = Doctor.objects.get(user=user)
                return redirect("doctor_page")
            except Doctor.DoesNotExist:
                try:
                    patient = Patient.objects.get(user=user)
                    return redirect("patient_page")
                except Patient.DoesNotExist:
                    messages.error(request, "User type not recognized.")
                    return redirect("login")
        else:
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect("login")

    return render(request, "Accounts/login.html")

@login_required
def doctor_page(request):
    # Ensure that the user is a doctor
    try:
        doctor = Doctor.objects.get(user=request.user)
        return render(request, "doctor/doctor_page.html", {"user": request.user})
    except Doctor.DoesNotExist:
        return HttpResponseForbidden("You are not authorized to view this page.")


@login_required
def patient_page(request):
    # Ensure that the user is a patient
    try:
        patient = Patient.objects.get(user=request.user)
        return render(request, "patient/patient_page.html", {"user": request.user})
    except Patient.DoesNotExist:
        return HttpResponseForbidden("You are not authorized to view this page.")


# Custom logout view
@login_required
def custom_logout(request):
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("index")
