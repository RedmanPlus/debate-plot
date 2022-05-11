from django.shortcuts import render, redirect
from .forms import TournamentForm, PlayerTournamentForm, FileUploadForm, ApiForm
from .models import UnsignedTournament, UnsignedPlayer, UnsignedRelation
from .retrieve import file_unpack_excel, players_update, double_depricate
from .api import api_extruder

# Create your views here.
def home(response):
	return render(response, 'TourUnpack/home.html', {})

def add(request):
	if request.method == 'POST':
		if request.POST.get("form_type") == "tour_form":
			tour_form = TournamentForm(request.POST)
			if tour_form.is_valid():
				n = tour_form.cleaned_data['name']
				d = tour_form.cleaned_data['date_conducted']
				num = tour_form.cleaned_data['num_players']
				UnsignedTournament.objects.create(name=n, date_conducted=d, num_players=num, has_tab=False)
				return redirect('/staff/')
		elif request.POST.get("form_type") == "tab_form":
			tab_form = FileUploadForm(request.POST, request.FILES)
			if tab_form.is_valid():
				n = tab_form.cleaned_data['name']
				f = request.FILES['tab_file']
				file_unpack_excel(f, n)
			
				return redirect('/staff/')
		elif request.POST.get("form_type") == "api_form":
			api_form = ApiForm(request.POST)
			if api_form.is_valid():
				n = api_form.cleaned_data['name']
				l = api_form.cleaned_data['link']
				api_extruder(l, n)

				return redirect('/staff/')

	else:
		tour_form = TournamentForm()
		tab_form = FileUploadForm()
		api_form = ApiForm()

	return render(request, 'TourUnpack/add.html', {'tour_form': tour_form, 'tab_form': tab_form, 'api_form': api_form})

def update(response):
	tours = UnsignedTournament.objects.all()
	
	t_list = []
	for tour in tours:
		t_list.append(tour.name)

	return render(response, 'TourUnpack/update.html', {'t_list': t_list})

def load(response):
	players_update()
	return redirect('/staff/')

def depricate(response):
	double_depricate()
	return redirect('/staff/')