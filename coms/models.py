from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Administrator,Doctor
class Ad(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='static/notifications/ads/', blank=True, null=True)
    created_by = models.ForeignKey(Administrator, on_delete=models.CASCADE, related_name='advice')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
        
class MedicalAdvice(models.Model):
    title = models.CharField(max_length=200)
    advice = models.TextField()
    image = models.ImageField(upload_to='static/notifications/advice/', blank=True, null=True)
    created_by = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='advice')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.doctor.name}"