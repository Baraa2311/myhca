from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserBase, Doctor, Patient,DoctorPatient



# General Custom User Admin
class UserBaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'email', 'user_type', 'phone_number', 'is_staff', 'is_active')
    search_fields = ('name', 'id', 'email', 'phone_number')
    ordering = ('id',)

    # For viewing/editing user details
    fieldsets = (
        (None, {'fields': ('name', 'email', 'phone_number', 'user_type', 'profile_image')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    # For creating new users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email','phone_number', 'user_type', 'profile_image')}
        ),
    )
    
    





# Doctor Admin
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'email', 'specialty', 'phone_number', 'is_active')
    search_fields = ('name', 'id', 'email', 'specialty')
    ordering = ('id',)

    fieldsets = (
        (None, {'fields': ('name', 'email', 'phone_number', 'profile_image', 'specialty', 'license_number', 'degree_certificate', 'bio')}),
        ('Status', {'fields': ('is_active',)}),
    )


# Patient Admin
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'email', 'date_of_birth', 'phone_number', 'is_active')
    search_fields = ('name', 'id', 'email', 'phone_number')
    ordering = ('id',)

    fieldsets = (
        (None, {'fields': ('name', 'email',  'phone_number', 'profile_image', 'date_of_birth', 'medical_history_file')}),
        ('Status', {'fields': ('is_active',)}),
    )


class DoctorPatientAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'status', 'date_assigned']
    list_filter = ['status', 'doctor', 'patient']
    search_fields = ['patient__name', 'doctor__name']

admin.site.register(DoctorPatient, DoctorPatientAdmin)


# Register Models in Admin Site
admin.site.register(UserBase, UserBaseAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)