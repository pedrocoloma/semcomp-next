from django import forms
from website.models import Inscricao

class InscricoesForm(forms.ModelForm):
	class Meta:
		model = Inscricao
		fields = ['comprovante']