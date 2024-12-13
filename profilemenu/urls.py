from django.urls import path
from . import views

urlpatterns = [
    path('', views.profilemenu, name='profilemenu'),
    path("contact2/", views.contact2, name="contact2"),
]