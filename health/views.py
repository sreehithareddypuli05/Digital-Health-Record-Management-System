from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
import json
from .models import Patient, Doctor, HealthWorker, MedicalFile, Appointment

def index(request):
    """Serve the main HTML page"""
    return render(request, 'health/index.html')

@csrf_exempt
@require_http_methods(["POST"])
def register_patient(request):
    """Register a new patient"""
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        aadhar = data.get('aadhar', '').strip()
        email = data.get('email', '').strip()
        
        # Validation
        if not all([name, phone, aadhar]):
            return JsonResponse({'success': False, 'error': 'All required fields must be filled'})
        
        if len(phone) != 10 or not phone.isdigit():
            return JsonResponse({'success': False, 'error': 'Phone must be 10 digits'})
        
        if len(aadhar) != 12 or not aadhar.isdigit():
            return JsonResponse({'success': False, 'error': 'Aadhar must be 12 digits'})
        
        # Check if patient already exists
        if Patient.objects.filter(aadhar=aadhar).exists():
            return JsonResponse({'success': False, 'error': 'Patient with this Aadhar already exists'})
        
        # Create patient
        patient = Patient.objects.create(
            aadhar=aadhar,
            name=name,
            phone=phone,
            email=email if email else None
        )
        
        return JsonResponse({
            'success': True, 
            'message': 'Patient registered successfully',
            'patient_data': {
                'aadhar': patient.aadhar,
                'name': patient.name,
                'phone': patient.phone,
                'email': patient.email
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def login_patient(request):
    """Login patient by name and phone"""
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        
        if not all([name, phone]):
            return JsonResponse({'success': False, 'error': 'Name and phone are required'})
        
        patient = Patient.objects.get(name=name, phone=phone)
        
        return JsonResponse({
            'success': True,
            'patient_data': {
                'aadhar': patient.aadhar,
                'name': patient.name,
                'phone': patient.phone,
                'email': patient.email
            }
        })
        
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': 'Patient not found'})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def register_doctor(request):
    """Register a new doctor"""
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        specialization = data.get('specialization', '').strip()
        hospital = data.get('hospital', '').strip()
        
        if not all([name, hospital]):
            return JsonResponse({'success': False, 'error': 'Name and hospital are required'})
        
        doctor = Doctor.objects.create(
            name=name,
            specialization=specialization if specialization else 'General',
            hospital=hospital
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Doctor registered successfully! ID: {doctor.doctor_id}',
            'doctor_id': doctor.doctor_id,
            'doctor_data': {
                'id': doctor.doctor_id,
                'name': doctor.name,
                'specialization': doctor.specialization,
                'hospital': doctor.hospital
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def login_doctor(request):
    """Login doctor by ID"""
    try:
        data = json.loads(request.body)
        doctor_id = data.get('doctor_id', '').strip()
        
        if not doctor_id:
            return JsonResponse({'success': False, 'error': 'Doctor ID is required'})
        
        doctor = Doctor.objects.get(doctor_id=doctor_id)
        
        return JsonResponse({
            'success': True,
            'doctor_data': {
                'id': doctor.doctor_id,
                'name': doctor.name,
                'specialization': doctor.specialization,
                'hospital': doctor.hospital
            }
        })
        
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': 'Invalid Doctor ID'})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def register_worker(request):
    """Register a new health worker"""
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        
        if not all([name, phone]):
            return JsonResponse({'success': False, 'error': 'Name and phone are required'})
        
        if len(phone) != 10 or not phone.isdigit():
            return JsonResponse({'success': False, 'error': 'Phone must be 10 digits'})
        
        worker = HealthWorker.objects.create(
            name=name,
            phone=phone
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Health Worker registered successfully! ID: {worker.worker_id}',
            'worker_id': worker.worker_id,
            'worker_data': {
                'id': worker.worker_id,
                'name': worker.name,
                'phone': worker.phone
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def login_worker(request):
    """Login health worker by ID"""
    try:
        data = json.loads(request.body)
        worker_id = data.get('worker_id', '').strip()
        
        if not worker_id:
            return JsonResponse({'success': False, 'error': 'Worker ID is required'})
        
        worker = HealthWorker.objects.get(worker_id=worker_id)
        
        return JsonResponse({
            'success': True,
            'worker_data': {
                'id': worker.worker_id,
                'name': worker.name,
                'phone': worker.phone
            }
        })
        
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': 'Invalid Worker ID'})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def upload_file(request):
    """Upload medical file for a patient"""
    try:
        data = json.loads(request.body)
        patient_aadhar = data.get('patient_aadhar', '').strip()
        file_name = data.get('file_name', '').strip()
        file_data = data.get('file_data', '')
        file_type = data.get('file_type', '')
        file_size = data.get('file_size', 0)
        uploader_type = data.get('uploader_type', '')
        uploader_id = data.get('uploader_id', '')
        
        if not all([patient_aadhar, file_name, file_data, uploader_type]):
            return JsonResponse({'success': False, 'error': 'Required fields missing'})
        
        # Verify patient exists
        patient = Patient.objects.get(aadhar=patient_aadhar)
        
        # Create medical file record
        medical_file = MedicalFile.objects.create(
            patient=patient,
            file_name=file_name,
            file_data=file_data,
            file_type=file_type,
            file_size=file_size,
            uploader_type=uploader_type,
            uploader_id=uploader_id
        )
        
        return JsonResponse({
            'success': True,
            'message': 'File uploaded successfully',
            'file_id': str(medical_file.id)
        })
        
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': 'Patient not found'})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def book_appointment(request):
    """Book an appointment"""
    try:
        data = json.loads(request.body)
        patient_aadhar = data.get('patient_aadhar', '').strip()
        hospital = data.get('hospital', '').strip()
        doctor_name = data.get('doctor_name', '').strip()
        appointment_date = data.get('appointment_date', '').strip()
        appointment_time = data.get('appointment_time', '').strip()
        
        if not all([patient_aadhar, hospital, doctor_name, appointment_date, appointment_time]):
            return JsonResponse({'success': False, 'error': 'All fields are required'})
        
        # Verify patient exists
        patient = Patient.objects.get(aadhar=patient_aadhar)
        
        # Create appointment
        appointment = Appointment.objects.create(
            patient=patient,
            hospital=hospital,
            doctor_name=doctor_name,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        )
        
        return JsonResponse({
    'success': True,
    'message': 'Appointment booked successfully',
    'appointment_code': appointment.appointment_code,
    'appointment_data': {
        'code': appointment.appointment_code,
        'hospital': appointment.hospital,
        'doctor': appointment.doctor_name,
        'date': appointment.appointment_date,  # already string
        'time': appointment.appointment_time   # already string
    }


        })
        
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': 'Patient not found'})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@require_http_methods(["GET"])
def get_patient_files(request, aadhar):
    """Get all files for a patient"""
    try:
        patient = Patient.objects.get(aadhar=aadhar)
        files = MedicalFile.objects.filter(patient=patient).order_by('-uploaded_at')
        
        files_data = []
        for file in files:
            files_data.append({
                'id': str(file.id),
                'name': file.file_name,
                'type': file.file_type,
                'size': file.file_size,
                'uploader': f"{file.uploader_type}-{file.uploader_id}",
                'uploaded_at': file.uploaded_at.strftime('%Y-%m-%d %H:%M'),
                'data_url': file.file_data
            })
        
        return JsonResponse({
            'success': True,
            'files': files_data
        })
        
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': 'Patient not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@require_http_methods(["GET"])
def verify_patient_qr(request, aadhar):
    """Verify patient exists by Aadhar from QR scan"""
    try:
        patient = Patient.objects.get(aadhar=aadhar)
        
        return JsonResponse({
            'success': True,
            'patient_data': {
                'aadhar': patient.aadhar,
                'name': patient.name,
                'phone': patient.phone,
                'email': patient.email
            }
        })
        
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': 'Patient not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})