from django.contrib import admin
from .models import Grade


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'assignment_score', 'exam_score', 'total_score', 'grade', 'semester', 'year')
    search_fields = ('student__first_name', 'student__last_name', 'course__name', 'semester')
    list_filter = ('grade', 'semester', 'year', 'course')
    ordering = ('-year', '-semester', 'course', 'student')

