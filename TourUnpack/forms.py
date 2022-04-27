from django import forms

class TournamentForm(forms.Form):
	name = forms.CharField(max_length=30)
	date_conducted = forms.DateField()
	num_players = forms.IntegerField()

class FileUploadForm(forms.Form):
	name = forms.CharField(max_length=30)
	tab_file = forms.FileField()

class PlayerTournamentForm(forms.Form):
	name = forms.CharField(max_length=20)
	surname = forms.CharField(max_length=20)
	r1 = forms.IntegerField()
	r1pos = forms.CharField(max_length=2)
	r1res = forms.IntegerField()
	r2 = forms.IntegerField()
	r2pos = forms.CharField(max_length=2)
	r2res = forms.IntegerField()
	r3 = forms.IntegerField()
	r3pos = forms.CharField(max_length=2)
	r3res = forms.IntegerField()
	r4 = forms.IntegerField()
	r4pos = forms.CharField(max_length=2)
	r4res = forms.IntegerField()
	r5 = forms.IntegerField()
	r5pos = forms.CharField(max_length=2)
	r5res = forms.IntegerField()