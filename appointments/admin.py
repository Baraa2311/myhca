from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    # Customize the admin display
    list_display = ('patient_name', 'doctor', 'date', 'time')  # Access patient name directly
    list_filter = ('date', 'doctor')  # Filters in sidebar
    search_fields = ('patient__name', 'doctor__name')  # Searchable fields using patient name
    ordering = ('date', 'time')  # Default ordering

    # Define a method for patient name in list_display
    def patient_name(self, obj):
        return obj.patient.name
    patient_name.admin_order_field = 'patient__name'  # Allows sorting by patient name
    patient_name.short_description = 'Patient Name'  # Label for the column