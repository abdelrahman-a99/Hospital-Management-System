from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import re
from .models import ContactSubmission, Department, Service, Testimonial, News, About


def index(request):
    """Home page view with featured content"""
    departments = Department.objects.all()[:3]
    featured_news = News.objects.filter(is_featured=True)[:3]
    testimonials = Testimonial.objects.filter(is_featured=True)[:3]

    context = {
        'departments': departments,
        'featured_news': featured_news,
        'testimonials': testimonials,
    }
    return render(request, "home/index.html", context)

def about(request):
    """About page view"""
    abouts = About.objects.all()
    return render(request, "home/about.html", {'abouts': abouts})

def departments(request):
    """List all departments"""
    departments = Department.objects.all()
    return render(request, "home/departments.html", {'departments': departments})

def department_detail(request, department_id):
    """Show department details and its services"""
    department = get_object_or_404(Department, id=department_id)
    services = department.services.all()

    context = {
        'department': department,
        'services': services,
    }
    return render(request, "home/department_detail.html", context)

def services(request):
    """List all services"""
    services = Service.objects.all()
    return render(request, "home/services.html", {'services': services})

def service_detail(request, service_id):
    """Show service details"""
    service = get_object_or_404(Service, id=service_id)
    return render(request, "home/service_detail.html", {'service': service})

def testimonials(request):
    """List all testimonials"""
    testimonials = Testimonial.objects.all()
    return render(request, "home/testimonials.html", {'testimonials': testimonials})

def news(request):
    """List all news articles"""
    news_list = News.objects.all()
    return render(request, "home/news.html", {'news_list': news_list})

def news_detail(request, news_id):
    """Show news article details"""
    news_item = get_object_or_404(News, id=news_id)
    return render(request, "home/news_detail.html", {'news': news_item})

def contact(request):
    """Handle contact form submissions"""
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        # Validate name (at least 3 characters and only letters)
        if not name.isalpha() or len(name) < 3:
            messages.error(request, "Please enter a valid name.")
            return render(request, "home/contact.html", {
                "name": name,
                "email": email,
                "message": message
            })

        # Validate email with a stronger regex
        elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            messages.error(request, "Please enter a valid email address.")
            return render(request, "home/contact.html", {
                "name": name,
                "email": email,
                "message": message
            })

        # Validate message (at least 10 characters)
        elif len(message) < 10:
            messages.error(request, "Please enter a message with at least 10 characters.")
            return render(request, "home/contact.html", {
                "name": name,
                "email": email,
                "message": message
            })

        else:
            # Save to database
            ContactSubmission.objects.create(
                name=name,
                email=email,
                message=message
            )

            # Send email notification
            subject = f"New Contact Form Submission from {name}"
            message = f"Message from: {name}\n\n{message}"
            from_email = email
            recipient_list = ['boda142004ahmed@gmail.com']

            try:
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, "Thank you for reaching out! We'll get back to you soon.")
            except Exception as e:
                messages.error(request, f"Error sending email: {str(e)}")

            return redirect("index")

    return render(request, "home/contact.html")
