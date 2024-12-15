from django.urls import path
from . import views




urlpatterns = [
    # Other paths...
    path("delete_appointment/", views.delete_appointment, name="delete_appointment"),

    # Other paths
    path('api/slots/<int:doctor_id>/', views.get_available_slots_api, name='get_available_slots'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
]