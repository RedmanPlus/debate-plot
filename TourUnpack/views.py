from django.shortcuts import render, redirect
from .forms import TournamentForm, PlayerTournamentForm, FileUploadForm
from .models import UnsignedTournament, UnsignedPlayer, UnsignedRelation


# Create your views here.
def home(response):
	return render(response, 'TourUnpack/home.html', {})


def add(response):
	if response.method == 'POST':
		if response.POST.get("form_type") == "form_tour":
			tour_form = TournamentForm(response.POST)
			if tour_form.is_valid():
				n = tour_form.cleaned_data['name']
				d = tour_form.cleaned_data['date_conducted']
				num = tour_form.cleaned_data['num_players']
				UnsignedTournament.objects.create(name=n, date_conducted=d, num_playesr=num, has_tab=False)
				return redirect('/staff/')
		elif response.POST.get("form_type") == "form_tab":
			tab_form = FileUploadForm(response.POST, response.FILES)
			if tab_form.is_valid():
				n = tab_form.cleaned_data['name']
				return redirect('/staff/')
	else:
		tour_form = TournamentForm()
		tab_form = FileUploadForm()

	return render(response, 'TourUnpack/add.html', {'tour_form': tour_form, 'tab_form': tab_form})