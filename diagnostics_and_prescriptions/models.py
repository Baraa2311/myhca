from django.db import models
from accounts.models import Patient,Doctor
from django.urls import reverse

class Diagnostic(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='diagnostics')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='diagnostics')
    test_name = models.CharField(max_length=255)
    test_results = models.TextField()
    test_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_absolute_url(self):
        return reverse("patient_diagnostics", args=[str(self.patient.id)])
        
    def __str__(self):
        return f"{self.test_name} for {self.patient.name}"
        
class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='prescriptions')
    medication_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255)
    instructions = models.TextField()
    issue_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_absolute_url(self):
        return reverse("patient_prescriptions", args=[str(self.patient.id)])
        
    def __str__(self):
        return f"Prescription for {self.patient.name} - {self.medication_name}"