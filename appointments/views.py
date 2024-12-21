import json
from django.shortcuts import render, get_object_or_404, redirect
from .models import Appointment, Message,Notification
from .forms import AppointmentForm
from Accounts.models import Doctor, Patient
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
from .observers import Subject, NotificationObserver  

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

                # Send a message to the doctor
                Message.objects.create(
                    sender=request.user, 
                    receiver=doctor.user, 
                    content=f"A new appointment request from {patient.user.username} for {date} at {time}.",
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

    if not user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'User not authenticated.'}, status=401)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content = data.get('content')

            if not content:
                return JsonResponse({'success': False, 'error': 'Content cannot be empty.'})

            # Assuming doctor is the recipient for patient messages
            patient = Patient.objects.get(user=user)
            latest_appointment = patient.appointment_set.latest('date')
            doctor_user = latest_appointment.doctor.user

            # Create a new message
            Message.objects.create(sender=user, receiver=doctor_user, content=content)

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    elif request.method == 'GET':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Fetch messages for the logged-in user
            messages = Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)
            messages = messages.order_by('timestamp')

            # Fetch notifications for the logged-in user
            notifications = Notification.objects.filter(user=user).order_by('-created_at')

            # Structure the response
            return JsonResponse({
                'success': True,
                'messages': [
                    {
                        'sender': msg.sender.username,
                        'receiver': msg.receiver.username,
                        'content': msg.content,
                        'timestamp': msg.timestamp,
                    }
                    for msg in messages
                ],
                'notifications': [
                    {
                        'content': notification.content,
                        'timestamp': notification.created_at,
                        'is_read': notification.is_read,
                    }
                    for notification in notifications
                ],
            })

        # Render template for HTML requests
        messages = Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)
        messages = messages.order_by('timestamp')
        notifications = Notification.objects.filter(user=user).order_by('-created_at')
        return render(request, 'appointments/messages.html', {
            'messages': messages,
            'notifications': notifications,
            'user': user
        })

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

def doctor_messages(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect unauthenticated users to login
    
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        return render(request, 'appointments/error.html', {'error': 'Only doctors can access this page.'})

    # Fetch messages where the doctor is the receiver
    messages = Message.objects.filter(receiver=request.user).order_by('timestamp')
    
    return render(request, 'appointments/doctor_messages.html', {
        'messages': messages,
        'user': request.user,
    })
