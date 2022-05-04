import requests
import json

def jprint(obj):
	text = json.dumps(obj, sort_keys=True, indent=4)
	print(text)

def jget(obj):
	j = obj.json()
	return j

def jstrip(odj):
	j = jget(obj)
	ret = []
	for item in j:
		ret.append(item['team'])

	return ret

teams = {}

for i in range(1, 6):
	response = requests.get(f'https://mos2022mlch.calicotab.com/api/v1/tournaments/mlch/rounds/{i}/pairings')
	res_response = requests.get('https://mos2022mlch.calicotab.com/api/v1/tournaments/mlch/teams/standings')
	res_response = jstrip(res_response)
	r = jget(response)
	for item in r:
		for team in item['teams']:
			team_response = requests.get(team['team'])
			tr = jget(team_response)
			if i == 1:
				teams[f'{tr["speakers"][0]["name"]}, {tr["speakers"][1]["name"]}'] = []

			if not f'{tr["speakers"][0]["name"]}, {tr["speakers"][1]["name"]}'.__contains__('Swing'):
				teams[f'{tr["speakers"][0]["name"]}, {tr["speakers"][1]["name"]}'].append(team['side'])

print(teams)