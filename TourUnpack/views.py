from django.shortcuts import render
from .forms import TournamentForm, PlayerTournamentForm
from .models import UnsignedTournament, UnsignedPlayer, UnsignedRelation

# Create your views here.
def home(response):
	return render(response, 'TourUnpack/home.html', {})

def add(response):
	if response.method == 'POST':
		tour_form = TournamentForm(response.POST)
		if form.is_valid():
			n = tour_form.cleaned_data['name']
			d = tour_form.cleaned_data['date_conducted']
			num = tour_form.cleaned_data['num_players']
			UnsignedTournament.objects.create(name=n, date_conducted=d, num_playesr=num, has_tab=False)
	else:
		tour_form = TournamentForm()

	tours = UnsignedTournament.objects.all()

	return render(response, 'TourUnpack/add.html', {'tour_form': tour_form})