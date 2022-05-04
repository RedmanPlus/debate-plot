from django.shortcuts import render, redirect
from .forms import TournamentForm, PlayerTournamentForm, FileUploadForm
from .models import UnsignedTournament, UnsignedPlayer, UnsignedRelation
from .retrieve import file_unpack_excel, players_update

# Create your views here.
def home(response):
	return render(response, 'TourUnpack/home.html', {})

def add(request):
	if request.method == 'POST':
		if request.POST.get("form_type") == "form_tour":
			tour_form = TournamentForm(request.POST)
			if tour_form.is_valid():
				n = tour_form.cleaned_data['name']
				d = tour_form.cleaned_data['date_conducted']
				num = tour_form.cleaned_data['num_players']
				UnsignedTournament.objects.create(name=n, date_conducted=d, num_players=num, has_tab=False)
				return redirect('/staff/')
		elif request.POST.get("form_type") == "form_tab":
			tab_form = FileUploadForm(request.POST, request.FILES)
			if tab_form.is_valid():
				n = tab_form.cleaned_data['name']
				f = request.FILES['file']
				file_unpack_excel(f, n)
				return redirect('/staff/')
	else:
		tour_form = TournamentForm()
		tab_form = FileUploadForm()

	return render(request, 'TourUnpack/add.html', {'tour_form': tour_form, 'tab_form': tab_form})

def update(response):
	tours = UnsignedTournament.objects.all()
	
	t_list = []
	for tour in tours:
		t_list.append(tour.name)

	return render(response, 'TourUnpack/update.html', {'t_list': t_list})

def load(response):
	players_update()
	return redirect('/staff/')