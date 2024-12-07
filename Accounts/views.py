from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import CustomUser, Patient, Doctor
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')  

User = get_user_model()

def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        pass2 = request.POST.get('confirm_password')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        phone_number = request.POST.get('phonenumber')
        dob = request.POST.get('dob')
        user_type = request.POST.get('user_type')  # 'patient' or 'doctor'

        print(f"Received data: {uname}, {email}, {password}, {pass2}, {gender}, {address}, {phone_number}, {dob}, {user_type}")

        if password != pass2:
            messages.error(request, "Your password and confirm password are not the same.", extra_tags='password-mismatch')
            return redirect('signup')

        # Validate password
        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, f"Password error: {e.messages[0]}")
            return redirect('signup')

        if User.objects.filter(username=uname).exists():
            user = User.objects.get(username=uname)
            if user.check_password(password):
                messages.error(request, "You are already registered. Please log in instead.", extra_tags='already-registered')
                return redirect('login')

        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered. Please log in instead.")
            return redirect('login')

        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect('signup')

        user = User.objects.create_user(username=uname, email=email, password=password)
        user.is_patient = (user_type == 'patient')
        user.is_doctor = (user_type == 'doctor')
        user.save()

        if user_type == 'patient':
            Patient.objects.create(user=user, gender=gender, address=address, phone_number=phone_number, dob=dob)
        elif user_type == 'doctor':
            specialty = request.POST.get('specialty')
            Doctor.objects.create(user=user, gender=gender, address=address, phone_number=phone_number, dob=dob, specialty=specialty)

        messages.success(request, "Registration completed successfully! Please log in.")
        return redirect('login')

    return render(request, 'Accounts/signup.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        users = CustomUser.objects.filter(email=email)

        if users.exists():
            for user in users:
                user = authenticate(request, username=user.username, password=password)
                if user:
                    auth_login(request, user)
                    if user.is_doctor:
                        return redirect('doctor_page')  

                    elif user.is_patient:
                        return redirect('patient_page')  

                    else:
                        messages.error(request, "User type not recognized.")
                        return redirect('login')

            messages.error(request, "Invalid email or password. Please try again.")
            return redirect('login')
        else:
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect('login')
    else:
        return render(request, 'Accounts/login.html')

@login_required
def doctor_page(request):
    # user = request.user
    # return render(request, 'doctor/doctor_page.html', {'user': user})
    if not request.user.is_doctor:
        return HttpResponseForbidden("You are not authorized to view this page.")
    return render(request, 'doctor/doctor_page.html', {'user': request.user})

@login_required
def patient_page(request):
    # user = request.user
    # return render(request, 'patient/patient_page.html', {'user': user})
    if not request.user.is_patient:
        return HttpResponseForbidden("You are not authorized to view this page.")
    return render(request, 'patient/patient_page.html', {'user': request.user})
