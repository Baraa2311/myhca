from django.conf import settings
from django.http import JsonResponse
from coms.models import Ad, MedicalAdvice

def get_ads_and_medical_advice(request):
    ads = list(Ad.objects.values())  # Convert queryset to a list of dictionaries
    medical_advice = []

    # Get the base URL for images from settings
    base_url = settings.STATICC_URL if hasattr(settings, 'STATICC_URL') else ''
    

    if request.user.is_authenticated:
        if hasattr(request.user, 'doctor'):
            medical_advice = list(MedicalAdvice.objects.filter(created_by=request.user).values())
        elif hasattr(request.user, 'patient'):
            medical_advice = list(MedicalAdvice.objects.filter(created_by__in=request.user.patient.doctors.all()).values())

    # Add the base URL to the image URLs in ads and medical advice
    for ad in ads:
        if ad.get('image'):
            ad['image'] = base_url + ad['image']
            

    for advice in medical_advice:
        if advice.get('image'):
            advice['image'] = base_url + advice['image']

    return JsonResponse({'ads': ads, 'medical_advice': medical_advice})