from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import MedicalAdvice, Ad
from .forms import MedAdviceForm, AdsForm
import logging
from accounts.models import Doctor
# Initialize logger
logger = logging.getLogger(__name__)

# Add Medical Advice
class AddAdviceView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = MedicalAdvice
    form_class = MedAdviceForm
    template_name = 'notifications/add_med_advice.html'
    success_url = '/notifications/Advices/'

    def test_func(self):
        return self.request.user.is_doctor

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a doctor.")
        return redirect('home')

    def form_valid(self, form):
        advice = form.save(commit=False)
        advice.created_by = get_object_or_404(Doctor, id=self.request.user.id)
        advice.save()
        return super().form_valid(form)

# Edit Medical Advice
class UpdateAdviceView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MedicalAdvice
    form_class = MedAdviceForm
    template_name = 'notifications/edit_med_advice.html'
    success_url = '/notifications/Advices/'

    def test_func(self):
        return self.request.user.is_doctor

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a doctor.")
        return redirect('home')

# Delete Medical Advice
class DeleteAdviceView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MedicalAdvice
    template_name = 'notifications/confirm_delete_advice.html'
    success_url = '/notifications/Advices/'

    def test_func(self):
        return self.request.user.is_doctor

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a doctor.")
        return redirect('home')


# List of Medical Advice
class MedAdviceListView(LoginRequiredMixin, ListView):
    model = MedicalAdvice
    template_name = 'notifications/advice_list.html'
    context_object_name = 'medical_advice'


# Add Ad
class AddAdView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Ad
    form_class = AdsForm
    template_name = 'notifications/add_ad.html'
    success_url = '/notifications/Ads/'

    def test_func(self):
        return self.request.user.is_doctor

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a doctor.")
        return redirect('home')

# Edit Ad
class UpdateAdView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ad
    form_class = AdsForm
    template_name = 'notifications/edit_ad.html'
    success_url = '/notifications/Ads/'

    def test_func(self):
        return self.request.user.is_doctor

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a doctor.")
        return redirect('home')

# Delete Ad
class DeleteAdView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ad
    template_name = 'notifications/confirm_delete_ad.html'
    success_url = '/notifications/Ads/'

    def test_func(self):
        return self.request.user.is_doctor

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a doctor.")
        return redirect('home')


# List of Ads
class AdsListView(LoginRequiredMixin, ListView):
    model = Ad
    template_name = 'notifications/ad_list.html'
    context_object_name = 'ads'