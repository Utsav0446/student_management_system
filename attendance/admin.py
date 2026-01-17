from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'status', 'remarks')
    search_fields = ('student__first_name', 'student__last_name', 'course__name', 'date')
    list_filter = ('status', 'date', 'course')
    ordering = ('-date', 'student')
    date_hierarchy = 'date'

