from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("departments/", views.departments, name="departments"),
    path("departments/<int:department_id>/", views.department_detail, name="department_detail"),
    path("services/", views.services, name="services"),
    path("services/<int:service_id>/", views.service_detail, name="service_detail"),
    path("testimonials/", views.testimonials, name="testimonials"),
    path("news/", views.news, name="news"),
    path("news/<int:news_id>/", views.news_detail, name="news_detail"),
    path("contact/", views.contact, name="contact"),
]
