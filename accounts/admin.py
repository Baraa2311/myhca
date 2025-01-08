from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserBase, Doctor, Patient,DoctorPatient



from django.contrib import admin
from .models import UserBase

class UserBaseAdmin(admin.ModelAdmin):
    list_display = ( 'id','name', 'email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'email')
    actions = ['activate_users', 'delete_users']
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(is_active=False)

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f'{queryset.count()} user(s) activated.')

    def delete_users(self, request, queryset):
        queryset.delete()
        self.message_user(request, f'{queryset.count()} user(s) deleted.')

    activate_users.short_description = 'Activate selected users'
    delete_users.short_description = 'Delete selected users'
    


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