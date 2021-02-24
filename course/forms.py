from django import forms
from django.utils.translation import ugettext_lazy as _

from allauth.account.forms import LoginForm, SetPasswordField, PasswordField
from allauth.account.utils import setup_user_email
from allauth.account.adapter import get_adapter

from course.models import Course

from allauth.account.forms import SignupForm


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        
        # fields = (
		# 	'date_joined', 'email', 'first_name', 'groups', 'id', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'last_name', 'password', 'user_permissions', 'username'
        # )
