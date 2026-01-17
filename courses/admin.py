from django.contrib import admin
from .models import Course, Enrollment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'name', 'credits', 'teacher', 'semester', 'year', 'is_active')
    search_fields = ('course_code', 'name', 'teacher__username')
    list_filter = ('is_active', 'semester', 'year')
    ordering = ('course_code',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date', 'status', 'grade')
    search_fields = ('student__first_name', 'student__last_name', 'course__name')
    list_filter = ('status', 'course')
    ordering = ('-enrollment_date',)

