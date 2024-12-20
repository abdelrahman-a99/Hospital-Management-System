import json
from django.shortcuts import render, get_object_or_404, redirect
from .models import Appointment, Message
from .forms import AppointmentForm
from Accounts.models import Doctor, Patient
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User

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
    return render(request, 'appointments/doctor_list.html', {'doctors': doctors})


@csrf_exempt
def patient_reservation(request):
    specialty = request.GET.get('specialty')
    doctors = Doctor.objects.filter(specialty=specialty) if specialty else Doctor.objects.all()

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            doctor_id = data.get('doctorId')
            date = data.get('date')
            time = data.get('time')

            if doctor_id and date and time:
                doctor = Doctor.objects.get(id=doctor_id)
                patient = Patient.objects.get(user=request.user)
                appointment = Appointment.objects.create(
                    doctor=doctor,
                    patient=patient,
                    date=date,
                    time=time,
                    status="Pending"
                )

                
                Message.objects.create(
                    sender=request.user, 
                    receiver=doctor.user,  
                    content=f"New appointment request from {patient.user.username} for {date} at {time}.",
                    appointment=appointment  
                )

                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Missing fields'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return render(request, 'appointments/patient_reservation.html', {
        'doctors': doctors,
        'selected_specialty': specialty,
    })

def upcoming_appointments(request):
    patient = Patient.objects.get(user=request.user)  
    appointments = Appointment.objects.filter(patient=patient).order_by('date', 'time')
    return render(request, 'appointments/upcoming_appointments.html', {
        'appointments': appointments
    })

def specialty_page(request):
    specialties = Doctor.objects.values_list('specialty', flat=True).distinct()
    return render(request, 'appointments/specialty_page.html', {'specialties': specialties})

@csrf_exempt
def messages_view(request):
    user = request.user

    if request.method == 'POST':
        data = json.loads(request.body)
        content = data.get('content')
        receiver_id = data.get('receiver_id')

        if content and receiver_id:
            receiver = User.objects.get(id=receiver_id)
            Message.objects.create(sender=user, receiver=receiver, content=content)
            return JsonResponse({'success': True, 'message': 'Message sent successfully.'})

        return JsonResponse({'success': False, 'error': 'Missing fields.'}, status=400)

    messages = Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)
    messages = messages.order_by('timestamp')
    return render(request, 'appointments/messages.html', {'messages': messages, 'user': user})