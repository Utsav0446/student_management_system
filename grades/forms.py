from django import forms
from .models import Grade


class GradeForm(forms.ModelForm):
    """Form for creating and updating Grade objects."""

    class Meta:
        model = Grade
        fields = [
            'student', 'course', 'assignment_score', 'exam_score',
            'semester', 'year', 'remarks'
        ]
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'assignment_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'exam_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'semester': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

