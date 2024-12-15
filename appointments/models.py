from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import time
from datetime import timedelta



class Appointment(models.Model):
    patient = models.ForeignKey('accounts.Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('accounts.Doctor', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=time(9, 0))
    duration = models.DurationField(default=timedelta(minutes=30))
    

    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name} at {self.date} {self.time}"