from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_list, name='doctor_list'),
    path('patient_reservation/', views.patient_reservation, name='patient_reservation'),
    path('specialty_page/', views.specialty_page, name='specialty_page'),
    path('patient_reservation/<str:specialty>/', views.patient_reservation, name='patient_reservation'),
]