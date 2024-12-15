from django.urls import path
from .views import PatientListView, PatientDetailsView, PatientRecordsView

urlpatterns = [
    path("patients/", PatientListView.as_view(), name="patient_list"),
    path("patients/<int:patient_id>/details/", PatientDetailsView.as_view(), name="patient_details"),
    path("patients/<int:patient_id>/records/", PatientRecordsView.as_view(), name="patient_records"),
]