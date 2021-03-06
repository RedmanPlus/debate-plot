from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .plot import plotbuilder, massiveplotbuilder
from .models import Tournament, WeirdTournament, PlayerTournamentRelation, CastratedRelation
from .forms import FindTournament, AddCredentials


# Create your views here.
def index(response):
	return render(response, "data/home.html", {})

def one(request):
	name = request.GET.get("name")
	tournament = request.GET.get("tournament")
	return_dict = plotbuilder(name, tournament)
	return render(request, "data/one.html", return_dict)

def all(request):
	name = request.GET.get("name")
	return_dict = massiveplotbuilder(name)
	return render(request, "data/all.html", return_dict)

def personal_page(response):
	if response.user:
		tpr = PlayerTournamentRelation.objects.filter(player_id=response.user.id)
		w_tpr = WeirdTournament.objects.filter(player_id=response.user.id)
		c_tpr = CastratedRelation.objects.filter(player_id=response.user.id)
		tl = []
		for tp in tpr:
			unit = {}
			tour = Tournament.objects.get(id=tp.toutnament_id)
			u = User.objects.get(id=response.user.id)
			unit['name'] = tour.name
			unit['link'] = f'/one/?name={u.username}&tournament={(tour.name).replace(" ", "%20")}'
			tl.append(unit)

		for w_tp in w_tpr:
			unit = {}
			tour = Tournament.objects.get(id=w_tp.tournament_id)
			u = User.objects.get(id=response.user.id)
			unit['name'] = tour.name
			unit['link'] = f'/one/?name={u.username}&tournament={(tour.name).replace(" ", "%20")}'
			tl.append(unit)

		for c_tp in c_tpr:
			unit = {}
			tour = Tournament.objects.get(id=c_tp.tournament_id)
			u = User.objects.get(id=response.user.id)
			unit['name'] = tour.name
			unit['link'] = f'/one/?name={u.username}&tournament={(tour.name).replace(" ", "%20")}'
			tl.append(unit)

		if tl == []:
			unit = {}
			unit['name'] = 'У вас пока нет турниров, в которых вы участвовали'
			unit['link'] = '/'
			tl.append()

			per_link = '/'

			return render(response, "data/personal_page.html", {'tournaments': tl, 'per_link': per_link})

	u = User.objects.get(id=response.user.id)
	per_link = f'/all/?name={u.username}'

	return render(response, "data/personal_page.html", {'tournaments': tl, 'per_link': per_link})

def donate(response):

	return render(response, "data/donate.html", {})