from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Appointment
from .forms import AppointmentForm
from .models import Doctor
def doctor_dashboard(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_dashboard')  
    else:
        form = AppointmentForm()

    appointments = Appointment.objects.all()  
    return render(request, 'appointments/doctor_list.html', {'form': form, 'appointments': appointments})
def doctor_list(request):
    
    doctors = Doctor.objects.all()

    
    context = {
        'doctors': doctors
    }

    return render(request, 'appointments/doctor_list.html', context)