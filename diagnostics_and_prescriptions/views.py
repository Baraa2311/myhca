from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from accounts.models import Patient
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DetailView, ListView,DeleteView
from .models import Diagnostic, Prescription
from django.urls import reverse_lazy

class DiagnosticListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    
    model = Diagnostic
    template_name = "doctor/patient_diagnostics.html"
    context_object_name = "diagnosis"

    def test_func(self):
        return self.request.user.is_doctor or self.request.user.is_patient

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a doctor")
        return redirect("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient_id'] = self.kwargs["patient_id"]
        return context
        
    def get_queryset(self):
        return Diagnostic.objects.filter(patient_id=self.kwargs["patient_id"])


class PrescriptionListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Prescription
    template_name = "doctor/patient_prescriptions.html"
    context_object_name = "prescriptions"

    def test_func(self):
        return self.request.user.is_doctor or self.request.user.is_patient

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a doctor")
        return redirect("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient_id'] = self.kwargs["patient_id"]
        return context
        
    def get_queryset(self):
        return Prescription.objects.filter(patient_id=self.kwargs["patient_id"])
        

# Mixin to ensure only doctors can access certain views
class DoctorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, 'doctor')  # Checks if the user is a doctor


# Diagnostic Views
class DiagnosticCreateView(LoginRequiredMixin, DoctorRequiredMixin, CreateView):
    model = Diagnostic
    fields = ['test_name', 'test_results']  # Exclude patient and doctor fields
    template_name = 'doctor/add_diagnostic.html'  
    def form_valid(self, form): 
        form.instance.doctor = self.request.user.doctor  # Assign the logged-in doctor
        form.instance.patient = get_object_or_404(Patient, id=self.kwargs['patient_id'])  # Get the patient from URL
        return super().form_valid(form)

class DiagnosticDeleteView(DeleteView): 
    model = Diagnostic 
    template_name = 'doctor/diagnostic_delete.html' 
    success_url = reverse_lazy('patient_list')


class DiagnosticUpdateView(LoginRequiredMixin, DoctorRequiredMixin, UpdateView):
    model = Diagnostic
    fields = ['test_name', 'test_results']
    template_name = 'doctor/add_diagnostic.html'

    def get_queryset(self):
        return Diagnostic.objects.filter(doctor=self.request.user.doctor)  # Restrict to diagnostics created by the doctor


# Prescription Views
class PrescriptionCreateView(LoginRequiredMixin, DoctorRequiredMixin, CreateView):
    model = Prescription
    fields = ['medication_name', 'dosage', 'instructions']
    template_name = 'doctor/add_prescription.html'
    

    def form_valid(self, form):
        form.instance.doctor = self.request.user.doctor
        form.instance.patient = get_object_or_404(Patient, id=self.kwargs['patient_id'])
        return super().form_valid(form)

class PrescriptionDeleteView(DeleteView): 
    model = Prescription 
    template_name = 'doctor/prescription_delete.html' 
    success_url = reverse_lazy('patient_list')
    

class PrescriptionUpdateView(LoginRequiredMixin, DoctorRequiredMixin, UpdateView):
    model = Prescription
    fields = ['medication_name', 'dosage', 'instructions']
    template_name = 'doctor/add_prescription.html'
    def get_queryset(self):
        return Prescription.objects.filter(doctor=self.request.user.doctor)

