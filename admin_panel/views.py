from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.views import View
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages
from accounts.models import Doctor, Patient, UserBase
from accounts.forms import DoctorSignUpForm, PatientSignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import logging

# Setup logging
logger = logging.getLogger(__name__)


# Admin views
class AdminHomeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'homepages/admin_home.html'
    def test_func(self):
        return self.request.user.is_administrator

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a patient.")
        return redirect('home')
        

class SubscriptionReviewView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = UserBase
    template_name = 'admin/subscription_review.html'
    context_object_name = 'users'
    
    def test_func(self):
        return self.request.user.is_administrator

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a patient.")
        return redirect('home')
        

class ReviewDecisionView(LoginRequiredMixin, UserPassesTestMixin, View):
            
    def test_func(self):
            return self.request.user.is_administrator

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a patient.")
        return redirect('home')
        
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get("user_id")
        decision = request.POST.get("decision")

        if not user_id or not decision:
            return JsonResponse({"status": "error", "message": "Invalid data."}, status=400)

        user = get_object_or_404(UserBase, id=user_id)

        if decision == "accept":
            user.is_active = True
            user.save()
            logger.info(f"User {user.name} approved.")
            return JsonResponse({"status": "success", "message": f"User {user.name} approved."})

        elif decision == "decline":
            user.delete()
            logger.info(f"User {user.name} declined and removed.")
            return JsonResponse({"status": "success", "message": f"User {user.name} declined and removed."})

        return JsonResponse({"status": "error", "message": "Invalid decision."}, status=400)

class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'admin/user_list.html'
    context_object_name = 'doctors'

    def test_func(self):
        return self.request.user.is_administrator

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a patient.")
        return redirect('home')
        
    def get_queryset(self):
        return Doctor.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patients'] = Patient.objects.all()
        return context

# Create a new doctor (CreateView)
class AddDoctorView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Doctor
    form_class = DoctorSignUpForm
    template_name = 'admin/add_doctor.html'
    success_url = '/admin/users/'

    def test_func(self):
        return self.request.user.is_administrator

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a patient.")
        return redirect('home')
        

        

# Create a new patient (CreateView)
class AddPatientView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Patient
    form_class = PatientSignUpForm
    template_name = 'admin/add_patient.html'
    success_url = '/admin/users/'

    def test_func(self):
        return self.request.user.is_administrator

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a patient.")
        return redirect('home')
        
        
# Update an existing doctor (UpdateView)
class UpdateDoctorView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Doctor
    form_class = DoctorSignUpForm
    template_name = 'admin/edit_doctor.html'
    success_url = '/admin/users/'

    def test_func(self):
        return self.request.user.is_administrator

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a patient.")
        return redirect('home')
        

# Update an existing patient (UpdateView)
class UpdatePatientView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Patient
    form_class = PatientSignUpForm
    template_name = 'admin/edit_patient.html'
    success_url = '/admin/users/'
    
    def test_func(self):
        return self.request.user.is_administrator

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a patient.")
        return redirect('home')
        