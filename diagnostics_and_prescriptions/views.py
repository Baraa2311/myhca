from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from accounts.models import Patient
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DetailView, ListView,DeleteView
from .models import Diagnostic, Prescription
from django.urls import reverse_lazy
from notifications.signals import notify


def send_notification(sender,receiver, message):
      notify.send(
        sender,  # sender
        recipient=receiver,  # recipient
        verb=message,  # message
    )
    
class DoctorMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_doctor

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a doctor.")
        return redirect('home')    
        
class DoctorPatientMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_doctor or self.request.user.is_patient

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a doctor nor patient")
        return redirect("home")

class DiagnosticListView(LoginRequiredMixin, DoctorPatientMixin, ListView):
    
    model = Diagnostic
    template_name = "doctor/patient_diagnostics.html"
    context_object_name = "diagnosis"

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient_id'] = self.kwargs["patient_id"]
        return context
        
    def get_queryset(self):
        return Diagnostic.objects.filter(patient_id=self.kwargs["patient_id"])


class PrescriptionListView(LoginRequiredMixin, DoctorPatientMixin, ListView):
    model = Prescription
    template_name = "doctor/patient_prescriptions.html"
    context_object_name = "prescriptions"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient_id'] = self.kwargs["patient_id"]
        return context
        
    def get_queryset(self):
        return Prescription.objects.filter(patient_id=self.kwargs["patient_id"])
        


# Diagnostic Views
class DiagnosticCreateView(LoginRequiredMixin, DoctorMixin, CreateView):
    model = Diagnostic
    fields = ['test_name', 'test_results']  # Exclude patient and doctor fields
    template_name = 'doctor/add_diagnostic.html'  
    def form_valid(self, form): 
        doctor=self.request.user.doctor
        patient=get_object_or_404(Patient, id=self.kwargs['patient_id'])
        form.instance.doctor =  doctor
        form.instance.patient = patient
        send_notification(doctor,patient,f"Dr.{doctor.name} given you a new diagnosis")
        return super().form_valid(form)

class DiagnosticDeleteView(LoginRequiredMixin,DoctorMixin,DeleteView): 
    model = Diagnostic 
    template_name = 'doctor/diagnostic_delete.html' 
    success_url = reverse_lazy('patient_list')


class DiagnosticUpdateView(LoginRequiredMixin, DoctorMixin, UpdateView):
    model = Diagnostic
    fields = ['test_name', 'test_results']
    template_name = 'doctor/add_diagnostic.html'

    def form_valid(self, form):
        # Get the updated prescription object
        diagnostic = form.save()

        # Send notification for the updated prescription
        send_notification(
            diagnostic.doctor, 
            diagnostic.patient, 
            f"Dr. {diagnostic.doctor.name} has updated a diagnosis"
        )

        # Return the response for a valid form submission
        return super().form_valid(form)

# Prescription Views
class PrescriptionCreateView(LoginRequiredMixin, DoctorMixin, CreateView):
    model = Prescription
    fields = ['medication_name', 'dosage', 'instructions']
    template_name = 'doctor/add_prescription.html'
    

    def form_valid(self, form):
        doctor=self.request.user.doctor
        patient=get_object_or_404(Patient, id=self.kwargs['patient_id'])
        form.instance.doctor = doctor
        form.instance.patient = patient
        send_notification(doctor,patient,f"Dr.{doctor.name} given you a new prescription")
        return super().form_valid(form)

class PrescriptionDeleteView(LoginRequiredMixin,DoctorMixin,DeleteView): 
    model = Prescription 
    template_name = 'doctor/prescription_delete.html' 
    success_url = reverse_lazy('patient_list')
    

class PrescriptionUpdateView(LoginRequiredMixin, DoctorMixin, UpdateView):
    model = Prescription
    fields = ['medication_name', 'dosage', 'instructions']
    template_name = 'doctor/add_prescription.html'
    
    

    def form_valid(self, form):
        # Get the updated prescription object
        prescription = form.save()

        # Send notification for the updated prescription
        send_notification(
            prescription.doctor, 
            prescription.patient, 
            f"Dr. {prescription.doctor.name} has updated a prescription"
        )

        # Return the response for a valid form submission
        return super().form_valid(form)
