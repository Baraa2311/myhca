import os
from django.db import models
import logging
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from accounts.models import UserBase, Doctor
import shutil
from django.templatetags.static import static

default_ad_img = "static/images/ads/default.png"
default_advice_img = "static/images/advice/default.png"

# Set up logging
logger = logging.getLogger(__name__)

# Custom validation for file types
def validate_image_file(value):
    ext = value.name.split('.')[-1].lower()
    valid_extensions = ['jpg', 'jpeg', 'png']
    max_size = 5 * 1024 * 1024  # 5MB limit
    if ext not in valid_extensions:
        raise ValidationError(f"Invalid file extension. Allowed extensions are: {', '.join(valid_extensions)}")
    if value.size > max_size:
        raise ValidationError(f"File size should not exceed 5MB.")










logger = logging.getLogger(__name__)

def rename_file(instance, file_type, id):
    try:
        # Get the file extension and path
        extension = instance.name.split('.')[-1]
        file_path = os.path.dirname(instance.name)  # Get the directory path
        new_filename = f"{slugify(id)}_{file_type}.{extension}"  # Create new file name
        new_file_path = os.path.join(file_path, new_filename)  # New file path
        
        # Rename the file on the file system
        if os.path.exists(instance.name):
            shutil.move(instance.name, new_file_path)  # Rename file in the directory

        # Update the file name in the database
        instance.name = new_file_path  # Update the field to the new name

    except Exception as e:
        logger.error(f"Error renaming file for {id}: {e}")
        raise ValidationError(f"Error renaming file: {str(e)}")


class Ad(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='static/images/ads/', default=default_ad_img, validators=[validate_image_file])
    created_by = models.ForeignKey(UserBase, on_delete=models.CASCADE, related_name='ad')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
     
    def save(self, *args, **kwargs):
        
      if self.image and self.id and self.image.name != default_advice_img:
        rename_file(self.image, 'image', self.id)
        
      super().save(*args, **kwargs)
     
    def delete(self, *args, **kwargs):
        # Delete the image file if it exists
        if self.image and not default_ad_img==self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)

class MedicalAdvice(models.Model):
    title = models.CharField(max_length=200)
    advice = models.TextField()
    image = models.ImageField(upload_to=f"static/images/advice/", default=default_advice_img, validators=[validate_image_file])
    created_by = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='advice')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.created_by.name}"
    
    def save(self, *args, **kwargs):
        
      if self.image and self.id and self.image.name != default_advice_img:
        rename_file(self.image, 'image', self.id)
        
      super().save(*args, **kwargs)
    
    
    def delete(self, *args, **kwargs):
        # Delete the image file if it exists
        if self.image and not default_advice_img==self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)