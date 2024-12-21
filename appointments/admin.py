from django.contrib import admin
from .models import Appointment,Message,Notification

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'date', 'time', 'status')
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at', 'is_read')  # Use actual model fields
    list_filter = ('is_read', 'created_at')  # Optional: Add filters for read status and date
    search_fields = ('user__username', 'content')  # Optional: Add search capability