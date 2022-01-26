from django import forms
from django.utils.translation import ugettext_lazy as _

from course.models import Course, Directorship


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class DirectorshipForm(forms.ModelForm):
    class Meta:
        model = Directorship
        fields = '__all__'