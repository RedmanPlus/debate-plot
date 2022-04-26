from datetime import datetime
from statistics import stdev, median
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool, DatetimeTickFormatter, NumeralTickFormatter
from django.contrib.auth.models import User
from .models import Tournament, PlayerTournamentRelation

def plotbuilder(name, tournament):
	tour = Tournament.objects.get(name=tournament)
	u = User.objects.get(username=name)
	points = PlayerTournamentRelation.objects.get(toutnament_id=tour.id, player_id=u.id)
	x = [1, 2, 3, 4, 5]
	y1 = [int(points.r1), int(points.r2), int(points.r3), int(points.r4), int(points.r5)]

	p = figure(
		y_range=(65, 85),
		title=f'Спикерские баллы за {tour.name}',
		tools=[HoverTool()],
		tooltips='В @x раунде вы набрали @y спикерских',
		sizing_mode='stretch_width',
		height=450,
		x_axis_label='Раунды',
		y_axis_label='Спикерские'
		)

	p.toolbar.autohide = True
	p.title_location = 'above'
	p.title.text_font_size = "25px"
	p.title.align = "center"
	p.title.text_color = "black"

	p.line(x, y1, color='blue', line_width=3)
	p.circle(x, y1, color='blue', size=10)

	script, div = components(p)

	avg = sum(y1) / len(y1)
	med = median(y1)
	st_dev = round(stdev(y1), 2)

	return_dict = {
		'div': div,
		'script': script,
		'avg': avg,
		'med': med,
		'st_dev': st_dev
	}

	return return_dict

def massiveplotbuilder(name):
	u = User.objects.get(username=name)
	tours = PlayerTournamentRelation.objects.filter(player_id=u.id)
	x_ax = []
	y_ax = []
	for tour in tours:
		x = Tournament.objects.get(id=tour.toutnament_id)
		y = (int(tour.r1) + int(tour.r2) + int(tour.r3) + int(tour.r4) + int(tour.r5))/5
		x_ax.append(datetime.combine(x.date_conducted, datetime.min.time()))
		y_ax.append(y)
	p = figure(
		y_range=(65, 85),
		title=f'Спикерские баллы за все турниры',
		tools=[HoverTool()],
		tooltips='В этом турнире вы получили средний спикерский @y',
		sizing_mode='stretch_width',
		height=450,
		x_axis_label='Турниры',
		y_axis_label='Спикерские'
		)

	p.toolbar.autohide = True
	p.title_location = 'above'
	p.title.text_font_size = "25px"
	p.title.align = "center"
	p.title.text_color = "black"

	p.line(x_ax, y_ax, color='blue', line_width=3)
	p.circle(x_ax, y_ax, color='blue', size=10)

	p.yaxis[0].formatter = NumeralTickFormatter(format="00.00")
	p.xaxis[0].formatter = DatetimeTickFormatter(months="%b %Y")

	script, div = components(p)

	avg = sum(y_ax) / len(y_ax)
	med = median(y_ax)
	st_dev = round(stdev(y_ax), 2)

	return_dict = {
		'div': div,
		'script': script,
		'avg': avg,
		'med': med,
		'st_dev': st_dev
	}

	return return_dict