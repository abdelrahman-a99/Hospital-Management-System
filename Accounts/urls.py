from django.urls import path
from . import views
from .phone_verification import verify_phone, resend_phone_code

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("doctor/", views.doctor_page, name="doctor_page"),
    path("patient/", views.patient_page, name="patient_page"),
    path("logout/", views.custom_logout, name="logout"),
    path('verify-phone/', verify_phone, name='verify_phone'),
    path('resend-phone-code/', resend_phone_code, name='resend_phone_code'),
]
