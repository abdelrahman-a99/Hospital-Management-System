from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Appointment
from .forms import AppointmentForm
from .models import Doctor
from .models import Appointment, Doctor
from .forms import AppointmentForm

def patient_reservation(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_reservation')  # Redirect to the same page after saving
    else:
        form = AppointmentForm()

    doctors = Doctor.objects.all()  # Fetch all doctors for selection

    return render(request, 'appointments/patient_reservation.html', {'form': form, 'doctors': doctors})
def doctor_dashboard(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_dashboard')  
    else:
        form = AppointmentForm()

    appointments = Appointment.objects.all()  
    return render(request, 'appointments/doctor_dashboard.html', {'form': form, 'appointments': appointments})
def doctor_list(request):
    
    doctors = Doctor.objects.all()

    
    context = {
        'doctors': doctors
    }

    return render(request, 'appointments/doctor_list.html', context)