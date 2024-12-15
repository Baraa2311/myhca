from django import forms
from .models import MedicalFile

class MedicalFileUploadForm(forms.ModelForm):
    class Meta:
        model = MedicalFile
        fields = ['file', 'file_type']
        widgets = {
            'file_type': forms.Select(attrs={'class': 'form-select'}),
        }