from django import forms
from django import forms
from .models import Ad,MedicalAdvice
from django.core.exceptions import ValidationError
import os
from django.utils.text import slugify
import logging
import datetime

def rename_file(instance, name_prefix, file_type, uname):
    try:
        extension = instance.name.split('.')[-1]
        filename = f"{slugify(uname)}_{name_prefix}_{file_type}.{extension}"
        instance.name = os.path.join(f'{name_prefix}s/', filename)
    except Exception as e:
        logger.error(f"Error renaming file for {uname}: {e}")
        raise ValidationError(f"Error renaming file: {str(e)}")



        
class MedAdviceForm(forms.ModelForm):
    class Meta:
        model = MedicalAdvice
        fields = ['title','advice','image']

    def save(self, commit=True):
        instance = super().save(commit=False)
        img = instance.image
        if img:
            rename_file(img, 'advice', 'advice_img', instance.title)
        if commit:
            instance.save()
        return instance