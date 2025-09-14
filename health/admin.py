from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Patient, Doctor, HealthWorker, MedicalFile, Appointment

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'aadhar', 'phone', 'email', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'aadhar', 'phone', 'email']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'aadhar', 'phone', 'email')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'doctor_id', 'specialization', 'hospital', 'created_at']
    list_filter = ['specialization', 'hospital', 'created_at']
    search_fields = ['name', 'doctor_id', 'hospital']
    readonly_fields = ['doctor_id', 'created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Doctor Information', {
            'fields': ('doctor_id', 'name', 'specialization', 'hospital')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(HealthWorker)
class HealthWorkerAdmin(admin.ModelAdmin):
    list_display = ['name', 'worker_id', 'phone', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'worker_id', 'phone']
    readonly_fields = ['worker_id', 'created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Worker Information', {
            'fields': ('worker_id', 'name', 'phone')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(MedicalFile)
class MedicalFileAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'patient', 'uploader_type', 'uploader_id', 'file_size', 'uploaded_at']
    list_filter = ['uploader_type', 'file_type', 'uploaded_at']
    search_fields = ['file_name', 'patient__name', 'patient__aadhar', 'uploader_id']
    readonly_fields = ['id', 'uploaded_at']
    ordering = ['-uploaded_at']
    
    fieldsets = (
        ('File Information', {
            'fields': ('file_name', 'file_type', 'file_size', 'patient')
        }),
        ('Upload Details', {
            'fields': ('uploader_type', 'uploader_id', 'uploaded_at')
        }),
        ('File Data', {
            'fields': ('file_data',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('patient')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['appointment_code', 'patient', 'doctor_name', 'hospital', 'appointment_date', 'appointment_time', 'status', 'created_at']
    list_filter = ['status', 'appointment_date', 'hospital', 'created_at']
    search_fields = ['appointment_code', 'patient__name', 'doctor_name', 'hospital']
    readonly_fields = ['appointment_code', 'created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Appointment Details', {
            'fields': ('appointment_code', 'patient', 'hospital', 'doctor_name')
        }),
        ('Schedule', {
            'fields': ('appointment_date', 'appointment_time', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('patient')

# Customize admin site headers
admin.site.site_header = "Digital Health Record Management"
admin.site.site_title = "Health Portal Admin"
admin.site.index_title = "Welcome to Health Portal Administration"