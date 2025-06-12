import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from twilio.rest import Client
from django.conf import settings
from .models import Patient, Doctor

def generate_verification_code():
    """Generate a 6-digit verification code."""
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def send_verification_code(phone_number, code):
    """Send verification code via Twilio SMS."""
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f'Your verification code is: {code}',
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        return True
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return False

@login_required
def verify_phone(request):
    """Handle phone verification."""
    # Get the user's profile
    if Patient.objects.filter(user=request.user).exists():
        profile = Patient.objects.get(user=request.user)
    else:
        profile = Doctor.objects.get(user=request.user)
    
    if not profile.phone_number:
        messages.error(request, 'No phone number found. Please update your profile first.')
        return redirect('profilemenu')
    
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        stored_code = cache.get(f'phone_verification_{request.user.id}')
        
        if not stored_code:
            messages.error(request, 'Verification code has expired. Please request a new one.')
            return redirect('verify_phone')
        
        if verification_code == stored_code:
            # Update the user's profile
            profile.phone_number_verified = True
            profile.save()
            
            # Clear the verification code from cache
            cache.delete(f'phone_verification_{request.user.id}')
            
            messages.success(request, 'Phone number verified successfully!')
            return redirect('profilemenu')
        else:
            messages.error(request, 'Invalid verification code. Please try again.')
    else:
        # If it's a GET request and no code is stored, send a new code
        if not cache.get(f'phone_verification_{request.user.id}'):
            code = generate_verification_code()
            cache.set(f'phone_verification_{request.user.id}', code, 600)  # Store for 10 minutes
            
            if send_verification_code(profile.phone_number, code):
                messages.success(request, 'Verification code has been sent to your phone number.')
            else:
                messages.error(request, 'Failed to send verification code. Please try again later.')

    return render(request, 'Accounts/phone_verification.html')

@login_required
def resend_phone_code(request):
    """Resend phone verification code."""
    if request.method == 'POST':
        # Get the user's profile
        if Patient.objects.filter(user=request.user).exists():
            profile = Patient.objects.get(user=request.user)
        else:
            profile = Doctor.objects.get(user=request.user)
        
        if not profile.phone_number:
            messages.error(request, 'No phone number found. Please update your profile first.')
            return redirect('profilemenu')
        
        # Generate new verification code
        code = generate_verification_code()
        
        # Store the code in cache for 10 minutes
        cache.set(f'phone_verification_{request.user.id}', code, 600)
        
        # Send the code via SMS
        if send_verification_code(profile.phone_number, code):
            messages.success(request, 'Verification code has been sent to your phone number.')
        else:
            messages.error(request, 'Failed to send verification code. Please try again later.')
        
        return redirect('verify_phone')
    
    return redirect('profilemenu') 