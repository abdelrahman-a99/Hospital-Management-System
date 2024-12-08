from django.urls import path
from . import views
# from .views import custom_logout

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('doctor/', views.doctor_page, name='doctor_page'),  
    path('patient/', views.patient_page, name='patient_page'),  
    # path('logout/', custom_logout, name='logout'),
    path('logout/', views.custom_logout, name='logout'),
]