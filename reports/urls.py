from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('attendance/', views.attendance_report, name='attendance_report'),
    path('grades/', views.grade_report, name='grade_report'),
    path('performance/', views.performance_report, name='performance_report'),
    path('enrollments/', views.enrollment_report, name='enrollment_report'),
]

