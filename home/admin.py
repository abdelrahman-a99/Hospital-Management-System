from django.contrib import admin
from .models import ContactSubmission, Department, Service, Testimonial, News


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('submitted_at',)
    ordering = ('-submitted_at',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('created_at', 'updated_at')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'price', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('department', 'created_at')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'rating', 'is_featured', 'created_at')
    search_fields = ('name', 'role', 'content')
    list_filter = ('rating', 'is_featured', 'created_at')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_featured', 'published_at')
    search_fields = ('title', 'content', 'author')
    list_filter = ('is_featured', 'published_at')
    prepopulated_fields = {'slug': ('title',)}
