from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django import forms
from .models import Patient, Doctor, Review

User = get_user_model()

class BaseProfileAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_email', 'gender', 'phone_number', 'address', 'dob')
    list_filter = ('gender',)
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'phone_number')
    readonly_fields = ('user',)

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'get_user_role')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    def get_user_role(self, obj):
        if obj.is_superuser:
            return 'Admin'
        if obj.groups.filter(name='Doctors').exists():
            return 'Doctor'
        if obj.groups.filter(name='Patients').exists():
            return 'Patient'
        return 'User'
    get_user_role.short_description = 'Role'
    get_user_role.admin_order_field = 'is_superuser'

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj:  # Only add role info in detail view
            role = self.get_user_role(obj)
            fieldsets = list(fieldsets)
            fieldsets.insert(2, ('Role Information', {'fields': [], 'description': f'This user is a {role}'}))
        return fieldsets

# Unregister the default UserAdmin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

class PatientCreationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Patient
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 
                 'gender', 'phone_number', 'address', 'dob')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Create the User first
        user = User.objects.create_user(
            username=self.cleaned_data['email'].split('@')[0],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        user.groups.add(Group.objects.get(name='Patients'))

        # Create the Patient profile
        patient = super().save(commit=False)
        patient.user = user
        if commit:
            patient.save()
        return patient

@admin.register(Patient)
class PatientAdmin(BaseProfileAdmin):
    form = PatientCreationForm

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:  # This is the add form
            return PatientCreationForm
        # For editing, use a regular ModelForm with only Patient fields
        class PatientEditForm(forms.ModelForm):
            class Meta:
                model = Patient
                fields = ('gender', 'phone_number', 'address', 'dob')
        return PatientEditForm

    def get_fieldsets(self, request, obj=None):
        if obj is None:  # Add form
            return (
                ('User Information', {
                    'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')
                }),
                ('Patient Information', {
                    'fields': ('gender', 'phone_number', 'address', 'dob')
                }),
            )
        # Edit form
        return (
            ('User Information', {
                'fields': ('user',)
            }),
            ('Patient Information', {
                'fields': ('gender', 'phone_number', 'address', 'dob')
            }),
        )

    def get_readonly_fields(self, request, obj=None):
        if obj is None:  # Add form
            return ()
        return ('user',)  # Make user field readonly in edit form

class DoctorCreationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Doctor
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 
                 'gender', 'phone_number', 'address', 'dob', 'specialty')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Create the User first
        user = User.objects.create_user(
            username=self.cleaned_data['email'].split('@')[0],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        user.groups.add(Group.objects.get(name='Doctors'))

        # Create the Doctor profile
        doctor = super().save(commit=False)
        doctor.user = user
        if commit:
            doctor.save()
        return doctor

@admin.register(Doctor)
class DoctorAdmin(BaseProfileAdmin):
    form = DoctorCreationForm
    list_display = BaseProfileAdmin.list_display + ('specialty',)
    list_filter = BaseProfileAdmin.list_filter + ('specialty',)
    search_fields = BaseProfileAdmin.search_fields + ('specialty',)

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:  # This is the add form
            return DoctorCreationForm
        # For editing, use a regular ModelForm with only Doctor fields
        class DoctorEditForm(forms.ModelForm):
            class Meta:
                model = Doctor
                fields = ('gender', 'phone_number', 'address', 'dob', 'specialty')
        return DoctorEditForm

    def get_fieldsets(self, request, obj=None):
        if obj is None:  # Add form
            return (
                ('User Information', {
                    'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')
                }),
                ('Doctor Information', {
                    'fields': ('gender', 'phone_number', 'address', 'dob', 'specialty')
                }),
            )
        # Edit form
        return (
            ('User Information', {
                'fields': ('user',)
            }),
            ('Doctor Information', {
                'fields': ('gender', 'phone_number', 'address', 'dob', 'specialty')
            }),
        )

    def get_readonly_fields(self, request, obj=None):
        if obj is None:  # Add form
            return ()
        return ('user',)  # Make user field readonly in edit form

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 
                    'doctor__user__first_name', 'doctor__user__last_name', 
                    'content')
    readonly_fields = ('patient', 'doctor', 'created_at')
