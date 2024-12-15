from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from datetime import datetime
import json
from accounts.models import Doctor,Patient,DoctorSchedule
from .models import Appointment
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def delete_appointment(request):
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            appointment_id = data.get("appointment_id")
            if not appointment_id:
                return JsonResponse({"error": "Invalid appointment ID"}, status=400)

            # Assuming Appointment is the model for appointments
            from .models import Appointment
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.delete()
            return JsonResponse({"message": "Appointment deleted successfully!"})
        except Appointment.DoesNotExist:
            return JsonResponse({"error": "Appointment not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)



def get_available_slots_api(request, doctor_id):
    # Get the date from the query parameter
    date_str = request.GET.get('date')
    
    if not date_str:
        return JsonResponse({'error': 'Date is required'}, status=400)

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    # Get the doctor object
    print(doctor_id)
    doctor = get_object_or_404(Doctor, id=doctor_id)
    

    # Get the schedule for the doctor on the specified date
    schedule = DoctorSchedule.objects.filter(doctor=doctor,day_of_week=str(date.strftime('%A'))).first()
    
    available_slots=[]
    
    if  schedule:
         # Get the available slots
        available_slots = schedule.get_available_slots(date)

   

    # Return available time slots
    return JsonResponse({'slots': available_slots})

def book_appointment(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            doctor_id = data.get('doctor_id')
            date_str = data.get('date')  # Date in "YYYY-MM-DD" format
            time_str = data.get('time')  # Time in "HH:MM" format
            
            # Validate input
            if not all([doctor_id, date_str, time_str]):
                return JsonResponse({'error': 'Missing required fields.'}, status=400)
                

            # Convert date and time strings to datetime objects
            try:
                appointment_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                appointment_time = datetime.strptime(time_str, "%H:%M:%S").time()
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'Invalid date or time format.'}, status=400)

            # Retrieve doctor and patient
            doctor = get_object_or_404(Doctor, id=doctor_id)
            patient = get_object_or_404(Patient, id=request.user.id)
            
            
            # Create the appointment
            appointment = Appointment.objects.create(
                doctor=doctor,
                date=appointment_date,
                time=appointment_time,
                patient=patient
            )

            return JsonResponse({
                'message': 'Appointment booked successfully!',
                'appointment': {
                    'id': appointment.id,
                    'doctor': doctor.name,
                    'date': str(appointment_date),
                    'time': str(appointment_time),
                    
                }
            }, status=201)

        except Exception as e:
            
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)