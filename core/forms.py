from django import forms
from django.utils.translation import ugettext_lazy as _

from allauth.account.forms import LoginForm, SetPasswordField, PasswordField
from allauth.account.utils import setup_user_email
from allauth.account.adapter import get_adapter

from core.models import User

from allauth.account.forms import SignupForm


class AllauthCompatLoginForm(LoginForm):
	def user_credentials(self):
		credentials = super(AllauthCompatLoginForm, self).user_credentials()
		credentials['login'] = credentials.get('email') or credentials.get('username')
		return credentials


class ContactForm(forms.Form):
	pass


class CustomSignupForm(SignupForm):
	def __init__(self, *args, **kwargs):
		super(CustomSignupForm, self).__init__(*args, **kwargs)
	
	def clean(self):
		super(CustomSignupForm, self).clean()
		if "password1" not in self.cleaned_data or "password2" not in self.cleaned_data:
			raise forms.ValidationError("This password is very common.")
			self.add_error('password1', e)

		if self.cleaned_data["password1"] \
				!= self.cleaned_data["password2"]:
			raise forms.ValidationError(_(
				"You must type the same password each time."))
		return self.cleaned_data
	
	def save(self, request):
		adapter = get_adapter()
		user = adapter.new_user(request)

		adapter.save_user(request, user, self)
		self.custom_signup(request, user)
		setup_user_email(request, user, [])
		return user
