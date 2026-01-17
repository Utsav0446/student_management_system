from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import models
from .models import Course, Enrollment
from .forms import CourseForm, EnrollmentForm


def course_list(request):
    """Display list of all courses."""
    courses = Course.objects.all()
    search_query = request.GET.get('q')
    if search_query:
        courses = courses.filter(
            models.Q(course_code__icontains=search_query) |
            models.Q(name__icontains=search_query)
        )
    return render(request, 'courses/course_list.html', {'courses': courses})


def course_create(request):
    """Create a new course."""
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course created successfully.')
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Create Course'})


def course_update(request, pk):
    """Update an existing course."""
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully.')
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Update Course'})


def course_delete(request, pk):
    """Delete a course."""
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully.')
        return redirect('course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})


def course_detail(request, pk):
    """Display course details with enrolled students."""
    course = get_object_or_404(Course, pk=pk)
    enrollments = Enrollment.objects.filter(course=course, status='active')
    return render(request, 'courses/course_detail.html', {'course': course, 'enrollments': enrollments})


def enrollment_list(request):
    """Display list of all enrollments."""
    enrollments = Enrollment.objects.all()
    return render(request, 'courses/enrollment_list.html', {'enrollments': enrollments})


def enrollment_create(request):
    """Create a new enrollment."""
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student enrolled successfully.')
            return redirect('enrollment_list')
    else:
        form = EnrollmentForm()
    return render(request, 'courses/enrollment_form.html', {'form': form, 'title': 'Enroll Student'})


def enrollment_delete(request, pk):
    """Delete an enrollment."""
    enrollment = get_object_or_404(Enrollment, pk=pk)
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Enrollment deleted successfully.')
        return redirect('enrollment_list')
    return render(request, 'courses/enrollment_confirm_delete.html', {'enrollment': enrollment})

