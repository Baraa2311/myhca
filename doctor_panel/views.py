from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, UpdateView,DetailView
from django.views import View
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages
from accounts.models import Doctor, Patient, UserBase
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import logging
from django.contrib.auth.decorators import login_required
from medical_records.models import MedicalFile
# Setup logging
logger = logging.getLogger(__name__)

# Create your views here.
class PatientListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'doctor/patient_list.html'
    context_object_name = 'patients'

    def test_func(self):
        return self.request.user.is_doctor

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a patient.")
        return redirect('home')
        
    def get_queryset(self):
        return Patient.objects.filter(doctors__id=self.request.user.id)




class PatientDetailsView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Patient
    template_name = "doctor/patient_details.html"
    context_object_name = "patient"
    pk_url_kwarg = "patient_id"

    def test_func(self):
        return self.request.user.is_doctor or self.request.user.is_administrator

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a doctor or administrator.")
        return redirect("home")


class PatientRecordsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = MedicalFile
    template_name = "doctor/patient_records.html"
    context_object_name = "files"

    def test_func(self):
        return self.request.user.is_doctor or self.request.user.is_administrator

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a doctor or administrator.")
        return redirect("home")

    def get_queryset(self):
        return MedicalFile.objects.filter(patient_id=self.kwargs["patient_id"]).order_by("-uploaded_at")