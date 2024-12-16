import os
from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Administrator, Doctor

class Ad(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='static/images/ads/', blank=True, null=True)
    created_by = models.ForeignKey(Administrator, on_delete=models.CASCADE, related_name='advice')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        # Delete the image file if it exists
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)

class MedicalAdvice(models.Model):
    title = models.CharField(max_length=200)
    advice = models.TextField()
    image = models.ImageField(upload_to=f"static/images/advice/", blank=True, null=True)
    created_by = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='advice')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.created_by.name}"

    def delete(self, *args, **kwargs):
        # Delete the image file if it exists
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)