from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, UpdateView,DetailView
from django.views import View
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages
from accounts.models import Doctor, Patient, UserBase,DoctorPatient
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import logging
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from medical_records.models import MedicalFile
# Setup logging
logger = logging.getLogger(__name__)


class DoctorMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_doctor

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a doctor.")
        return redirect('home')




class PatientListView(LoginRequiredMixin, DoctorMixin, ListView):
    template_name = 'doctor/patient_list.html'
    context_object_name = 'patients'

    def get_queryset(self):
        return Patient.objects.filter(
            doctor_relationships__doctor=self.request.user,
            doctor_relationships__status=DoctorPatient.Status.ACCEPTED
        )




class PatientDetailsView(LoginRequiredMixin, DoctorMixin, DetailView):
    model = Patient
    template_name = "doctor/patient_details.html"
    context_object_name = "patient"
    pk_url_kwarg = "patient_id"



class PatientRecordsView(LoginRequiredMixin, DoctorMixin, ListView):
    model = MedicalFile
    template_name = "doctor/patient_records.html"
    context_object_name = "files"

    def get_queryset(self):
        return MedicalFile.objects.filter(patient_id=self.kwargs["patient_id"]).order_by("-uploaded_at")