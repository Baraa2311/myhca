from django.contrib import admin
from .models import Diagnostic,Prescription

class DiagnosticAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'doctor', 'patient', 'test_name', 'test_results')
    search_fields = ('created_at', 'doctor', 'patient', 'test_name')
    ordering = ('created_at',)

    fieldsets = (
        (None, {'fields': ( 'doctor', 'patient', 'test_name','test_results')}),
    )

class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'doctor', 'patient', 'medication_name', 'dosage','instructions')
    search_fields = ('created_at', 'doctor', 'patient', 'medication_name')
    ordering = ('created_at',)

    fieldsets = (
        (None, {'fields': ('doctor', 'patient', 'medication_name', 'dosage','instructions')}),
    )

admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(Diagnostic, DiagnosticAdmin)