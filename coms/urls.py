from django.urls import path
from .views import (
    AddAdviceView,
    UpdateAdviceView,
    MedAdviceListView,
    UpdateAdView,
    AddAdView,
    AdsListView,
    DeleteAdviceView,
    DeleteAdView
)

urlpatterns = [
    # Medical Advice URLs
    path('Advices/', MedAdviceListView.as_view(), name='advice_list'),
    path('add/advice/', AddAdviceView.as_view(), name='add_advice'),
    path('edit/advice/<int:pk>/', UpdateAdviceView.as_view(), name='edit_advice'),
    path('delete/advice/<int:pk>/', DeleteAdviceView.as_view(), name='delete_advice'),

    # Ad URLs
    path('Ads/', AdsListView.as_view(), name='ad_list'),
    path('add/ads/', AddAdView.as_view(), name='add_ads'),
    path('edit/ads/<int:pk>/', UpdateAdView.as_view(), name='edit_ads'),
    path('delete/ad/<int:pk>/', DeleteAdView.as_view(), name='delete_ad'),
]