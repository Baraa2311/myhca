from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
import logging

# Set up logger for error handling
logger = logging.getLogger(__name__)

class CustomLoginRedirectView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_type = request.user.user_type
        


        # Dictionary for user type redirection
        redirect_map = {
            'patient': 'patient_home',
            'doctor': 'doctor_home',
            'admin': 'admin:index'
        }

        # Redirect to the corresponding view based on the user type
        
        if user_type in redirect_map:
            return redirect(redirect_map[user_type])
        else:
            # Log if the user type is unexpected
            logger.warning(f"Unexpected user type: {user_type} for user {request.user.id}")
            return redirect('home')  # Default redirect

class HomePageView(TemplateView):
    template_name = 'Home.html'