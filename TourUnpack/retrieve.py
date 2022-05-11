import pandas as pd
from fuzzywuzzy import fuzz, process
from django.contrib.auth.models import User
from .models import UnsignedTournament, UnsignedPlayer, UnsignedRelation, UnsignedWeirdTournament, UnsignedCastratedRelation
from data.models import Tournament, PlayerTournamentRelation, WeirdTournament, CastratedRelation

def file_unpack_excel(file, tour_name):

	df_speaks = pd.read_excel(file, sheet_name='Спикеры')
	df_res = pd.read_excel(file, sheet_name='Команды')

	t = UnsignedTournament.objects.get(name=tour_name)

	df_speaks = df_speaks.set_index('name')
	df_res = df_res.set_index('team')

	for name_pair in df_speaks.index:
		if ('Swing' in name_pair) or ('Свинг' in name_pair) or ('Speaker' in name_pair) or ('Спикер' in name_pair):
			continue
		else:
			try:
				surname, name = name_pair.split(' ')
			except IndexError:
				ret = name_pair.split(' ')
				surname, name = ret[0], ret[1]
			player = UnsignedPlayer.objects.filter(name=name, surname=surname)

			if not player.exists():
				player = UnsignedPlayer.objects.create(name=name, surname=surname)
				player.save()
			else:
				player = player.first()

			cast_rel = UnsignedCastratedRelation.objects.filter(tournament=t, player=player)
			if cast_rel.exists():
				cast_rel = cast_rel.first()
				fill_form = [
					df_speaks.loc[name_pair, 'R1'],
					df_speaks.loc[name_pair, 'R2'],
					df_speaks.loc[name_pair, 'R3'],
					df_speaks.loc[name_pair, 'R4'],
					df_speaks.loc[name_pair, 'R5'],
					df_res.loc[df_speaks.loc[name_pair, 'team'], 'R1'],
					df_res.loc[df_speaks.loc[name_pair, 'team'], 'R2'],
					df_res.loc[df_speaks.loc[name_pair, 'team'], 'R3'],
					df_res.loc[df_speaks.loc[name_pair, 'team'], 'R4'],
					df_res.loc[df_speaks.loc[name_pair, 'team'], 'R5']
				]

				rel = UnsignedRelation.objects.create(tournament=t, 
					player=player,
					r1 = fill_form[0],
					r2 = fill_form[1],
					r3 = fill_form[2],
					r4 = fill_form[3],
					r5 = fill_form[4],
					r1pos = cast_rel.r1pos,
					r2pos = cast_rel.r2pos,
					r3pos = cast_rel.r3pos,
					r4pos = cast_rel.r4pos,
					r5pos = cast_rel.r5pos,
					r1res = fill_form[5],
					r2res = fill_form[6],
					r3res = fill_form[7],
					r4res = fill_form[8],
					r5res = fill_form[9]
					)
				
				rel.save()
			else:

				fill_form = [
					df_speaks.loc[name_pair, 'R1'],
					df_speaks.loc[name_pair, 'R2'],
					df_speaks.loc[name_pair, 'R3'],
					df_speaks.loc[name_pair, 'R4'],
					df_speaks.loc[name_pair, 'R5'],
					(df_res.loc[df_speaks.loc[name_pair, 'team'], 'R1']),
					(df_res.loc[df_speaks.loc[name_pair, 'team'], 'R2']),
					(df_res.loc[df_speaks.loc[name_pair, 'team'], 'R3']),
					(df_res.loc[df_speaks.loc[name_pair, 'team'], 'R4']),
					(df_res.loc[df_speaks.loc[name_pair, 'team'], 'R5'])
				]


				rel = UnsignedRelation.objects.create(tournament=t, 
					player=player,
					r1 = fill_form[0],
					r2 = fill_form[1],
					r3 = fill_form[2],
					r4 = fill_form[3],
					r5 = fill_form[4],
					r1pos = 'No',
					r2pos = 'No',
					r3pos = 'No',
					r4pos = 'No',
					r5pos = 'No',
					r1res = fill_form[5],
					r2res = fill_form[6],
					r3res = fill_form[7],
					r4res = fill_form[8],
					r5res = fill_form[9]
					)
				rel.save()

def players_update():

	sign_players = User.objects.all()

	for player in sign_players:
		uns_ver = UnsignedPlayer.objects.filter(name=player.first_name, surname=player.last_name)
		if uns_ver.exists():
			uns_ver = uns_ver.first()
			uns_rels = UnsignedRelation.objects.filter(player_id=uns_ver)
			uns_weird = UnsignedWeirdTournament.objects.filter(player_id=uns_ver)
			uns_cast = UnsignedCastratedRelation.objects.filter(player_id=uns_ver)

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

			if uns_cast.exists():
				for ver in uns_cast:
					uns_tour = UnsignedTournament.objects.get(id=ver.tournament_id)
					try:
						tour = Tournament.objects.get(name=uns_tour.name, date_conducted=uns_tour.date_conducted)
					except:
						tour = Tournament.objects.create(
							name=uns_tour.name,
							date_conducted=uns_tour.date_conducted
							)

					test_relation = CastratedRelation.objects.filter(tournament=tour, player=player)

					if not test_relation.exists():

						relation = CastratedRelation.objects.create(
							tournament = tour,
							player = player,
							avg_res = ver.avg_res,
							stdev_res = ver.stdev_res,
							firsts = ver.firsts,
							seconds = ver.seconds,
							r1pos = ver.r1pos,
							r2pos = ver.r2pos,
							r3pos = ver.r3pos,
							r4pos = ver.r4pos,
							r5pos = ver.r5pos,				
							)

						tour.save()
						relation.save()

def double_depricate():

	u = UnsignedPlayer.objects.all()

	for user in u:
		name, surname = user.name, user.surname

		for other_user in u:
			other_name, other_surname = other_user.name, other_user.surname

			a = fuzz.ratio(name, other_name)
			a_0 = fuzz.partial_ratio(name, other_name)
			b = fuzz.ratio(surname, other_surname)
			b_0 = fuzz.partial_ratio(surname, other_surname)

			first_check = ((a + a_0)/2 + (b + b_0)/2)/2

			if first_check >= 75.0:
				ind, other_ind = user.id, other_user.id

				tours = UnsignedRelation.objects.filter(player=other_user)
				for tour in tours:
					tour.player_id = ind
					tour.save()

				weird_tours = UnsignedWeirdTournament.objects.filter(player=other_user)
				for w_tour in weird_tours:
					w_tour.player_id = ind
					w_tour.save()

				cast_tours = UnsignedCastratedRelation.objects.filter(player=other_user)
				for c_tour in cast_tours:
					c_tour.player_id = ind
					c_tour.save()

			a0 = fuzz.ratio(name, other_surname)
			a0_0 = fuzz.partial_ratio(name, other_surname)
			b0 = fuzz.ratio(surname, other_name)
			b0_0 = fuzz.partial_ratio(surname, other_name)

			second_check = ((a0 + a0_0)/2 + (b0 + b0_0)/2)/2

			if second_check >= 75:
				ind, other_ind = user.id, other_user.id

				tours = UnsignedRelation.objects.filter(player=other_user)
				for tour in tours:
					tour.player_id = ind
					tour.save()

				weird_tours = UnsignedWeirdTournament.objects.filter(player=other_user)
				for w_tour in weird_tours:
					w_tour.player_id = ind
					w_tour.save()

				cast_tours = UnsignedCastratedRelation.objects.filter(player=other_user)
				for c_tour in cast_tours:
					c_tour.player_id = ind
					c_tour.save()