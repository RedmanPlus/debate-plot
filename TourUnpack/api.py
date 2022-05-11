import requests
import json
from .models import UnsignedTournament, UnsignedPlayer, UnsignedRelation, UnsignedCastratedRelation

def jprint(obj):
	text = json.dumps(obj, sort_keys=True, indent=4)
	print(text)

def jget(obj):
	j = obj.json()
	return j

def slugstrip(obj, link, name):
	j = jget(obj)
	for item in j:
		if item['short_name'] == name:
			return item['slug']

def resstrip(obj, link, slug):
	j = jget(obj)
	ret = {}
	for element in j:
		ret[str(element['team']).replace(f'{link}/api/v1/tournaments/{slug}/teams/', '')] = [
		element['metrics'][0]['value'],  
		element['metrics'][2]['value'], 
		element['metrics'][3]['value'],]

	return ret

def speakstrip(obj, link, slug):
	j = jget(obj)
	ret = {}
	for element in j:
		ret[str(element['speaker']).replace(f'{link}/api/v1/tournaments/{slug}/speakers/', '')] = [
		element['metrics'][1]['value'],
		element['metrics'][2]['value']
		]

	return ret

def posstrip(obj, link, slug):
	j = jget(obj)
	ret = {}
	for element in j:
		for side in element['teams']:
			ret[str(side['team']).replace(f'{link}/api/v1/tournaments/{slug}/teams/', '')] = side['side']

	return ret

def teamstrip(obj):
	j = jget(obj)
	ret = {}
	for element in j:
		ret[str(element['id'])] = [
			[
			str(element['speakers'][0]['id']), 
			element['speakers'][0]['name']
			], 
			[
			str(element['speakers'][1]['id']), 
			element['speakers'][1]['name']
			]
		]

	return ret


def api_extruder(link, tourname):

	slug = slugstrip(requests.get(f'{link}/api/v1/tournaments'), link, tourname)

	res_response = requests.get(f'{link}/api/v1/tournaments/{slug}/teams/standings')
	speak_response = requests.get(f'{link}/api/v1/tournaments/{slug}/speakers/standings')
	team_response = requests.get(f'{link}/api/v1/tournaments/{slug}/teams')

	a = resstrip(res_response, link, slug)
	b = speakstrip(speak_response, link, slug)
	c = teamstrip(team_response)
	d = {}

	for i in range(1, 6):
		pos_response = requests.get(f'{link}/api/v1/tournaments/{slug}/rounds/{i}/pairings')
		p = posstrip(pos_response, link, slug)
		d[i] = p

	result = {}

	for key, value in c.items():

		stand = []
		for stand_key, stand_value in d.items():
				
			try:

				if stand_value[str(key)] == '-':
					stand.append('No')
				else:
					stand.append(stand_value[str(key)])
		
			except KeyError:

				stand.append(['No'])


		res = a[str(key)]

		speak_1 = b[str(value[0][0])]
		speak_2 = b[str(value[1][0])]

		result[value[0][1]] = [stand, res, speak_1]
		result[value[1][1]] = [stand, res, speak_2]

	for key, value in result.items():
		name, surname = key.split(' ')
		player = UnsignedPlayer.objects.filter(name=name, surname=surname)
		if not player.exists():
			player = UnsignedPlayer.objects.filter(name=surname, surname=name)
			if not player.exists():
				player = UnsignedPlayer.objects.create(name=name, surname=surname)
			else:
				player = player.first()
		else:
			player = player.first()

		tour = UnsignedTournament.objects.get(name=tourname)

		full_relation = UnsignedRelation.objects.filter(tournament=tour, player=player)
		if full_relation.exists():
			full_relation = full_relation.first()
			full_relation.r1pos = value[0][0]
			full_relation.r2pos = value[0][1]
			full_relation.r3pos = value[0][2]
			full_relation.r4pos = value[0][3]
			full_relation.r5pos = value[0][4]

			full_relation.save()
		else:
			relation = UnsignedCastratedRelation.objects.create(
				tournament=tour,
				player=player,
				avg_res=value[2][0],
				stdev_res=value[2][1],
				firsts=value[1][1],
				seconds=value[1][2],
				r1pos=value[0][0],
				r2pos=value[0][1],
				r3pos=value[0][2],
				r4pos=value[0][3],
				r5pos=value[0][4],
				)

			relation.save()
