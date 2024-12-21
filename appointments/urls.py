from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_list, name='doctor_list'),
    path('patient_reservation/', views.patient_reservation, name='patient_reservation'),
    path('specialty_page/', views.specialty_page, name='specialty_page'),
    path('upcoming_appointments/', views.upcoming_appointments, name='upcoming_appointments'),
    path('messages/', views.messages_view, name='messages'),
    path('doctor_messages/', views.doctor_messages, name='doctor_messages'),
]