from django import forms

class FindTournament(forms.Form):
	name = forms.CharField(label='Название турнира', max_length=30)