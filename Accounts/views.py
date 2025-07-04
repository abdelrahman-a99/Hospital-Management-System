from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout as auth_logout, get_user_model)
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings
from .models import Patient, Doctor
from datetime import datetime
import re
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse

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
        user.is_active = True  # Set to True as allauth will handle activation
        user.save()

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

        # Use allauth's complete_signup to handle email verification
        complete_signup(
            request,
            user,
            allauth_settings.EMAIL_VERIFICATION,
            None,  # success_url
        )

        messages.success(request, 'Registration successful! Please check your email to verify your account.')
        return redirect('account_email_verification_sent')

    return render(request, 'Accounts/signup.html')


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        remember = request.POST.get("remember")

        # Authenticate using email and password
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Set the backend before logging in
            user.backend = 'Accounts.backends.EmailBackend'
            login(request, user)

            # Remember Me logic
            if remember:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)  # Session expires on browser close

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


def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if not email:
            messages.error(request, 'Please enter your email address.')
            return render(request, 'Accounts/password_reset_request.html')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Don't reveal if email exists or not for security
            messages.success(request, 'If an account with that email exists, you will receive password reset instructions.')
            return render(request, 'Accounts/password_reset_request.html')

        # Generate password reset token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Create reset URL
        reset_url = request.build_absolute_uri(
            reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        )

        # Send email
        subject = 'Password Reset Request - Nile\'s Care'
        message = render_to_string('Accounts/email/password_reset_email.html', {
            'user': user,
            'reset_url': reset_url,
            'site_name': settings.SITE_NAME,
        })

        try:
            email_message = EmailMultiAlternatives(
                subject=subject,
                body="Please use an HTML compatible email viewer.",  # fallback text
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
            )
            email_message.attach_alternative(message, "text/html")
            email_message.send()
            messages.success(request, 'Password reset instructions have been sent to your email.')
        except Exception as e:
            messages.error(request, 'Failed to send password reset email. Please try again later.')

        return render(request, 'Accounts/password_reset_request.html')

    return render(request, 'Accounts/password_reset_request.html')


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            # Validate password
            if not password1:
                messages.error(request, 'Password is required.')
                return render(request, 'Accounts/password_reset_confirm.html')

            if len(password1) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
                return render(request, 'Accounts/password_reset_confirm.html')

            if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password1):
                messages.error(request, 'Password must contain at least one letter, one number, and one special character.')
                return render(request, 'Accounts/password_reset_confirm.html')

            if password1 != password2:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'Accounts/password_reset_confirm.html')

            # Set new password
            user.set_password(password1)
            user.save()

            messages.success(request, 'Your password has been reset successfully. You can now login with your new password.')
            return redirect('login')

        return render(request, 'Accounts/password_reset_confirm.html')
    else:
        messages.error(request, 'The password reset link is invalid or has expired.')
        return redirect('password_reset_request')


def password_reset_done(request):
    """Show password reset done page"""
    return render(request, 'Accounts/password_reset_done.html')
