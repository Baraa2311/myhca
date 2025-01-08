# context_processors.py
from coms.models import Ad, MedicalAdvice

def common_data(request):
    ads = Ad.objects.all()  # Retrieve all ads (modify as needed)
    
    medical_advice = None
    if request.user.is_authenticated:
        if hasattr(request.user, 'doctor'):  # Check if the user is a doctor
            # Retrieve all medical advice created by the doctor
            medical_advice = MedicalAdvice.objects.filter(created_by=request.user)
        elif hasattr(request.user, 'patient'):  # Check if the user is a patient
            # Retrieve all medical advice created by the patient's doctors
            medical_advice = MedicalAdvice.objects.filter(created_by__in=request.user.patient.doctors.all())

    return {
        'ads': ads,
        'medical_advice': medical_advice
    }