from django.db import models
from students.models import Student
from courses.models import Course


class Grade(models.Model):
    """
    Grade model to record and manage student grades.
    """
    GRADE_CHOICES = [
        ('A', 'A'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B', 'B'),
        ('B-', 'B-'),
        ('C+', 'C+'),
        ('C', 'C'),
        ('C-', 'C-'),
        ('D+', 'D+'),
        ('D', 'D'),
        ('D-', 'D-'),
        ('F', 'F'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')
    assignment_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    exam_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    grade = models.CharField(max_length=5, choices=GRADE_CHOICES, blank=True, null=True)
    semester = models.CharField(max_length=20, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'course', 'semester', 'year']
        ordering = ['-year', '-semester', 'course']

    def __str__(self):
        return f"{self.student} - {self.course} - {self.grade}"

    def calculate_total(self):
        """Calculate total score from assignment and exam scores."""
        if self.assignment_score is not None and self.exam_score is not None:
            self.total_score = self.assignment_score + self.exam_score
            self.calculate_letter_grade()
        elif self.assignment_score is not None:
            self.total_score = self.assignment_score
            self.calculate_letter_grade()
        elif self.exam_score is not None:
            self.total_score = self.exam_score
            self.calculate_letter_grade()

    def calculate_letter_grade(self):
        """Calculate letter grade based on total score."""
        if self.total_score is None:
            return

        if self.total_score >= 90:
            self.grade = 'A'
        elif self.total_score >= 85:
            self.grade = 'A-'
        elif self.total_score >= 80:
            self.grade = 'B+'
        elif self.total_score >= 75:
            self.grade = 'B'
        elif self.total_score >= 70:
            self.grade = 'B-'
        elif self.total_score >= 65:
            self.grade = 'C+'
        elif self.total_score >= 60:
            self.grade = 'C'
        elif self.total_score >= 55:
            self.grade = 'C-'
        elif self.total_score >= 50:
            self.grade = 'D+'
        elif self.total_score >= 45:
            self.grade = 'D'
        elif self.total_score >= 40:
            self.grade = 'D-'
        else:
            self.grade = 'F'

    def save(self, *args, **kwargs):
        self.calculate_total()
        super().save(*args, **kwargs)

