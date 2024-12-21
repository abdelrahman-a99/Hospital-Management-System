from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Accounts.models import CustomUser, Patient, Doctor
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import re

@login_required
def profilemenu(request):
    user = request.user
    User = get_user_model()  # Get the custom user model

    if request.method == 'POST':
        # Determine if the user is updating their password
        if 'password' in request.POST or 'confirm_password' in request.POST:
            pass1 = request.POST.get('password')
            pass2 = request.POST.get('confirm_password')

            if pass1 != pass2:
                messages.error(request, "Password and Confirm Password do not match.")
                return redirect('profilemenu')

            try:
                # Validate the new password
                validate_password(pass1, user=user)
                user.set_password(pass1)  # Set the new password
                user.save()

                # Log the user back in after password change
                from django.contrib.auth import update_session_auth_hash
                update_session_auth_hash(request, user)

                messages.success(request, "Password updated successfully!")
                return redirect('profilemenu')

            except ValidationError as e:
                messages.error(request, f"Password error: {e.messages[0]}")
                return redirect('profilemenu')

        # Update other profile fields
        uname = request.POST.get('username')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        phone_number = request.POST.get('phonenumber')
        dob = request.POST.get('dob')

        # Validate and update username
        if uname and uname != user.username:
            if User.objects.filter(username=uname).exists():
                messages.error(request, "Username already exists. Please choose a different username.")
                return redirect('profilemenu')
            user.username = uname

        # Validate and update email
        if email and email != user.email:
            if User.objects.filter(email=email).exists():
                messages.error(request, "This email is already registered. Please choose a different email.")
                return redirect('profilemenu')
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
            doctor.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profilemenu')

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


def contact2(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        # Validate name (at least 3 characters and only letters)
        if not name.isalpha() or len(name) < 3:
            messages.error(
                request, "Please enter a valid name."
            )

            return render(
                request,
                "profilemenu",
                {"name": "", "email": email, "message": message},
            )

        # Validate email with a stronger regex
        elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            messages.error(request, "Please enter a valid email address.")

            return render(
                request,
                "profilemenu",
                {"name": name, "email": "", "message": message},
            )

        # Validate message (at least 10 characters)
        elif len(message) < 10:
            messages.error(
                request,
                "Please enter a message with at least 10 characters.",
            )

            return render(
                request,
                "profilemenu/profilemenu-page.html",
                {"name": name, "email": email, "message": ""},
            )

        else:
            # Optionally, save this data to the database or send an email
            # Save data to the database if valid

            # ContactSubmission.objects.create(name, email, message)
            # ContactSubmission.objects.create(name=name, email=email, message=message)

            # If all validations pass, proceed with form processing
            print(f"Message received from {name} ({email}): {message}")

            # Send an email notification
            # subject = f"New contact form submission from {form.cleaned_data['name']}"
            # message = f"Message from: {form.cleaned_data['name']}\n\n{form.cleaned_data['message']}"
            # from_email = form.cleaned_data['email']
            # recipient_list = ['a.ahmed2299@nu.edu.eg']  # Replace with the recipient's email

            # Email notification details
            subject = f"New Contact Form Submission from {name}"
            # message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            message = f"Message from: {name}\n\n{message}"
            from_email = email  # Replace with your email
            recipient_list = ['boda142004ahmed@gmail.com']  # Replace with the recipient's email

            # send_mail(subject, message, from_email, recipient_list)

            try:
                # Send the email
                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                messages.error(request, f"Error sending email: {str(e)}")

            messages.success(
                request,
                "Thank you for reaching out! We'll get back to you soon.",
            )

            return redirect(
                "profilemenu"
            )  # Redirect back in case of error without saving data

        # When there are errors, the form is re-rendered with the previous inputs
        # return render(
        #     request,
        #     "hospital_app/index.html",
        #     {"name": name, "email": email, "message": message},
        # )

    # Render index.html with any messages if validation fails
    return render(request, "profilemenu/profilemenu-page.html")
