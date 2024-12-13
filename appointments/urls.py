from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_list, name='doctor_list'),
    path('reservation/', views.patient_reservation, name='patient_reservation'),
]
