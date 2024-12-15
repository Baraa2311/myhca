from django.shortcuts import render
from .models import Ad,MedicalAdvice
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from .forms import AdsForm,MedAdviceForm
from accounts.models import Administrator,Doctor
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class AdsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Ad
    template_name = 'notifications/ad_list.html'
    context_object_name = 'ads'
    
    def test_func(self):
        return self.request.user.is_administrator

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a patient.")
        return redirect('home')
        
   
    

class AddAdView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Ad
    form_class = AdsForm
    template_name = 'admin/add_ad.html'
    success_url = '/notifications/Ads/'
    def form_valid(self, form):
        ad = form.save(commit=False)
        ad.created_by = get_object_or_404(Administrator, id=self.request.user.id)
        ad.save()

    def test_func(self):
        return self.request.user.is_administrator

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a patient.")
        return redirect('home')
        
    


class UpdateAdView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ad
    form_class = AdsForm
    template_name = 'admin/edit_ad.html'
    success_url = '/notifications/Ads/'
    
    def test_func(self):
        return self.request.user.is_administrator

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a patient.")
        return redirect('home')
        



class MedAdviceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = MedicalAdvice
    template_name = 'notifications/med_advice_list.html'
    context_object_name = 'advices'    
    
    def test_func(self):
        return self.request.user.is_doctor

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a patient.")
        return redirect('home')
        
    
    
class AddAdviceView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = MedicalAdvice
    form_class = MedAdviceForm
    template_name = 'notifications/add_med_advice.html'
    success_url = '/notifications/Advices/'
    
    def test_func(self):
        return self.request.user.is_doctor

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a patient.")
        return redirect('home')
        
    def form_valid(self, form):
        advice = form.save(commit=False)
        advice.created_by = get_object_or_404(Doctor, id=self.request.user.id)
        advice.save()

    


class UpdateAdviceView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MedicalAdvice
    form_class = MedAdviceForm
    template_name = 'notifications/edit_med_advice.html'
    success_url = '/notifications/Advices/'
    
    def test_func(self):
        return self.request.user.is_doctor

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a patient.")
        return redirect('home')
        