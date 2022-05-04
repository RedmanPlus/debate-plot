from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegisterForm
from TourUnpack.retrieve import players_update

# Create your views here.
def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			new_user = authenticate(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password1']
				)
			if new_user is not None:
				
				login(request, new_user)

				players_update()

				return redirect('/')
	else:
		form = RegisterForm()

	return render(request, 'register/register.html', {'form': form})