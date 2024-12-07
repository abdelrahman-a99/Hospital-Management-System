from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import CustomUser, Patient, Doctor
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
        # Retrieve the form data
        uname = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        pass2 = request.POST.get("confirm_password")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        phone_number = request.POST.get("phonenumber")
        dob = request.POST.get("dob")
        user_type = request.POST.get("user_type")  # 'patient' or 'doctor'
        specialty = request.POST.get("specialty")  # For doctor only

        print(
            f"Received data: {uname}, {email}, {password}, {pass2}, {gender}, {address}, {phone_number}, {dob}, {user_type}"
        )

        # Validate password matching
        if password != pass2:
            messages.error(
                request,
                "Your password and confirm password are not the same.",
                extra_tags="password-mismatch",
            )

            # return redirect('signup')

            return render(
                request,
                "Accounts/signup.html",
                {
                    "username": uname,
                    "email": email,
                    "gender": gender,
                    "address": address,
                    "phone_number": phone_number,
                    "dob": dob,
                    "user_type": user_type,
                },
            )

        # Validate password strength using Django's built-in validator
        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, f"Password error: {e.messages[0]}")

            # return redirect("signup")

            return render(
                request,
                "Accounts/signup.html",
                {
                    "username": uname,
                    "email": email,
                    "gender": gender,
                    "address": address,
                    "phone_number": phone_number,
                    "dob": dob,
                    "user_type": user_type,
                },
            )

        # Username validation (allow only letters and numbers)
        if not re.match("^[a-zA-Z0-9]+$", uname):
            messages.error(request, "Username can only contain letters and numbers.")

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

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address.")
            return render(
                request,
                "Accounts/signup.html",
                {
                    "username": uname,
                    "email": "",
                    "gender": gender,
                    "address": address,
                    "phone_number": phone_number,
                    "dob": dob,
                    "user_type": user_type,
                },
            )

        # Validate phone number using regex (for Egypt)
        # phone_regex = r"^\+20[1-9][0-9]{8}$|^\+20[2-9][0-9]{7}$"
        # phone_regex = r"^\+20(10|11|12|15)[0-9]{8}$"
        phone_regex = r"^(010|011|012|015)[0-9]{8}$"

        if not re.match(phone_regex, phone_number):
            messages.error(request, "Please enter a valid Egyptian phone number.")

            return render(
                request,
                "Accounts/signup.html",
                {
                    "username": uname,
                    "email": email,
                    "gender": gender,
                    "address": address,
                    "phone_number": "",
                    "dob": dob,
                    "user_type": user_type,
                },
            )

        # Check if username already exists
        # if User.objects.filter(username=uname).exists():
        #     user = User.objects.get(username=uname)
        #     if user.check_password(password):
        #         messages.error(
        #             request,
        #             "You are already registered. Please log in instead.",
        #             extra_tags="already-registered",
        #         )
        #         return redirect("login")

        # another way
        # if User.objects.filter(username=uname).exists():
        #     messages.error(
        #         request,
        #         "You are already registered. Please log in instead.",
        #         extra_tags="already-registered",
        #     )

        #     # Redirect to login page
        #     return redirect(
        #         "login"
        #     )  # Redirecting to the login page after informing the user

        # another logical way
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

            # return render(
            #     request,
            #     "Accounts/signup.html",
            #     {
            #         "username": uname,
            #         "email": email,
            #         "gender": gender,
            #         "address": address,
            #         "phone_number": phone_number,
            #         "dob": dob,
            #         "user_type": user_type,
            #     },
            # )

            return redirect(
                "login"
            )  # Redirecting to the login page after informing the user

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
            dob_date = datetime.strptime(
                dob, "%Y-%m-%d"
            )  # Parse DOB to a datetime object

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
            messages.error(
                request, "Invalid date of birth format. Please use YYYY-MM-DD."
            )

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
        user.is_patient = user_type == "patient"
        user.is_doctor = user_type == "doctor"
        user.save()

        # Handle patient/doctor specific data
        if user_type == "patient":
            Patient.objects.create(
                user=user,
                gender=gender,
                address=address,
                phone_number=phone_number,
                dob=dob,
            )
            return redirect("patient_page")  # Redirect directly to the patient page

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
            return redirect("doctor_page")  # Redirect directly to the doctor page

        messages.success(request, "Registration completed successfully! Please log in.")
        return redirect("login")

    return render(request, "Accounts/signup.html")


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if the user exists with the provided email
        # try:
        #     user = CustomUser.objects.get(email=email)
        # except CustomUser.DoesNotExist:
        #     messages.error(request, "Invalid email or password. Please try again.")
        #     return redirect("login")

        # Authenticate the user directly
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # Successful authentication
            auth_login(request, user)

            if user.is_doctor:
                return redirect("doctor_page")

            elif user.is_patient:
                return redirect("patient_page")

            else:
                messages.error(request, "User type not recognized.")
                return redirect("login")

        else:
            # Authentication failed
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect("login")
    else:
        return render(request, "Accounts/login.html")


@login_required
def doctor_page(request):
    # Ensure that the user is a doctor
    if not request.user.is_doctor:
        return HttpResponseForbidden("You are not authorized to view this page.")

    return render(request, "doctor/doctor_page.html", {"user": request.user})


@login_required
def patient_page(request):
    # Ensure that the user is a patient
    if not request.user.is_patient:
        return HttpResponseForbidden("You are not authorized to view this page.")

    return render(request, "patient/patient_page.html", {"user": request.user})


# Custom logout view
@login_required
def custom_logout(request):
    logout(request)  # Logs out the user and clears the session
    messages.success(request, "You have been logged out successfully.")

    # return redirect("login")  # Redirects the user to the login page after logging out

    return redirect("index")  # Redirect to home page after logging out
