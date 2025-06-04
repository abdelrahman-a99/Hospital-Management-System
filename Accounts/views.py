from datetime import datetime
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Patient, Doctor
from django.contrib.auth import logout
import re

User = get_user_model()


# Helper function to render the signup form with current input data and error messages
def render_signup_form(request, error_message=None, **kwargs):
    if error_message:
        messages.error(request, error_message)

    return render(request, "Accounts/signup.html", kwargs)


def signup(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        phone_number = request.POST.get("phone_number")
        dob = request.POST.get("dob")
        user_type = request.POST.get("user_type")

        # Check if username already exists
        if User.objects.filter(username=uname).exists():
            messages.error(
                request, "Username already exists. Please choose a different username."
            )
            return render(
                request,
                "Accounts/signup.html",
                {
                    "username": "",
                    "email": email,
                    "gender": gender,
                    "address": address,
                    "phone_number": phone_number,
                    "dob": dob,
                    "user_type": user_type,
                },
            )

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(
                request, "This email is already registered. Please log in instead."
            )
            return redirect("login")

        # Validate date of birth and age
        if not dob:
            messages.error(request, "Date of birth is required.")
            return render(
                request,
                "Accounts/signup.html",
                {
                    "username": uname,
                    "email": email,
                    "gender": gender,
                    "address": address,
                    "phone_number": phone_number,
                    "dob": "",
                    "user_type": user_type,
                },
            )

        # Check if age is >= 12 (validate dob)
        try:
            dob_date = datetime.strptime(dob, "%Y-%m-%d")
            today = datetime.today()
            age = (
                today.year
                - dob_date.year
                - ((today.month, today.day) < (dob_date.month, dob_date.day))
            )

            if age < 12:
                messages.error(request, "You must be at least 12 years old to sign up.")
                return render(
                    request,
                    "Accounts/signup.html",
                    {
                        "username": uname,
                        "email": email,
                        "gender": gender,
                        "address": address,
                        "phone_number": phone_number,
                        "dob": "",
                        "user_type": user_type,
                    },
                )

        except ValueError:
            messages.error(request, "Invalid date of birth format. Please use YYYY-MM-DD.")
            return render(
                request,
                "Accounts/signup.html",
                {
                    "username": uname,
                    "email": email,
                    "gender": gender,
                    "address": address,
                    "phone_number": phone_number,
                    "dob": "",
                    "user_type": user_type,
                },
            )

        # Create user and save to database
        user = User.objects.create_user(username=uname, email=email, password=password)
        
        # Handle patient/doctor specific data
        if user_type == "patient":
            Patient.objects.create(
                user=user,
                gender=gender,
                address=address,
                phone_number=phone_number,
                dob=dob,
            )
        elif user_type == "doctor":
            specialty = request.POST.get("specialty")
            Doctor.objects.create(
                user=user,
                gender=gender,
                address=address,
                phone_number=phone_number,
                dob=dob,
                specialty=specialty,
            )

        messages.success(request, "Registration completed successfully! Please log in.")
        return redirect("login")

    return render(request, "Accounts/signup.html")


# def login(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         # Check if the user exists with the provided email
#         try:
#             user = CustomUser.objects.get(email=email)
#         except CustomUser.DoesNotExist:
#             messages.error(request, "Invalid email or password. Please try again.")
#             return redirect("login")

#         # Authenticate the user directly
#         # user = authenticate(request, username=email, password=password)
#         if user is not None:
#             # Successful authentication
#             auth_login(request, user)

#             if user.is_doctor:
#                 return redirect("doctor_page")

#             elif user.is_patient:
#                 return redirect("patient_page")

#             else:
#                 messages.error(request, "User type not recognized.")
#                 return redirect("login")

#         else:
#             # Authentication failed
#             messages.error(request, "Invalid email or password. Please try again.")
#             return redirect("login")
#     else:
#         return render(request, "Accounts/login.html")

# def login(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         try:
#             user = CustomUser.objects.get(email=email)
#         except CustomUser.DoesNotExist:
#             messages.error(request, "Invalid email or password.")
#             return redirect("login")

#         # Authenticate using username (linked to email)
#         user = authenticate(request, username=user.username, password=password)
#         if user:
#             auth_login(request, user)
#             return redirect("patient_page" if user.is_patient else "doctor_page")
#         else:
#             messages.error(request, "Invalid email or password.")
#             return redirect("login")
#     return render(request, "Accounts/login.html")

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # First try to find the user by email
        try:
            user = User.objects.get(email=email)
            # Then authenticate using the username and password
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                # Successful authentication
                auth_login(request, user)
                
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
        except User.DoesNotExist:
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
