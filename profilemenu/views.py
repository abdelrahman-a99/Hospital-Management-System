from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Accounts.models import CustomUser, Patient, Doctor
from django.contrib.auth import get_user_model
from django.core.validators import validate_email

User = get_user_model()  # Get the custom user model

@login_required
def profilemenu(request):
    user = request.user

    if request.method == 'POST':
        # Get the form data
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirm_password')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        phone_number = request.POST.get('phonenumber')
        dob = request.POST.get('dob')
        user_type = request.POST.get('user_type')  # 'patient' or 'doctor'

        # Check if the username or email is changed and validate uniqueness
        if uname != user.username and User.objects.filter(username=uname).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect('profilemenu')

        if email != user.email and User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered. Please choose a different email.")
            return redirect('profilemenu')

        # Password validation (if password fields are provided)
        if pass1 or pass2:  # Only validate if passwords are provided
            if pass1 != pass2:
                messages.error(request, "Password and Confirm Password do not match.")
                return redirect('profilemenu')

            try:
                validate_password(pass1, user=user)  # Validate new password
                user.set_password(pass1)  # Set the new password
            except ValidationError as e:
                messages.error(request, f"Password error: {e.messages[0]}")
                return redirect('profilemenu')

        # Update User model (all fields except password and email)
        user.username = uname
        user.email = email
        user.save()

        # Update Patient or Doctor model based on user type
        if user.is_patient:
            patient = get_object_or_404(Patient, user=user)
            patient.gender = gender
            patient.address = address
            patient.phone_number = phone_number
            patient.dob = dob
            patient.save()
        elif user.is_doctor:
            specialty = request.POST.get('specialty')
            doctor = get_object_or_404(Doctor, user=user)
            doctor.gender = gender
            doctor.address = address
            doctor.phone_number = phone_number
            doctor.dob = dob
            doctor.specialty = specialty
            doctor.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profilemenu')  # Redirect to avoid form resubmission

    # Pre-fill form with existing user data for GET requests
    context = {
        'username': user.username,
        'email': user.email,    
        'gender': '',
        'address': '',
        'phone_number': '',
        'dob': '',
        'user_type': 'patient' if user.is_patient else 'doctor',
        'specialty': '',
    }

    # Fetch related data for Patient or Doctor models if available
    if user.is_patient:
        patient = get_object_or_404(Patient, user=user)
        context.update({
            'gender': patient.gender,
            'address': patient.address,
            'phone_number': patient.phone_number,
            'dob': patient.dob,
        })
    elif user.is_doctor:
        doctor = get_object_or_404(Doctor, user=user)
        context.update({
            'gender': doctor.gender,
            'address': doctor.address,
            'phone_number': doctor.phone_number,
            'dob': doctor.dob,
            'specialty': doctor.specialty,
        })

    return render(request, 'profilemenu/profilemenu-page.html', context)
