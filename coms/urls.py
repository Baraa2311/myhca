from django.urls import path
from .views import (
    AddAdviceView,
    UpdateAdviceView,
    MedAdviceListView,
    DeleteAdviceView,
    
)

urlpatterns = [
    # Medical Advice URLs
    path('Advices/', MedAdviceListView.as_view(), name='advice_list'),
    path('add/advice/', AddAdviceView.as_view(), name='add_advice'),
    path('edit/advice/<int:pk>/', UpdateAdviceView.as_view(), name='edit_advice'),
    path('delete/advice/<int:pk>/', DeleteAdviceView.as_view(), name='delete_advice'),
]