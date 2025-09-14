from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class Patient(models.Model):
    aadhar = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.aadhar}"

class Doctor(models.Model):
    SPECIALIZATIONS = [
        ('General', 'General'),
        ('Cardiology', 'Cardiology'),
        ('Orthopedics', 'Orthopedics'),
        ('Pediatrics', 'Pediatrics'),
        ('Dermatology', 'Dermatology'),
        ('Neurology', 'Neurology'),
        ('ENT', 'ENT'),
        ('Endocrinology', 'Endocrinology'),
        ('Gastroenterology', 'Gastroenterology'),
        ('Nephrology', 'Nephrology'),
        ('Oncology', 'Oncology'),
        ('Radiology', 'Radiology'),
        ('Urology', 'Urology'),
        ('Hematology', 'Hematology'),
        ('Dentistry', 'Dentistry'),
        ('Anesthesiology', 'Anesthesiology'),
        ('Psychiatry', 'Psychiatry'),
        ('Pulmonology', 'Pulmonology'),
        ('Rheumatology', 'Rheumatology'),
    ]
    
    doctor_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATIONS)
    hospital = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.doctor_id:
            import random
            while True:
                new_id = f"DOC{random.randint(1000, 9999)}"
                if not Doctor.objects.filter(doctor_id=new_id).exists():
                    self.doctor_id = new_id
                    break
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"

class HealthWorker(models.Model):
    worker_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.worker_id:
            import random
            while True:
                new_id = f"WRK{random.randint(1000, 9999)}"
                if not HealthWorker.objects.filter(worker_id=new_id).exists():
                    self.worker_id = new_id
                    break
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} - {self.worker_id}"

class MedicalFile(models.Model):
    UPLOADER_TYPES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('worker', 'Health Worker'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_files')
    file_name = models.CharField(max_length=255)
    file_data = models.TextField()  # Base64 encoded file data
    file_type = models.CharField(max_length=50)
    file_size = models.IntegerField()
    uploader_type = models.CharField(max_length=10, choices=UPLOADER_TYPES)
    uploader_id = models.CharField(max_length=20)  # Doctor ID or Worker ID
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.file_name} - {self.patient.name}"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    appointment_code = models.CharField(max_length=10, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    hospital = models.CharField(max_length=200)
    doctor_name = models.CharField(max_length=100)
    appointment_date = models.DateField()
    appointment_time = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.appointment_code:
            import random
            while True:
                new_code = f"APT{random.randint(100000, 999999)}"
                if not Appointment.objects.filter(appointment_code=new_code).exists():
                    self.appointment_code = new_code
                    break
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.appointment_code} - {self.patient.name} with {self.doctor_name}"