from django import forms
import os

from .models import Diagnostic,Prescription

class DiagnosticForm(forms.ModelForm):
    class Meta:
        model = Diagnostic
        fields = ['test_name','test_results']
        
        def save(self, commit=True):
            instance = super().save(commit=False)
            instance.patient =patient
            instance.doctor = doctor
            instance.save()
        