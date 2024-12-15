from django.urls import path
from .views import HomePageView, CustomLoginRedirectView

urlpatterns = [
    # Home page view
    path('', HomePageView.as_view(), name='home'),
    
    # Custom login redirect based on user type
    path('redirect/', CustomLoginRedirectView.as_view(), name='custom_login_redirect'),
]