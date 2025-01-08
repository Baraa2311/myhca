from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import MedicalFileUploadForm
from .models import MedicalFile
from django.views.generic import CreateView, ListView
from django.shortcuts import get_object_or_404
from accounts.models import Patient
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class PatientMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_patient

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a patient.")
        return redirect('home')
        
class UploadFileView(LoginRequiredMixin, PatientMixin, CreateView):
    template_name = 'patient/upload_medical_files.html'
    form_class = MedicalFileUploadForm
    success_url = reverse_lazy('view_medical_files')  # Use reverse_lazy to dynamically resolve the URL

        
    def form_valid(self, form):
        medical_file = form.save(commit=False)
        medical_file.patient =get_object_or_404(Patient, id=self.request.user.id)
        
        # Perform additional validations or logic here if necessary
        try:
            medical_file.save()
        except ValidationError as e:
            form.add_error(None, str(e))  # Add error to the form if there is an issue during file save
            return self.form_invalid(form)
        
        return redirect(self.success_url)


class ShowFilesView(LoginRequiredMixin, PatientMixin, ListView):
    template_name = 'patient/view_medical_files.html'
    context_object_name = 'files'
        
    def get_queryset(self):
        # Ensure that we're only retrieving the files for the current authenticated user
        return MedicalFile.objects.filter(patient=self.request.user).order_by('-uploaded_at')  # Sort files by upload date (newest first)