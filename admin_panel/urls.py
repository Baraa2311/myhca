from django.urls import path
from .views import (
    AdminHomeView, 
    ReviewDecisionView, 
    SubscriptionReviewView, 
    UserListView, 
    AddDoctorView, 
    AddPatientView, 
    UpdateDoctorView, 
    UpdatePatientView
)

urlpatterns = [
    # Admin views
    path('review/', SubscriptionReviewView.as_view(), name='subscription_review'),
    path('review/decision/', ReviewDecisionView.as_view(), name='review_decision'),
    
    # User management views
    path('users/', UserListView.as_view(), name='user_list'),
    
    # Add and Edit doctor and patient views
    path('add/doctor/', AddDoctorView.as_view(), name='add_doctor'),
    path('add/patient/', AddPatientView.as_view(), name='add_patient'),
    
    # Update views with more descriptive names and ID validation
    path('edit/doctor/<int:pk>/', UpdateDoctorView.as_view(), name='edit_doctor'),
    path('edit/patient/<int:pk>/', UpdatePatientView.as_view(), name='edit_patient'),
]