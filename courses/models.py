from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    """
    Course model to store course information.
    """
    course_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    credits = models.IntegerField(default=3)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses_taught')
    semester = models.CharField(max_length=20, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    max_students = models.IntegerField(default=30)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['course_code']

    def __str__(self):
        return f"{self.course_code} - {self.name}"


class Enrollment(models.Model):
    """
    Enrollment model to track student course enrollments.
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
    ]

    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    grade = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        unique_together = ['student', 'course']
        ordering = ['course', 'student']

    def __str__(self):
        return f"{self.student} - {self.course} ({self.status})"

