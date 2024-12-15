from django.urls import path
from .views import AdminSignUpView, PatientSignUpView, DoctorSignUpView, RegistrationPendingView, DoctorHomeView, PatientHomeView,AdminHomeView,ProfileDetailView, ProfileUpdateView
from . import views



urlpatterns = [
    path('profile/', ProfileDetailView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),

    # Registration URLs
    path('doctor/signup/', DoctorSignUpView.as_view(), name='doctor_signup'),
    path('patient/signup/', PatientSignUpView.as_view(), name='patient_signup'),
    path('admin/signup/', AdminSignUpView.as_view(), name='admin_signup'),
    
    # Registration Pending URL
    path('registration-pending/', RegistrationPendingView.as_view(), name='registration_pending'),
    
    # Home Pages
    path('doctor/', DoctorHomeView.as_view(), name='doctor_home'),
    path('patient/', PatientHomeView.as_view(), name='patient_home'),
    path('admin/', AdminHomeView.as_view(), name='admin_home'),
    
    # Select Doctor URL
    path("select_doctor/", views.select_doctor, name="select_doctor"),
    path("doctor_requests/", views.doctor_requests, name="doctor_requests"),
    path("delete_doctor/<int:doctor_id>/", views.delete_doctor, name="delete_doctor"),
    path("doctor_details/<int:doctor_id>/", views.doctor_details, name="doctor_details"),
    
    
    # Appointment Times URL
    path('select-doctor/appointments/<int:doctor_id>/times/', views.get_appointment_times, name='get_appointment_times'),
]