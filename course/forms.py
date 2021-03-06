from django import forms
from django.utils.translation import ugettext_lazy as _

from course.models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
