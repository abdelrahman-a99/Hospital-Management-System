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