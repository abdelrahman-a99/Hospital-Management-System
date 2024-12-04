from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('doctor/', views.doctor_page, name='doctor_page'),  
    path('patient/', views.patient_page, name='patient_page'),  
]