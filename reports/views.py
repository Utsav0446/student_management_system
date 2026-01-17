from django.shortcuts import render
from django.db import models
from django.db.models import Avg, Count
from students.models import Student
from courses.models import Course, Enrollment
from attendance.models import Attendance
from grades.models import Grade


def dashboard(request):
    """Display dashboard with overview statistics."""
    total_students = Student.objects.filter(is_active=True).count()
    total_courses = Course.objects.filter(is_active=True).count()
    total_enrollments = Enrollment.objects.filter(status='active').count()
    total_attendance_records = Attendance.objects.count()
    total_grade_records = Grade.objects.count()

    # Recent students
    recent_students = Student.objects.filter(is_active=True).order_by('-enrollment_date')[:5]

    # Courses with most enrollments
    popular_courses = Course.objects.filter(is_active=True).annotate(
        enrollment_count=Count('enrollments')
    ).order_by('-enrollment_count')[:5]

    # Average attendance rate
    attendance_stats = Attendance.objects.aggregate(
        present=Count('id', filter=models.Q(status='present')),
        absent=Count('id', filter=models.Q(status='absent')),
        late=Count('id', filter=models.Q(status='late'))
    )
    total_attendance = attendance_stats['present'] + attendance_stats['absent'] + attendance_stats['late']
    attendance_rate = (attendance_stats['present'] / total_attendance * 100) if total_attendance > 0 else 0

    return render(request, 'reports/dashboard.html', {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
        'total_attendance_records': total_attendance_records,
        'total_grade_records': total_grade_records,
        'recent_students': recent_students,
        'popular_courses': popular_courses,
        'attendance_rate': round(attendance_rate, 2),
    })


def attendance_report(request):
    """Generate attendance report."""
    courses = Course.objects.filter(is_active=True)
    course_id = request.GET.get('course')

    if course_id:
        course = get_object_or_404(Course, pk=course_id)
        attendances = Attendance.objects.filter(course=course).order_by('-date')
    else:
        attendances = Attendance.objects.all().order_by('-date')[:100]
        course = None

    # Calculate attendance statistics
    if course:
        stats = attendances.aggregate(
            present=Count('id', filter=models.Q(status='present')),
            absent=Count('id', filter=models.Q(status='absent')),
            late=Count('id', filter=models.Q(status='late'))
        )
    else:
        stats = {'present': 0, 'absent': 0, 'late': 0}

    return render(request, 'reports/attendance_report.html', {
        'courses': courses,
        'attendances': attendances,
        'selected_course': course,
        'stats': stats,
    })


def grade_report(request):
    """Generate grade report."""
    courses = Course.objects.filter(is_active=True)
    course_id = request.GET.get('course')

    if course_id:
        course = get_object_or_404(Course, pk=course_id)
        grades = Grade.objects.filter(course=course).order_by('student')
    else:
        grades = Grade.objects.all().order_by('student')[:100]
        course = None

    # Calculate grade distribution
    grade_distribution = {}
    if course:
        for grade_record in grades:
            if grade_record.grade:
                grade_distribution[grade_record.grade] = grade_distribution.get(grade_record.grade, 0) + 1

    # Calculate average score
    avg_score = grades.aggregate(avg=Avg('total_score'))['avg']

    return render(request, 'reports/grade_report.html', {
        'courses': courses,
        'grades': grades,
        'selected_course': course,
        'grade_distribution': grade_distribution,
        'avg_score': round(avg_score, 2) if avg_score else 0,
    })


def performance_report(request):
    """Generate student performance report."""
    students = Student.objects.filter(is_active=True)
    student_id = request.GET.get('student')

    if student_id:
        student = get_object_or_404(Student, pk=student_id)
        grades = Grade.objects.filter(student=student).order_by('-year', '-semester')
        attendances = Attendance.objects.filter(student=student).order_by('-date')
    else:
        student = None
        grades = []
        attendances = []

    # Calculate GPA
    gpa = 0
    total_credits = 0
    total_grade_points = 0
    grade_point_map = {
        'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7,
        'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0,
        'D-': 0.7, 'F': 0.0
    }

    if student:
        for grade in grades:
            if grade.grade and grade.course:
                gp = grade_point_map.get(grade.grade, 0)
                total_grade_points += gp * grade.course.credits
                total_credits += grade.course.credits

        gpa = total_grade_points / total_credits if total_credits > 0 else 0

    # Calculate attendance rate
    attendance_rate = 0
    if student:
        stats = attendances.aggregate(
            present=Count('id', filter=models.Q(status='present')),
            total=Count('id')
        )
        attendance_rate = (stats['present'] / stats['total'] * 100) if stats['total'] > 0 else 0

    return render(request, 'reports/performance_report.html', {
        'students': students,
        'selected_student': student,
        'grades': grades,
        'attendances': attendances,
        'gpa': round(gpa, 2),
        'attendance_rate': round(attendance_rate, 2),
        'total_credits': total_credits,
    })


def enrollment_report(request):
    """Generate enrollment report."""
    courses = Course.objects.filter(is_active=True)
    course_id = request.GET.get('course')

    if course_id:
        course = get_object_or_404(Course, pk=course_id)
        enrollments = Enrollment.objects.filter(course=course).order_by('student')
    else:
        enrollments = Enrollment.objects.all().order_by('student')[:100]
        course = None

    # Enrollment statistics
    enrollment_stats = {
        'active': enrollments.filter(status='active').count(),
        'completed': enrollments.filter(status='completed').count(),
        'dropped': enrollments.filter(status='dropped').count(),
    }

    return render(request, 'reports/enrollment_report.html', {
        'courses': courses,
        'enrollments': enrollments,
        'selected_course': course,
        'stats': enrollment_stats,
    })


# Import get_object_or_404 at the bottom to avoid circular imports
from django.shortcuts import get_object_or_404

