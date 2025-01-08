import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from allauth.account.views import SignupView
from .forms import DoctorSignUpForm, PatientSignUpForm
from .models import Doctor, Patient, DoctorPatient,UserBase
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from appointments.models import Appointment
from datetime import datetime
from django.db.models import Q
from notifications.signals import notify
from django.shortcuts import redirect
from django.views import View
from notifications.models import Notification
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

class DoctorMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_doctor

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a doctor.")
        return redirect('home')
    
class PatientMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_patient

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a patient.")
        return redirect('home')
    


class MarkAllNotificationsReadView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Mark all unread notifications as read for the authenticated user
            Notification.objects.filter(recipient=request.user, unread=True).update(unread=False)
        return redirect('home')  # Or redirect to any other page, like the profile page

def send_notification(sender,receiver, message):
     notify.send(
        sender,  # sender
        recipient=receiver,  # recipient
        verb=message,  # message
    ) 

# Set up logging
logger = logging.getLogger(__name__)

# Enhanced Doctor Signup
class DoctorSignUpView(SignupView):
    form_class = DoctorSignUpForm
    template_name = 'account/signup_doctor.html'

    def form_valid(self, form):
        doctor = form.save(commit=False)
        doctor.user_type = 'doctor'
        doctor.save()
        
        logger.info(f"Doctor {doctor.name} registered successfully.")
        return redirect('registration_pending')

# Enhanced Patient Signup
class PatientSignUpView(SignupView):
    form_class = PatientSignUpForm
    template_name = 'account/signup_patient.html'

    def form_valid(self, form):
        patient = form.save(commit=False)
        patient.user_type = 'patient'
        patient.save()
        
        logger.info(f"Patient {patient.name} registered successfully.")
        return redirect('registration_pending')



# Registration Pending View
class RegistrationPendingView(TemplateView):
    template_name = 'registration_pending.html'


# Enhanced Doctor Home View
class DoctorHomeView(LoginRequiredMixin, DoctorMixin, TemplateView):
    template_name = 'homepages/doctor_home.html'


# Enhanced Patient Home View
class PatientHomeView(LoginRequiredMixin, PatientMixin, TemplateView):
    template_name = 'homepages/patient_home.html'
    login_url = 'custom_login_redirect'


        

        
# Select Doctor View - Enhanced with Error Handling and Feedback
@login_required
def select_doctor(request):
    patient = get_object_or_404(Patient, id=request.user.id)
    if request.method == 'POST':
        specialty = request.POST.get('specialty')
        doctor_id = request.POST.get('doctor_id')

        # Ensure doctor exists
        doctor = get_object_or_404(Doctor, id=doctor_id)
        
        


        # Ensure the user can only have one doctor per specialty
        print("gg")
        # Check if the DoctorPatient relationship exists
        existing_selection = DoctorPatient.objects.            filter(patient=patient, doctor__specialty=specialty).first()

        if existing_selection:
            print(existing_selection)
            # Send notification
            send_notification(existing_selection.patient, existing_selection.doctor, f"Patient {existing_selection.patient.name} has left your patient list")
            # Delete the record
            existing_selection.delete()
        else:
            print("No such relationship exists.")

        # Create new selection
        DoctorPatient.objects.create(patient=patient, doctor=doctor, status='Pending')
        send_notification(patient,doctor,f"Patient {patient.name} has requested your services")
        
        messages.success(request, f"Doctor {doctor.name} assigned successfully.")
        logger.info(f"Patient {patient.name} selected doctor {doctor.name} successfully.")
        return JsonResponse({"message": "Doctor assigned successfully"})

    specialties = {
        specialty: Doctor.objects.filter(specialty=specialty)
        for specialty in Doctor.objects.values_list("specialty", flat=True).distinct()
    }
    
    selected_doctors = patient.selected_doctors.all()
    relations = []
    
    for doctor in selected_doctors:  
       
        relation=DoctorPatient.objects.get(doctor=doctor, patient=patient)
        current_datetime = datetime.now()
        relation.doctor.has_appointment = Appointment.objects.filter(
    doctor=doctor,
    patient=patient
).filter(
    Q(date__gt=current_datetime.date()) |  # Future dates
    Q(date=current_datetime.date(), time__gte=current_datetime.time())  # Same date, future time
).first()
        relations.append(relation)
        
        
    
    
    return render(request, "patient/select_doctor.html", {
        "specialties": specialties,
        "relations": relations,
        "selected_doctors":selected_doctors,
       
    })






# Profile Detail View
class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserBase
    template_name = "profile/profile_detail.html"
    context_object_name = "user_profile"

    def get_object(self):
        user=self.request.user
        if self.request.user.is_doctor:
            user=get_object_or_404(Doctor, id=self.request.user.id)
        return user

# Profile Update View
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserBase
    
    fields = ['name', 'email', 'phone_number', 'profile_image'] 
    template_name = "profile/profile_edit.html"
    context_object_name = "user_profile"
    success_url='profile'
    def get_object(self):
            self.model = Doctor
            user=self.request.user
            if self.request.user.is_doctor:
                user=get_object_or_404(Doctor, id=self.request.user.id)
                self.fields.append('bio')
            return user
    
    def form_valid(self, form):
       user= form.save(commit=False)
       if user.is_doctor:
         user.bio=form['bio'].data
       try:
           user.save()
       except ValidationError as e:
                form.add_error(None, str(e))  
                return self.form_invalid(form)
       return redirect(self.success_url)
        
    def get_success_url(self):
        return reverse_lazy('profile')  
        
        
        
@login_required
def doctor_requests(request):
    doctor = get_object_or_404(Doctor, id=request.user.id)
    pending_requests = DoctorPatient.objects.filter(doctor=doctor, status='Pending')
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        action = request.POST.get('action')  # Accept or Reject
        relationship = get_object_or_404(DoctorPatient, doctor=doctor, patient_id=patient_id)

        if action == 'accept':
            relationship.status = 'Accepted'
            send_notification(relationship.doctor,relationship.patient,f"Doctor {relationship.doctor.name} has accepted you as his patient")
            messages.success(request, f"Accepted request from {relationship.patient.name}.")
        elif action == 'reject':
            send_notification(relationship.doctor,relationship.patient,f"Doctor {relationship.doctor.name} has rejected you as his patient")
            relationship.status = 'Rejected'
            messages.success(request, f"Rejected request from {relationship.patient.name}.")
        relationship.save()
        return JsonResponse({"message": "Request updated successfully."})

    return render(request, "doctor/requests.html", {"pending_requests": pending_requests})




@login_required
def delete_doctor(request):
       
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            doc_Id = data.get("doctor_id")
            if not doc_Id:
                return JsonResponse({"error": "Invalid Doctor ID"}, status=400)
            patient = get_object_or_404(Patient, id=request.user.id)
            doctor = get_object_or_404(Doctor, id=doc_Id)
    
            # Make sure the relationship exists before attempting to delete
            try:
                relationship = DoctorPatient.objects.get(patient=patient, doctor=doctor)
            except DoctorPatient.DoesNotExist:
                return JsonResponse({"error": "Relationship not found"}, status=404)

         
            
            relationship.delete()
            return JsonResponse({"message": "Doctor deleted successfully!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)
        
          
            
                
    relationship.delete()
    send_notification(patient, doctor, f"Patient {patient.name} has left your patient list")
    
    # Respond with JSON to confirm deletion
    return JsonResponse({"success": "Doctor removed successfully."}, status=200)


@login_required
def doctor_details(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, "patient/doctor_details.html", {"doctor": doctor})

# Enhanced Appointment Times Retrieval
def get_appointment_times(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    # Replace with actual logic for fetching available appointment times
    available_times = [
        "9:00 AM - 10:00 AM",
        "11:00 AM - 12:00 PM",
        "2:00 PM - 3:00 PM",
    ]

    logger.info(f"Retrieved available appointment times for doctor {doctor.name}.")
    return JsonResponse({'times': available_times})