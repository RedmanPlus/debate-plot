from django import forms

class FindTournament(forms.Form):
	name = forms.CharField(label='Название турнира', max_length=30)

class AddCredentials(forms.Form):
	first_name = forms.CharField(label='Имя спикера', max_length=20)
	last_name = forms.CharField(label='Фамилия спикера', max_length=20)