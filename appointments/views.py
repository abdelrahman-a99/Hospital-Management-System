from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from .models import Appointment
from .forms import AppointmentForm
from Accounts.models import Doctor, Review
from django.http import JsonResponse
from datetime import datetime
from django.template.loader import get_template
from django.db.models import Avg

from appointments import models

def doctor_dashboard(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_dashboard')  # Redirect to the same page after saving
    else:
        form = AppointmentForm()

    appointments = Appointment.objects.all()  # Fetch all appointments to display
    return render(request, 'appointments/doctor_list.html', {'form': form, 'appointments': appointments})
def doctor_list(request):
    # Querying all doctors from the database
    doctors = Doctor.objects.all()

    # Passing the doctors data to the template
    context = {
        'doctors': doctors
    }

    return render(request, 'appointments/doctor_list.html', context)

def patient_reservation(request):
    specialties = Doctor.objects.values_list('specialty', flat=True).distinct()  # Get distinct specialties
    selected_specialty = request.GET.get('specialty', '')  # Get the selected specialty from the query parameters

    # Fetch doctors based on the selected specialty
    if selected_specialty:
        doctors = Doctor.objects.filter(specialty=selected_specialty).annotate(average_rating=Avg('reviews__rating')).order_by('user__username')
    else:
        doctors = Doctor.objects.all().annotate(average_rating=Avg('reviews__rating')).order_by('user__username')

    context = {
        'specialties': specialties,  # All specialties to be shown in a dropdown
        'doctors': doctors,  # Filtered list of doctors based on the selected specialty
        'selected_specialty': selected_specialty  # Current selected specialty
    }

    return render(request, 'appointments/patient_reservation.html', context)

def specialty_page(request):
    """
    Displays doctors by specialty.
    """
    specialties = Doctor.objects.values_list('specialty', flat=True).distinct()
    
    if request.method == "GET":
        # If a specialty is selected from the list, fetch doctors for that specialty
        selected_specialty = request.GET.get('specialty')
        doctors = Doctor.objects.filter(specialty=selected_specialty) if selected_specialty else []
        
        # Fetch reviews for each doctor
        for doctor in doctors:
            doctor.reviews = Review.objects.filter(doctor=doctor)
        
        return render(request, 'appointments/specialty_page.html', {
            'specialties': specialties,
            'doctors': doctors,
            'selected_specialty': selected_specialty
        })
    return render(request, 'appointments/specialty_page.html')