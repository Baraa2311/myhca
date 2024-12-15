from django.urls import path
from .views import UploadFileView, ShowFilesView

urlpatterns = [
    path('upload-medical-file/', UploadFileView.as_view(), name='upload_medical_file'),
    path('medical-files/', ShowFilesView.as_view(), name='view_medical_files'),
]