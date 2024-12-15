from django.db import models
from django.conf import settings
from accounts.models import Patient
from django.core.exceptions import ValidationError

class MedicalFile(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_files')
    file = models.FileField(upload_to=f"medical_files")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(
        max_length=50,
        choices=[
            ('photo', 'Photo'),
            ('video', 'Video'),
            ('ct_scan', 'CT Scan'),
            ('x_ray', 'X-Ray'),
            ('other', 'Other')
        ],
        default='other'
    )
    def save(self, *args, **kwargs):
        # Update storage usage
        if not self.pk:  # Only update on new file uploads
            file_size = self.file.size
            if not self.patient.has_space_for(file_size):
                raise ValidationError("Not enough storage space.")
            self.patient.update_used_storage(file_size)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient.name} - {self.file_type} ({self.uploaded_at})"