import uuid
import string
import secrets
import os
import logging
import re
from django.utils.text import slugify
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse
from enum import Enum
from django.core.exceptions import ValidationError
from PIL import Image
from django.utils.timezone import now
from django.utils import timezone
from datetime import time, timedelta
from appointments.models import Appointment
# Set up logging
logger = logging.getLogger(__name__)

# Constants for prefixes and user types
USER_TYPE_PREFIX = {
    'administrator': '1',
    'doctor': '2',
    'patient': '3'
}

# Enum class for user types
class UserType(Enum):
    ADMIN = 'administrator'
    DOCTOR = 'doctor'
    PATIENT = 'patient'
default_img="static/images/profile_images/default.jpeg"

def generate_id(user_type):
            prefix = USER_TYPE_PREFIX.get(user_type, '9')
            year = str(datetime.now().year)
            unique_part = str(uuid.uuid4().int)[:4]
            return f"{prefix}{year}{unique_part}"
            
            
def rename_file(instance,file_type, id):
    try:
        extension = instance.name.split('.')[-1]
        filename = f"{slugify(id)}_{file_type}.{extension}"
        instance.name = os.path.join(filename)
    except Exception as e:
        logger.error(f"Error renaming file for {id}: {e}")
        raise ValidationError(f"Error renaming file: {str(e)}")
        
# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, id, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(id=id, email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('user_type', UserType.ADMIN.name)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(id, email, name, password, **extra_fields)


        
# Helper function to delete files if they exist
def delete_file_if_exists(file_field):
    if file_field and os.path.exists(file_field.path):
        os.remove(file_field.path)


# Password Generation Function
def generate_secure_password(length=12):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        if (re.search(r'[a-z]', password) and
            re.search(r'[A-Z]', password) and
            re.search(r'[0-9]', password) and
            re.search(r'[\W_]', password)):  # \W matches non-alphanumeric characters
            break  # Valid password
    return password

# Custom validation for file types
def validate_image_file(value):
    ext = value.name.split('.')[-1].lower()
    valid_extensions = ['jpg', 'jpeg', 'png']
    max_size = 5 * 1024 * 1024  # 5MB limit
    if ext not in valid_extensions:
        raise ValidationError(f"Invalid file extension. Allowed extensions are: {', '.join(valid_extensions)}")
    if value.size > max_size:
        raise ValidationError(f"File size should not exceed 5MB.")

def validate_pdf_file(value):
    ext = value.name.split('.')[-1].lower()
    max_size = 10 * 1024 * 1024  # 10MB limit
    if ext != 'pdf':
        raise ValidationError("Invalid file extension. Only PDF is allowed.")
    if value.size > max_size:
        raise ValidationError(f"File size should not exceed 10MB.")        
        
# Custom UserBase model
class UserBase(AbstractBaseUser, PermissionsMixin):
    STATUS_CHOICES = [(True, 'Active'), (False, 'Inactive')]
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(choices=STATUS_CHOICES, default=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    user_type = models.CharField(
        max_length=10,
        choices=[(tag.name, tag.value) for tag in UserType],
    )
    profile_image = models.ImageField(upload_to=f"static/images/profile_images/",default=default_img, validators=[validate_image_file])
    id = models.CharField(max_length=9, unique=True, primary_key=True, editable=False)
    phone_number = PhoneNumberField(blank=True, null=True)
    
    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['name', 'email']

    objects = UserManager()

    def save(self, *args, **kwargs):
        
        # Set the user_type based on the class name if not already set
        if not self.user_type:
            self.user_type = self.__class__.__name__.lower()

        # Generate a unique ID if not already set
        if not self.id:
            self.id=generate_id(self.user_type)
        # Generate a secure password if none is provided
        if not self.password and self.is_active:
            genpassword = generate_secure_password()
            mail_file_path = f"mail/{self.id}.txt"
            with open(mail_file_path, 'w') as mail_file:
                mail_file.write(f"Your ID is: {self.id}\nYour password is: {genpassword}")
            self.set_password(genpassword)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.specialty}" if self.is_doctor else f"Patient: {self.name}"

    def delete(self, *args, **kwargs):
        if not self.profile_image==default_img:
            delete_file_if_exists(self.profile_image)
        super().delete(*args, **kwargs)

    @property
    def is_patient(self):
        return self.user_type == UserType.PATIENT.value

    @property
    def is_doctor(self):
        return self.user_type == UserType.DOCTOR.value

    @property
    def is_administrator(self):
        return self.user_type == UserType.ADMIN.value


# Doctor-specific model
class Doctor(UserBase):
    class Specialty(models.TextChoices):
        Dentist = 'Dentist', _('Dentist')

        Psychiatrist = 'Psychiatrist', _('Psychiatrist')

        ENT = 'ENT', _('ENT')


    license_number = models.CharField(max_length=255)
    degree_certificate = models.FileField(upload_to='static/certificates/',validators=[validate_pdf_file], blank=True, null=True)
    bio = models.TextField(blank=True)
    specialty = models.CharField(max_length=50, choices=Specialty.choices)
    patients = models.ManyToManyField('Patient', through='DoctorPatient', related_name='selected_doctors')

    class Meta:
        verbose_name = "Doctor"

    def __str__(self):
        return f"Dr. {self.name} ({self.specialty})"

    def get_absolute_url(self):
        return reverse("doctor_detail", args=[str(self.id)])

    def delete(self, *args, **kwargs):
        delete_file_if_exists(self.degree_certificate)
        super().delete(*args, **kwargs)
   
    def save(self, *args, **kwargs):  
        # Generate a unique ID if not already set
        is_new=False
        if not self.id:
            is_new=True
            self.id=generate_id(self.user_type)
                       
        if self.degree_certificate:
            rename_file(self.degree_certificate, 'degree_certificate', self.id)
            
        super().save(*args, **kwargs)
        if is_new:
            DoctorSchedule.create_default_schedule(self)
    
    
# Administrator-specific model
class Administrator(UserBase):
    class Meta:
        verbose_name = "Administrator"


# Patient-specific model
class Patient(UserBase):
    medical_history_file = models.FileField(upload_to='static/patients/medical_history/', validators=[validate_pdf_file], blank=True, null=True)
    
    date_of_birth = models.DateField()
    storage_limit = models.BigIntegerField(default=52428800)  # 50 MB default limit in bytes
    used_storage = models.BigIntegerField(default=0)
    doctors= models.ManyToManyField('Doctor', through='DoctorPatient', related_name='assigned_patients')

    class Meta:
        verbose_name = "Patient"

    def __str__(self):
        return f"Patient: {self.name}"

    def get_absolute_url(self):
        return reverse("patient_detail", args=[str(self.id)])

    def delete(self, *args, **kwargs):
        delete_file_if_exists(self.medical_history_file)
        super().delete(*args, **kwargs)

    def has_space_for(self, file_size):
        return (self.used_storage + file_size) <= self.storage_limit

    def update_used_storage(self, file_size):
        if not self.has_space_for(file_size):
            raise ValidationError(_('Not enough storage available for this file.'))
        self.used_storage += file_size
        self.save()
 
    def save(self, *args, **kwargs):         
        # Generate a unique ID if not already set
        if not self.id:
            if not self.id:
                self.id=generate_id(self.user_type)
        
                
        if self.medical_history_file :
            rename_file(self.medical_history_file, 'medical_history_file', self.id)

        super().save(*args, **kwargs)

# Relationship between Doctor and Patient
class DoctorPatient(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Pending', _('Pending')
        ACCEPTED = 'Accepted', _('Accepted')
        REJECTED = 'Rejected', _('Rejected')

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='doctor_relationships')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patient_relationships')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    date_assigned = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('patient', 'doctor')
        
        
    def save(self, *args, **kwargs):
        if self.status == self.Status.ACCEPTED:
            # Handle logic when a doctor accepts a patient
            # Example: Send email notification to patient
            pass
        super().save(*args, **kwargs)
    
    
    def clean(self):
        # Ensure a patient cannot have multiple doctors with the same specialty
        if DoctorPatient.objects.filter(patient=self.patient, doctor__specialty=self.doctor.specialty, status=DoctorPatient.Status.ACCEPTED).exists():
            raise ValidationError(_('Patient already has a doctor with this specialty.'))

    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name} ({self.status})"
        
from datetime import timedelta, time
from django.utils import timezone
from django.db import models
from .models import Appointment  # Import your Appointment model

class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=20)  # e.g., Monday, Tuesday, etc.
    start_time = models.TimeField()
    end_time = models.TimeField()

    def get_available_slots(self, date):
        """
        Generate available 30-minute time slots between start_time and end_time,
        excluding already booked slots, for a specific date.
        """
        available_slots = []
        current_time = self.start_time

        # Fetch appointments for the specific date (exact match on date)
        booked_slots = Appointment.objects.filter(
            doctor=self.doctor,
            date=date
        ).values_list('time', flat=True)

        while current_time < self.end_time:
            if current_time not in booked_slots:
                available_slots.append(current_time)
            current_time = (
                timezone.datetime.combine(timezone.now().date(), current_time) + timedelta(minutes=30)
            ).time()  # 30-minute intervals
        return available_slots

    @staticmethod
    def create_default_schedule(doctor):
        """
        Creates a default schedule for a doctor from Monday to Friday, 9 AM to 4 PM.
        """
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        default_start_time = time(9, 0)  # 09:00 AM
        default_end_time = time(16, 0)  # 04:00 PM

        schedules = [
            DoctorSchedule(
                doctor=doctor,
                day_of_week=day,
                start_time=default_start_time,
                end_time=default_end_time
            )
            for day in weekdays
        ]
        DoctorSchedule.objects.bulk_create(schedules)

    def update_schedule(self, updated_schedules):
        """
        Updates the doctor's schedule.
        :param updated_schedules: A list of dictionaries containing day_of_week, start_time, and end_time.
        """
        for schedule in updated_schedules:
            DoctorSchedule.objects.update_or_create(
                doctor=self.doctor,
                day_of_week=schedule['day_of_week'],
                defaults={
                    'start_time': schedule['start_time'],
                    'end_time': schedule['end_time'],
                }
            )