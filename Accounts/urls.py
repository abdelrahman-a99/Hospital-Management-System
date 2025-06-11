from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("doctor/", views.doctor_page, name="doctor_page"),
    path("patient/", views.patient_page, name="patient_page"),
    path("logout/", views.custom_logout, name="logout"),
]
