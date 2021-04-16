import requests

from django import forms
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import authenticate, login

from allauth.account.forms import LoginForm, SetPasswordField, PasswordField
from allauth.account.utils import setup_user_email
from allauth.account.adapter import get_adapter

from core.models import User

from allauth.account.forms import SignupForm


class AllauthCompatLoginForm(LoginForm):
	def user_credentials(self):
		login = self.cleaned_data["login"]
		password = self.cleaned_data["password"]

		response = requests.post('https://suap.ifrn.edu.br/api/v2/autenticacao/token/', {
			"username": login,
			"password": password,
		})
		try:
			suapResponse = response.json()
			if suapResponse["token"]:
				try:
					user = User.objects.get(username__exact=login)
					if user:
						userAutentication = authenticate(username=login, password=str(password))
						if userAutentication is None:
							user.set_password(str(password))
							user.save()
				except:
					pass
		except:
			pass
		
		credentials = super(AllauthCompatLoginForm, self).user_credentials()
		credentials['login'] = credentials.get('username')
		credentials['password'] = credentials.get('password')
		return credentials

class ContactForm(forms.Form):
	pass


class CustomSignupForm(SignupForm):
	def __init__(self, *args, **kwargs):
		super(CustomSignupForm, self).__init__(*args, **kwargs)
		self.fields['siape'] = forms.CharField(required=True)
		self.fields['siape'].widget.attrs.update({
			'class': 'form-control'
		})
	
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

		siape = int(self.cleaned_data.pop('siape'))
		user.siape = siape

		adapter.save_user(request, user, self)
		self.custom_signup(request, user)
		setup_user_email(request, user, [])
		return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
			'date_joined', 'email', 'first_name', 'groups', 'id', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'last_name', 'password', 'user_permissions', 'username'
        )


class UserFoodForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
			'date_joined', 'email', 'first_name', 'groups', 'id', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'last_name', 'password', 'user_permissions', 'username'
        )
