from django.urls import path
from . import views

app_name = 'health'

urlpatterns = [
    path('', views.index, name='index'),
    
    # Patient endpoints
    path('api/register-patient/', views.register_patient, name='register_patient'),
    path('api/login-patient/', views.login_patient, name='login_patient'),
    path('api/patient-files/<str:aadhar>/', views.get_patient_files, name='get_patient_files'),
    path('api/verify-patient/<str:aadhar>/', views.verify_patient_qr, name='verify_patient_qr'),
    
    # Doctor endpoints
    path('api/register-doctor/', views.register_doctor, name='register_doctor'),
    path('api/login-doctor/', views.login_doctor, name='login_doctor'),
    
    # Health Worker endpoints
    path('api/register-worker/', views.register_worker, name='register_worker'),
    path('api/login-worker/', views.login_worker, name='login_worker'),
    
    # File and appointment endpoints
    path('api/upload-file/', views.upload_file, name='upload_file'),
    path('api/book-appointment/', views.book_appointment, name='book_appointment'),
]