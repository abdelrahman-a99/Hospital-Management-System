from django.contrib import admin
from .models import Patient, Doctor
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(CustomUser, UserAdmin)