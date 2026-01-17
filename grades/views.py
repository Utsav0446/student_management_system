from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import models
from .models import Grade
from .forms import GradeForm


def grade_list(request):
    """Display list of all grades."""
    grades = Grade.objects.all()
    course_filter = request.GET.get('course')
    student_filter = request.GET.get('student')
    semester_filter = request.GET.get('semester')

    if course_filter:
        grades = grades.filter(course_id=course_filter)
    if student_filter:
        grades = grades.filter(student_id=student_filter)
    if semester_filter:
        grades = grades.filter(semester=semester_filter)

    courses = Course.objects.all()
    students = Student.objects.all()
    return render(request, 'grades/grade_list.html', {
        'grades': grades,
        'courses': courses,
        'students': students
    })


def grade_create(request):
    """Create a new grade record."""
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grade recorded successfully.')
            return redirect('grade_list')
    else:
        form = GradeForm()
    return render(request, 'grades/grade_form.html', {'form': form, 'title': 'Record Grade'})


def grade_update(request, pk):
    """Update an existing grade record."""
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grade updated successfully.')
            return redirect('grade_list')
    else:
        form = GradeForm(instance=grade)
    return render(request, 'grades/grade_form.html', {'form': form, 'title': 'Update Grade'})


def grade_delete(request, pk):
    """Delete a grade record."""
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        grade.delete()
        messages.success(request, 'Grade record deleted successfully.')
        return redirect('grade_list')
    return render(request, 'grades/grade_confirm_delete.html', {'grade': grade})


def grade_by_course(request, course_id):
    """Display grade records for a specific course."""
    course = get_object_or_404(Course, pk=course_id)
    grades = Grade.objects.filter(course=course).order_by('student')
    return render(request, 'grades/grade_by_course.html', {
        'course': course,
        'grades': grades
    })


def grade_by_student(request, student_id):
    """Display grade records for a specific student."""
    student = get_object_or_404(Student, pk=student_id)
    grades = Grade.objects.filter(student=student).order_by('-year', '-semester')
    return render(request, 'grades/grade_by_student.html', {
        'student': student,
        'grades': grades
    })


def student_report_card(request, student_id):
    """Generate a report card for a specific student."""
    student = get_object_or_404(Student, pk=student_id)
    grades = Grade.objects.filter(student=student).order_by('-year', '-semester')

    # Calculate GPA
    total_credits = 0
    total_grade_points = 0
    grade_point_map = {
        'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7,
        'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0,
        'D-': 0.7, 'F': 0.0
    }

    for grade in grades:
        if grade.grade and grade.course:
            gp = grade_point_map.get(grade.grade, 0)
            total_grade_points += gp * grade.course.credits
            total_credits += grade.course.credits

    gpa = total_grade_points / total_credits if total_credits > 0 else 0

    return render(request, 'grades/report_card.html', {
        'student': student,
        'grades': grades,
        'gpa': round(gpa, 2),
        'total_credits': total_credits
    })


# Import models at the bottom to avoid circular imports
from courses.models import Course
from students.models import Student

