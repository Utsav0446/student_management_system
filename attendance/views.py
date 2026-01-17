from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import models
from .models import Attendance
from .forms import AttendanceForm


def attendance_list(request):
    """Display list of all attendance records."""
    attendances = Attendance.objects.all()
    course_filter = request.GET.get('course')
    student_filter = request.GET.get('student')
    date_filter = request.GET.get('date')

    if course_filter:
        attendances = attendances.filter(course_id=course_filter)
    if student_filter:
        attendances = attendances.filter(student_id=student_filter)
    if date_filter:
        attendances = attendances.filter(date=date_filter)

    courses = Course.objects.all()
    students = Student.objects.all()
    return render(request, 'attendance/attendance_list.html', {
        'attendances': attendances,
        'courses': courses,
        'students': students
    })


def attendance_create(request):
    """Create a new attendance record."""
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance recorded successfully.')
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'attendance/attendance_form.html', {'form': form, 'title': 'Record Attendance'})


def attendance_update(request, pk):
    """Update an existing attendance record."""
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance updated successfully.')
            return redirect('attendance_list')
    else:
        form = AttendanceForm(instance=attendance)
    return render(request, 'attendance/attendance_form.html', {'form': form, 'title': 'Update Attendance'})


def attendance_delete(request, pk):
    """Delete an attendance record."""
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        attendance.delete()
        messages.success(request, 'Attendance record deleted successfully.')
        return redirect('attendance_list')
    return render(request, 'attendance/attendance_confirm_delete.html', {'attendance': attendance})


def attendance_by_course(request, course_id):
    """Display attendance records for a specific course."""
    course = get_object_or_404(Course, pk=course_id)
    attendances = Attendance.objects.filter(course=course).order_by('-date')
    return render(request, 'attendance/attendance_by_course.html', {
        'course': course,
        'attendances': attendances
    })


def attendance_by_student(request, student_id):
    """Display attendance records for a specific student."""
    student = get_object_or_404(Student, pk=student_id)
    attendances = Attendance.objects.filter(student=student).order_by('-date')
    return render(request, 'attendance/attendance_by_student.html', {
        'student': student,
        'attendances': attendances
    })


# Import models at the bottom to avoid circular imports
from courses.models import Course
from students.models import Student

