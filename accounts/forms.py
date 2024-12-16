from django import forms
from .models import Doctor, Patient, UserBase
from django import forms
from .models import Doctor, Patient, Administrator
from allauth.account.forms import SignupForm
from phonenumber_field.formfields import PhoneNumberField
from django.core.exceptions import ValidationError
import os
from django.utils.text import slugify
import logging
import datetime

# Setup logging
logger = logging.getLogger(__name__)

# Utility function to rename profile images
def rename_file(instance, name_prefix, file_type, uname):
    try:
        extension = instance.name.split('.')[-1]
        filename = f"{slugify(uname)}_{name_prefix}_{file_type}.{extension}"
        instance.name = os.path.join(f'{name_prefix}s/', filename)
    except Exception as e:
        logger.error(f"Error renaming file for {uname}: {e}")
        raise ValidationError(f"Error renaming file: {str(e)}")
        
        
class DoctorSignUpForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'email','license_number', 'phone_number','bio', 'specialty', 'degree_certificate']

    def clean_specialty(self):
        specialty = self.cleaned_data.get('specialty')
        if not specialty:
            raise ValidationError('Specialty is required.')
        return specialty

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        degree_certificate = instance.degree_certificate
        uname = instance.name

        
            
        
        if degree_certificate:
            rename_file(degree_certificate, 'doctor', 'degree_certificate', uname)

        if commit:
            instance.save()
        return instance

from django import forms
from .models import Patient
from django.forms import DateInput

class PatientSignUpForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'email', 'phone_number', 'date_of_birth', 'medical_history_file']
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'dob-datepicker'})
        }

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        age = (datetime.date.today() - dob).days // 365
        if age < 18:
            raise ValidationError('Patient must be at least 18 years old.')
        return dob

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        medical_history_file = instance.medical_history_file
        uname = instance.name      
        
        if medical_history_file:
            rename_file(medical_history_file, 'patient', 'medical_history', uname)

        if commit:
            instance.save()
        return instance

class AdminSignUpForm(forms.ModelForm):
    class Meta:
        model = Administrator
        fields = ['name', 'email', 'phone_number']
  
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user_type = 'admin'
        uname = instance.name     
        
        if commit:
            instance.save()
        return instance