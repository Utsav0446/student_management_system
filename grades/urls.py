from django.urls import path
from . import views

urlpatterns = [
    path('', views.grade_list, name='grade_list'),
    path('create/', views.grade_create, name='grade_create'),
    path('<int:pk>/update/', views.grade_update, name='grade_update'),
    path('<int:pk>/delete/', views.grade_delete, name='grade_delete'),
    path('course/<int:course_id>/', views.grade_by_course, name='grade_by_course'),
    path('student/<int:student_id>/', views.grade_by_student, name='grade_by_student'),
    path('report-card/<int:student_id>/', views.student_report_card, name='student_report_card'),
]

