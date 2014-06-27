from django import forms

from .models import SemcompUser



class UserSignupForm(forms.ModelForm):
	class Meta:
		model = SemcompUser
		fields = ['email', 'full_name', 'id_usp', 'password']
		widgets = {
			'password': forms.PasswordInput
		}
