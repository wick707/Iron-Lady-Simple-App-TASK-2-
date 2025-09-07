from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'overview': forms.Textarea(attrs={'rows': 4}),
            'target_audience': forms.Textarea(attrs={'rows': 4}),
            'interests_aligned': forms.Textarea(attrs={'rows': 4}),
        }

