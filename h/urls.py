
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('allauth.urls')),
    path('super/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('clinic.urls')),    
    path('doctor/', include('doctor_panel.urls')), 
     
    path('', include('clinic.urls')),    
    path('doctor/', include('diagnostics_and_prescriptions.urls')),
    
    path('notifications/', include('coms.urls')),
    
    path('records/', include('medical_records.urls')),    
    path('', include('appointments.urls')),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
