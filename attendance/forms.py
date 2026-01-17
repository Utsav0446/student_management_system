from django import forms
from .models import Attendance


class AttendanceForm(forms.ModelForm):
    """Form for creating and updating Attendance objects."""

    class Meta:
        model = Attendance
        fields = ['student', 'course', 'date', 'status', 'remarks']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

