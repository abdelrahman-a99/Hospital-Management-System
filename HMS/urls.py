from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("Accounts/", include("Accounts.urls")),
    path("doctor/", include("doctor.urls")),
    path("patient/", include("patient.urls")),
    path('appointments/', include('appointments.urls')),  # This should work if appointments.urls exists
]