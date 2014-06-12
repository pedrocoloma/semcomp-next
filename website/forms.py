from django import forms

from .models import Company, SemcompUser

class CompanyForm(forms.ModelForm):
	class Meta:
		model = Company
		fields = ['name', 'logo', 'type']


class UserSignupForm(forms.ModelForm):
	class Meta:
		model = SemcompUser
		fields = ['email', 'full_name', 'id_usp', 'password']
		widgets = {
			'password': forms.PasswordInput
		}
