from django.urls import path
from .views import PatientSignUpView, DoctorSignUpView, RegistrationPendingView, DoctorHomeView, PatientHomeView,ProfileDetailView, ProfileUpdateView,MarkAllNotificationsReadView
from . import views





urlpatterns = [
    # Your other URL patterns
    path('notifications/read-all/', MarkAllNotificationsReadView.as_view(), name='notifications_read_all'),

    path('profile/', ProfileDetailView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),

    # Registration URLs
    path('doctor/signup/', DoctorSignUpView.as_view(), name='doctor_signup'),
    path('patient/signup/', PatientSignUpView.as_view(), name='patient_signup'),
    
    
    # Registration Pending URL
    path('registration-pending/', RegistrationPendingView.as_view(), name='registration_pending'),
    
    # Home Pages
    path('doctor/', DoctorHomeView.as_view(), name='doctor_home'),
    path('patient/', PatientHomeView.as_view(), name='patient_home'),
    
    
    # Select Doctor URL
    path("select_doctor/", views.select_doctor, name="select_doctor"),
    path("doctor_requests/", views.doctor_requests, name="doctor_requests"),
    path("delete_doctor/", views.delete_doctor, name="delete_doctor"),
    path("doctor_details/<int:doctor_id>/", views.doctor_details, name="doctor_details"),
    
    
    # Appointment Times URL
    path('select-doctor/appointments/<int:doctor_id>/times/', views.get_appointment_times, name='get_appointment_times'),
]