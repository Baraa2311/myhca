from django.urls import path
from .views import (DiagnosticListView,PrescriptionListView,
    DiagnosticCreateView, DiagnosticUpdateView,
    PrescriptionCreateView, PrescriptionUpdateView
    ,DiagnosticDeleteView,PrescriptionDeleteView
)


urlpatterns = [
    path("patients/<int:patient_id>/diagnostics/", DiagnosticListView.as_view(), name='patient_diagnostics'),
    path("patients/<int:patient_id>/prescriptions/", PrescriptionListView.as_view(), name='patient_prescriptions'),
       # Diagnostics
       path('diagnostics/<int:pk>/delete/', DiagnosticDeleteView.as_view(), name='diagnostic_delete'),
    path('diagnostics/create/<int:patient_id>/', DiagnosticCreateView.as_view(), name='diagnostic_create'),
    path('diagnostics/update/<int:pk>/', DiagnosticUpdateView.as_view(), name='diagnostic_update'),
    

    # Prescriptions
    path('prescriptions/<int:pk>/delete/', PrescriptionDeleteView.as_view(), name='prescription_delete'),
    path('prescriptions/create/<int:patient_id>/', PrescriptionCreateView.as_view(), name='prescription_create'),
    path('prescriptions/update/<int:pk>/', PrescriptionUpdateView.as_view(), name='prescription_update'),
    
]