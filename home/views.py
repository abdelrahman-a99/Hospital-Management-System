from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError

from django.shortcuts import render, redirect
from django.contrib import messages
import re  # Import the 're' module for regular expressions
from .models import ContactSubmission  # Import the model
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_protect

# Create your views here.

def index(request):
    return render(request, "home/index.html")

def contact(request):
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
                "home/index.html",
                {"name": name, "email": email, "message": message},
            )

        # Validate email with a stronger regex
        elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            messages.error(request, "Please enter a valid email address.")

            return render(
                request,
                "home/index.html",
                {"name": name, "email": email, "message": message},
            )

        # Validate message (at least 10 characters)
        elif len(message) < 10:
            messages.error(
                request,
                "Please enter a message with at least 10 characters.",
            )

            return render(
                request,
                "home/index.html",
                {"name": name, "email": email, "message": message},
            )

        else:
            # Optionally, save this data to the database or send an email
            # Save data to the database if valid
            
            # ContactSubmission.objects.create(name, email, message)
            ContactSubmission.objects.create(name=name, email=email, message=message)

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
                "index"
            )  # Redirect back in case of error without saving data

        # When there are errors, the form is re-rendered with the previous inputs
        # return render(
        #     request,
        #     "hospital_app/index.html",
        #     {"name": name, "email": email, "message": message},
        # )

    # Render index.html with any messages if validation fails
    return render(request, "home/index.html")


# @csrf_protect  # Ensure CSRF protection is enabled for this view
# def contact(request):
#     if request.method == "POST":
#         name = request.POST.get("name", "").strip()
#         email = request.POST.get("email", "").strip()
#         message = request.POST.get("message", "").strip()

#         if not name.isalpha() or len(name) < 3:
#             return JsonResponse({'success': False, 'message': 'Invalid name'})

#         elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
#             return JsonResponse({'success': False, 'message': 'Invalid email'})

#         elif len(message) < 10:
#             return JsonResponse({'success': False, 'message': 'Message too short'})

#         else:
#             ContactSubmission.objects.create(name=name, email=email, message=message)
#             return JsonResponse({'success': True, 'message': 'Thank you for your submission'})

#     return JsonResponse({'success': False, 'message': 'Invalid request'})
