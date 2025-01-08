from django import forms
from django import forms
from .models import Ad,MedicalAdvice
from django.core.exceptions import ValidationError
import os
import datetime
import logging


logger = logging.getLogger(__name__)







default_advice_img = "static/images/advice/default.png"
        
class MedAdviceForm(forms.ModelForm):
    class Meta:
        model = MedicalAdvice
        fields = ['title','advice','image']

    