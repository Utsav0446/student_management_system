from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_list, name='attendance_list'),
    path('create/', views.attendance_create, name='attendance_create'),
    path('<int:pk>/update/', views.attendance_update, name='attendance_update'),
    path('<int:pk>/delete/', views.attendance_delete, name='attendance_delete'),
    path('course/<int:course_id>/', views.attendance_by_course, name='attendance_by_course'),
    path('student/<int:student_id>/', views.attendance_by_student, name='attendance_by_student'),
]

