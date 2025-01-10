import uuid
import string
import secrets
import os
import logging
import re
from decimal import Decimal
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
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from mailjet_rest import Client
from django.contrib.auth import get_user_model
from payments.models import Plan,UserSubscription
import shutil
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from datetime import timedelta
from django.templatetags.static import static




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
    ADMIN = 'admin'
    DOCTOR = 'doctor'
    PATIENT = 'patient'



default_img = "static/images/profile_images/default.jpeg"


def generate_id(user_type):
    prefix = USER_TYPE_PREFIX.get(user_type, '9')
    print(prefix+'---------------')
    year = str(datetime.now().year)
    unique_part = str(uuid.uuid4().int)[:4]
    return f"{prefix}{year}{unique_part}"
            
            
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
        


def send_mail(recepiant,subject,message):
      print('sending mail')
      if settings.USE_MAILJET:
                # Create a Mailjet client
                mailjet = Client(auth=(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD), version='v3.1')

                data = {
                    'Messages': [
                        {
                            'From': {
                                'Email': 'baraahca2001@gmail.com',
                                'Name': 'Buolink',
                            },
                            'To': [
                                {
                                    'Email': recepiant.email,
                                    'Name': recepiant.name,
                                }
                            ],
                            'Subject': subject,
                            'TextPart': message,
                            'HTMLPart': message,
                        }
                    ]
                }

                result = mailjet.send.create(data=data)
                if result.status_code != 200:
                    print('error')
                    logger.error(f"Error sending email: {result.text}")
      else:
          print(f"Sending email to {recepiant.email}:")
          print(f"Subject: {subject}")
          print(f"Message:\n{message}")
                
                
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
        extra_fields.setdefault('user_type', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(id, email, name, password, **extra_fields)

# Helper function to delete files if they exist
def delete_file_if_exists(file_field):
    if file_field and os.path.exists(file_field.path):
        try:
            os.remove(file_field.path)
        except Exception as e:
            logger.error(f"Error deleting file: {e}")

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
    profile_image = models.ImageField(upload_to=f"static/images/profile_images/", default=default_img, validators=[validate_image_file])
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
            self.id = generate_id(self.user_type)
            if self.profile_image and self.profile_image !=default_img:
                rename_file(self.profile_image, 'img', self.id)
        
        # Generate a secure password if none is provided
        if not self.is_active:
            ADMINS= list(UserBase.objects.filter(user_type=UserType.ADMIN.value))
            subject = f"New User, {self.name}"
            message = render_to_string('mail/new_user.html', {
                'name':self.name,
                'id': self.id,
                'user_type':self.user_type,
            })
            #edit recepient to include all admins
            for admin in ADMINS:
                send_mail(admin,subject,message)
        if not self.password and self.is_active:
            genpassword = generate_secure_password()
            
            subject = f"Welcome to Biolink, {self.name}"
            credentials_message = render_to_string('mail/credentials_email.html', {
                'name':self.name,
                'id': self.id,
                'password': genpassword,
            })
            send_mail(self,subject,credentials_message)
            
            self.set_password(genpassword)
        print(self.user_type)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_type}: {self.name}"

    def delete(self, *args, **kwargs):
        send_mail(self,subject,credentials_message)
        if not self.profile_image == default_img:
            delete_file_if_exists(self.profile_image)
            subject = f"Your Biolink account has been deleted, {self.name}"
            deleted_message = render_to_string('mail/account_deleted.html', {
                'name':self.name,
            })
            
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
        Psychiatry = 'Psychiatry', _('Psychiatry')
        Diagnostic = 'Diagnostic', _('Diagnostic')
        Ripperdoc = 'Ripperdoc', _('Ripperdoc')
        NeuroSurgery = 'Neuro-surgery', _('Neuro-surgery')
        InfectiousDisease = 'Infectious Disease', _('Infectious Disease')
        

    license_number = models.CharField(max_length=255)
    degree_certificate = models.FileField(upload_to='static/certificates/', validators=[validate_pdf_file], blank=True, null=True)
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
        is_new = False
        if not self.id:
            is_new = True
            #fix here
            self.id = generate_id(self.user_type)
        
        if self.degree_certificate:
            rename_file(self.degree_certificate, 'degree_certificate', self.id)
            
        
        super().save(*args, **kwargs)
        if is_new:
            DoctorSchedule.create_default_schedule(self)





class Patient(UserBase):
    medical_history_file = models.FileField(upload_to='static/patients/medical_history/', validators=[validate_pdf_file], blank=True, null=True)
    date_of_birth = models.DateField()
    doctors = models.ManyToManyField('Doctor', through='DoctorPatient', related_name='assigned_patients')

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
        """
        Checks if the user has enough storage space left in their subscription plan.
        """
        try:
            subscription = self.usersubscription
        except UserSubscription.DoesNotExist:
            raise ValidationError("This patient does not have an active subscription.")
        
        common=1
        if subscription.plan.data_type == 'MB':
            common*=1024
        elif subscription.plan.data_type == 'GB':
            common=1024*1024
        remaining_space = (subscription.plan.data_limit * common) - (subscription.data_used*common)
        return file_size <= remaining_space  # file_size is in KB

    def update_used_storage(self, file_size):
        """
        Updates the used storage for the user's subscription if there is enough space.
        """
        try:
            subscription = self.usersubscription
        except UserSubscription.DoesNotExist:
            raise ValidationError("This patient does not have an active subscription.")

        if not self.has_space_for(file_size):
            raise ValidationError("Not enough storage available in the current plan.")

        common=1
        if subscription.plan.data_type == 'MB':
            common*=1024
        elif subscription.plan.data_type == 'GB':
            common=1024*1024
            
        

        subscription.data_used +=Decimal(file_size) / Decimal(1024)  
        subscription.save()

    def save(self, *args, **kwargs):
        is_new = self._state.adding  # Check if the object is being created
        if is_new:
            self.id = generate_id(self.user_type)

        if self.medical_history_file:
            rename_file(self.medical_history_file, 'medical_history_file', self.id)

        super().save(*args, **kwargs)

        # Assign free plan after the object is created
        if is_new:
            free_plan = Plan.objects.filter(name__iexact='free').first()
            if not free_plan:
                raise ValidationError("Free plan is not defined in the database.")

            # Create a subscription for the new patient
            UserSubscription.objects.create(
                user=self,
                plan=free_plan,
                data_used=0,
                plan_start_date=now().date(),
                plan_end_date=now().date() + timedelta(days=free_plan.duration),
                active=True,
            )

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
      
        super().save(*args, **kwargs)
    
    def clean(self):
        if DoctorPatient.objects.filter(patient=self.patient, doctor__specialty=self.doctor.specialty, status=DoctorPatient.Status.ACCEPTED).exists():
            raise ValidationError(_('Patient already has a doctor with this specialty.'))

    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name} ({self.status})"

class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=20)  # e.g., Monday, Tuesday, etc.
    start_time = models.TimeField()
    end_time = models.TimeField()

    def get_available_slots(self, date):
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
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        default_start_time = time(9, 0)  # 09:00 AM
        default_end_time = time(16, 0)  # 04:00 PM

        for day in weekdays:
            DoctorSchedule.objects.create(
                doctor=doctor,
                day_of_week=day,
                start_time=default_start_time,
                end_time=default_end_time
            )