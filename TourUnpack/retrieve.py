from io import StringIO
import pandas as pd
from django.contrib.auth.models import User
from .models import UnsignedTournament, UnsignedPlayer, UnsignedRelation, UnsignedWeirdTournament
from data.models import Tournament, PlayerTournamentRelation, WeirdTournament

def file_unpack_csv(f):
	with open('filename.csv', w) as destination:
		for chunk in f.chunks():
			destination.write(chunk)

def file_unpack_excel(file, tour_name):

	df_speaks = pd.read_excel(StringIO(file.read().decode('utf-8')), sheet_name='Спикеры')
	df_res = pd.read_excel(StringIO(file.read().decode('utf-8')), sheet_name='Команды')

	t = UnsignedTournament.objects.get(name=tour_name)

	df_speaks = df_speaks.set_index('Name')
	df_res = df_res.set_index('Name')

	for name_pair in df_speaks.index:
		if name_pair == 'unnamed':
			continue
		else:
			surname, name = name_pair.split(' ')
			player = UnsignedPlayer.objects.filter(name=name, surname=surname)

			if not player.exists():
				player = UnsignedPlayer.objects.create(name=name, surname=surname)
				player.save()
			else:
				player = player.first()

			rel = UnsignedWeirdTournament.objects.create(tournament=t, 
				player=player,
				r1 = df_speaks.loc[name_pair, 'Round 1'],
				r2 = df_speaks.loc[name_pair, 'Round 2'],
				r3 = df_speaks.loc[name_pair, 'Round 3'],
				r4 = df_speaks.loc[name_pair, 'Round 4'],
				r5 = df_speaks.loc[name_pair, 'Round 5'],
				r6 = df_speaks.loc[name_pair, 'Round 6'],
				r1pos = 'No',
				r2pos = 'No',
				r3pos = 'No',
				r4pos = 'No',
				r5pos = 'No',
				r6pos = 'No',
				r1res = int(df_res.loc[df_speaks.loc[name_pair, 'Team'], 'Rank R1']),
				r2res = int(df_res.loc[df_speaks.loc[name_pair, 'Team'], 'Rank R2']),
				r3res = int(df_res.loc[df_speaks.loc[name_pair, 'Team'], 'Rank R3']),
				r4res = int(df_res.loc[df_speaks.loc[name_pair, 'Team'], 'Rank R4']),
				r5res = int(df_res.loc[df_speaks.loc[name_pair, 'Team'], 'Rank R5']),
				r6res = int(df_res.loc[df_speaks.loc[name_pair, 'Team'], 'Rank R6'])
				)
			rel.save()

def players_update():

	sign_players = User.objects.all()

	for player in sign_players:
		uns_ver = UnsignedPlayer.objects.get(name=player.first_name, surname=player.last_name)
		uns_rels = UnsignedRelation.objects.filter(player_id=uns_ver)
		uns_weird = UnsignedWeirdTournament.objects.filter(player_id=uns_ver)

		for rel in uns_rels:
			uns_tour = UnsignedTournament.objects.get(id=rel.tournament_id)
			try:
				tour = Tournament.objects.get(name=uns_tour.name, date_conducted=uns_tour.date_conducted)
			except:
				tour = Tournament.objects.create(
					name=uns_tour.name,
					date_conducted=uns_tour.date_conducted
					)

			test_relation = PlayerTournamentRelation.objects.filter(toutnament=tour, player=player)

			if not test_relation.exists():

				relation = PlayerTournamentRelation.objects.create(
					toutnament = tour,
					player = player,
					r1 = rel.r1,
					r2 = rel.r2,
					r3 = rel.r3,
					r4 = rel.r4,
					r5 = rel.r5,
					r1pos = rel.r1pos,
					r2pos = rel.r2pos,
					r3pos = rel.r3pos,
					r4pos = rel.r4pos,
					r5pos = rel.r5pos,
					r1res = rel.r1res,
					r2res = rel.r2res,
					r3res = rel.r3res,
					r4res = rel.r4res,
					r5res = rel.r5res				
					)

				tour.save()
				relation.save()

		if uns_weird.exists():
			for ver in uns_weird:
				uns_tour = UnsignedTournament.objects.get(id=ver.tournament_id)
				try:
					tour = Tournament.objects.get(name=uns_tour.name, date_conducted=uns_tour.date_conducted)
				except:
					tour = Tournament.objects.create(
						name=uns_tour.name,
						date_conducted=uns_tour.date_conducted
						)

				test_relation = WeirdTournament.objects.filter(tournament=tour, player=player)

				if not test_relation.exists():

					relation = WeirdTournament.objects.create(
						tournament = tour,
						player = player,
						r1 = ver.r1,
						r2 = ver.r2,
						r3 = ver.r3,
						r4 = ver.r4,
						r5 = ver.r5,
						r6 = ver.r6,
						r1pos = ver.r1pos,
						r2pos = ver.r2pos,
						r3pos = ver.r3pos,
						r4pos = ver.r4pos,
						r5pos = ver.r5pos,
						r6pos = ver.r6pos,
						r1res = ver.r1res,
						r2res = ver.r2res,
						r3res = ver.r3res,
						r4res = ver.r4res,
						r5res = ver.r5res,
						r6res = ver.r6res				
						)

					tour.save()
					relation.save()