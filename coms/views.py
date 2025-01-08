from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import MedicalAdvice, Ad
from .forms import MedAdviceForm
import logging
from accounts.models import Doctor
# Initialize logger
logger = logging.getLogger(__name__)

class DoctorMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_doctor

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a doctor.")
        return redirect('home')
    

# Add Medical Advice
class AddAdviceView(LoginRequiredMixin, DoctorMixin, CreateView):
    model = MedicalAdvice
    form_class = MedAdviceForm
    template_name = 'notifications/add_med_advice.html'
    success_url = '/notifications/Advices/'

    

    def form_valid(self, form):
        advice = form.save(commit=False)
        advice.created_by = get_object_or_404(Doctor, id=self.request.user.id)
        print(advice.image)
        advice.save()
        return super().form_valid(form)

# Edit Medical Advice
class UpdateAdviceView(LoginRequiredMixin, DoctorMixin, UpdateView):
    model = MedicalAdvice
    form_class = MedAdviceForm
    template_name = 'notifications/edit_med_advice.html'
    success_url = '/notifications/Advices/'

    

# Delete Medical Advice
class DeleteAdviceView(LoginRequiredMixin, DoctorMixin, DeleteView):
    model = MedicalAdvice
    template_name = 'notifications/confirm_delete_advice.html'
    success_url = '/notifications/Advices/'

    


# List of Medical Advice
class MedAdviceListView(LoginRequiredMixin,DoctorMixin, ListView):
    model = MedicalAdvice
    template_name = 'notifications/advice_list.html'
    context_object_name = 'medical_advice'
    
    


