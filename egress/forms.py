from django import forms
from django.utils.translation import ugettext_lazy as _

from allauth.account.forms import LoginForm, SetPasswordField, PasswordField
from allauth.account.utils import setup_user_email
from allauth.account.adapter import get_adapter

from egress.models import Egress

from allauth.account.forms import SignupForm


class EgressForm(forms.ModelForm):
    class Meta:
        model = Egress
        fields = '__all__'
