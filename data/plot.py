from datetime import datetime
from statistics import stdev, median
from bokeh.plotting import figure
from bokeh.layouts import layout
from bokeh.embed import components
from bokeh.models import HoverTool, DatetimeTickFormatter, NumeralTickFormatter, Panel, Tabs, Div
from django.contrib.auth.models import User
from .models import Tournament, WeirdTournament, PlayerTournamentRelation, CastratedRelation

# builds a plot for an individual tournament

def plotbuilder(name, tournament):

	tour = Tournament.objects.get(name=tournament)
	u = User.objects.get(username=name)
	try:
		points = PlayerTournamentRelation.objects.get(toutnament_id=tour.id, player_id=u.id)
		x = [1, 2, 3, 4, 5]
		y1 = [int(points.r1), int(points.r2), int(points.r3), int(points.r4), int(points.r5)]

	except:

		try:
			points = WeirdTournament.objects.get(tournament_id=tour.id, player_id=u.id)
			x = [1, 2, 3, 4, 5, 6]
			y1 = [int(points.r1), int(points.r2), int(points.r3), int(points.r4), int(points.r5), int(points.r6)]
		except:
			div = 'Тэб для этого турнира записан в базе данных не полностью'
			script = 'и к сожалению, у нас есть только общие данные о среднем спикерском и стандартном отклонении'
			points = CastratedRelation.objects.get(tournament_id=tour.id, player_id=u.id)
			avg = points.avg_res
			med = 'Данных недостаточно для вычисления медианного значения'
			st_dev = points.stdev_res

			return_dict = {
				'div': div,
				'script': script,
				'avg': avg,
				'med': med,
				'st_dev': st_dev
			}

			return return_dict

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

	avg = round(sum(y1) / len(y1), 2)
	med = round(median(y1), 2)
	st_dev = round(stdev(y1), 2)

	return_dict = {
		'div': div,
		'script': script,
		'avg': avg,
		'med': med,
		'st_dev': st_dev
	}

	return return_dict

# builds a series of plots for a full analytica page

def massiveplotbuilder(name):
	u = User.objects.get(username=name)
	tours = PlayerTournamentRelation.objects.filter(player_id=u.id)
	weird_tours = WeirdTournament.objects.filter(player_id=u.id)
	cast_tours = CastratedRelation.objects.filter(player_id=u.id)

	x_ax = []
	x_c_ax = []
	y_ax = []
	y_c_ax = []
	y_med_ax = []
	y_stdev_ax = []
	y_c_stdev_ax = []

	x_pos_ax = [1,2,3,4]
	y_res_sum = [0, 0, 0, 0]
	y_res_count = [0, 0, 0, 0]

	x_points_ax = list(range(65, 86))
	y_points_ax = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# unpacks regular tournaments

	for tour in tours:
		x = Tournament.objects.get(id=tour.toutnament_id)
		y = (int(tour.r1), int(tour.r2), int(tour.r3), int(tour.r4), int(tour.r5))

		y_avg = round(sum(y) / len(y), 2)
		y_med = round(median(y), 2)
		y_stdev = round(stdev(y), 2)

		res_list = [tour.r1res, tour.r2res, tour.r3res, tour.r4res, tour.r5res]
		pos_list = [tour.r1pos, tour.r2pos, tour.r3pos, tour.r4pos, tour.r5pos]

		y_points_ax[tour.r1 - 65] += 1
		y_points_ax[tour.r2 - 65] += 1
		y_points_ax[tour.r3 - 65] += 1
		y_points_ax[tour.r4 - 65] += 1
		y_points_ax[tour.r5 - 65] += 1

		for res, pos in zip(res_list, pos_list):
			if pos == "No":
				continue
			else:
				if pos == '1p':
					y_res_sum[0] += res
					y_res_count[0] += 1
				elif pos == '1o':
					y_res_sum[1] += res
					y_res_count[1] += 1
				elif pos == '2p':
					y_res_sum[2] += res
					y_res_count[2] += 1
				elif pos == '2o':
					y_res_sum[3] += res
					y_res_count[3] += 1

		x_ax.append(datetime.combine(x.date_conducted, datetime.min.time()))
		x_c_ax.append(datetime.combine(x.date_conducted, datetime.min.time()))
		y_ax.append(y_avg)
		y_med_ax.append(y_med)
		y_stdev_ax.append(y_stdev)

# unpacks weird tournaments

	for w_tour in weird_tours:
		x = Tournament.objects.get(id=w_tour.tournament_id)
		y = (int(w_tour.r1), int(w_tour.r2), int(w_tour.r3), int(w_tour.r4), int(w_tour.r5), int(w_tour.r6))

		y_avg = round(sum(y) / len(y), 2)
		y_med = round(median(y), 2)
		y_stdev = round(stdev(y), 2)

		y_points_ax[w_tour.r1 - 66] += 1
		y_points_ax[w_tour.r2 - 66] += 1
		y_points_ax[w_tour.r3 - 66] += 1
		y_points_ax[w_tour.r4 - 66] += 1
		y_points_ax[w_tour.r5 - 66] += 1
		y_points_ax[w_tour.r6 - 66] += 1

		res_list = [w_tour.r1res, w_tour.r2res, w_tour.r3res, w_tour.r4res, w_tour.r5res, w_tour.r6res]
		pos_list = [w_tour.r1pos, w_tour.r2pos, w_tour.r3pos, w_tour.r4pos, w_tour.r5pos, w_tour.r6pos]

		for res, pos in zip(res_list, pos_list):
			if pos == "No":
				continue
			else:
				if pos == '1p':
					y_res_sum[0] += res
					y_res_count[0] += 1
				elif pos == '1o':
					y_res_sum[1] += res
					y_res_count[1] += 1
				elif pos == '2p':
					y_res_sum[2] += res
					y_res_count[2] += 1
				elif pos == '2o':
					y_res_sum[3] += res
					y_res_count[3] += 1

		x_ax.append(datetime.combine(x.date_conducted, datetime.min.time()))
		x_c_ax.append(datetime.combine(x.date_conducted, datetime.min.time()))
		y_ax.append(y_avg)
		y_med_ax.append(y_med)
		y_stdev_ax.append(y_stdev)

	for c_tour in cast_tours:
		x = Tournament.objects.get(id=c_tour.tournament_id)

		y_avg = c_tour.avg_res
		y_stdev = round(c_tour.stdev_res, 2)

		x_ax.append(datetime.combine(x.date_conducted, datetime.min.time()))
		y_ax.append(y_avg)
		y_stdev_ax.append(y_stdev)

	n = len(x_ax)
	n1 = len(x_c_ax)

	for i in range(n):
		for j in range(0, n-1):
			if x_ax[j] > x_ax[j + 1]:
				x_ax[j], x_ax[j + 1] = x_ax[j + 1], x_ax[j]
				y_ax[j], y_ax[j + 1] = y_ax[j + 1], y_ax[j]		
				y_stdev_ax[j], y_stdev_ax[j + 1] = y_stdev_ax[j + 1], y_stdev_ax[j]

	for l in range(n1):
		for c in range(0, n1-1):
			if x_c_ax[c] > x_c_ax[c + 1]:
				x_c_ax[c], x_c_ax[c + 1] = x_c_ax[c + 1], x_c_ax[c]
				y_med_ax[c], y_med_ax[c + 1] = y_med_ax[c + 1], y_med_ax[c]

# general average plot

	p = figure(
		y_range=(65, 85),
		title=f'Средние спикерские баллы за все турниры',
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

	avg = p.line(x_ax, y_ax, color='blue', line_width=3)
	avg_c = p.circle(x_ax, y_ax, color='blue', size=10)

	p.yaxis[0].formatter = NumeralTickFormatter(format="00.00")
	p.xaxis[0].formatter = DatetimeTickFormatter(months="%b %Y")

	tab1 = Panel(child=p, title='Среднее')

# median plot

	p_med = figure(
		y_range=(65, 85),
		title=f'Медианные спикерские баллы за все турниры',
		tools=[HoverTool()],
		tooltips='В этом турнире вы получили медианный спикерский @y',
		sizing_mode='stretch_width',
		height=450,
		x_axis_label='Турниры',
		y_axis_label='Спикерские'
		)

	p_med.toolbar.autohide = True
	p_med.title_location = 'above'
	p_med.title.text_font_size = "25px"
	p_med.title.align = "center"
	p_med.title.text_color = "black"

	p_med.line(x_c_ax, y_med_ax, color='blue', line_width=3)
	p_med.circle(x_c_ax, y_med_ax, color='blue', size=10)

	p_med.yaxis[0].formatter = NumeralTickFormatter(format="00.00")
	p_med.xaxis[0].formatter = DatetimeTickFormatter(months="%b %Y")

	tab2 = Panel(child=p_med, title='Медианное')

# standart deviation plot

	p_stdev = figure(
		title=f'Стандартное отклонение спикерских баллов за все турниры',
		tools=[HoverTool()],
		tooltips='В этом турнире стандартное отклонение составило @y',
		sizing_mode='stretch_width',
		height=450,
		x_axis_label='Турниры',
		y_axis_label='Спикерские'
		)

	p_stdev.toolbar.autohide = True
	p_stdev.title_location = 'above'
	p_stdev.title.text_font_size = "25px"
	p_stdev.title.align = "center"
	p_stdev.title.text_color = "black"

	p_stdev.line(x_ax, y_stdev_ax, color='blue', line_width=3)
	p_stdev.circle(x_ax, y_stdev_ax, color='blue', size=10)

	p_stdev.yaxis[0].formatter = NumeralTickFormatter(format="00.00")
	p_stdev.xaxis[0].formatter = DatetimeTickFormatter(months="%b %Y")

	tab3 = Panel(child=p_stdev, title='Стандартное отклонение')

	result = Tabs(tabs=[tab1, tab2, tab3])

	script, div = components(result)

# checks if there's any info about positions written in a database

	if y_res_sum != [0, 0, 0, 0]:
		y_res_ax = []
		for s, c in zip(y_res_sum, y_res_count):
			y_res_ax.append(round(s/c, 2))

# position-result relation bar-chart

		p_bar = figure(
			title='Колличество турнирных баллов в зависимости от позиции',
			tools=[HoverTool()],
			tooltips='Играя на @x вы набираете в среднем @y командных баллов',
			sizing_mode='stretch_width',
			height=450,
			x_axis_label='Позиции',
			y_axis_label='Баллы'
			)

		p_bar.toolbar.autohide = True
		p_bar.title_location = 'above'
		p_bar.title.text_font_size = "25px"
		p_bar.title.align = "center"
		p_bar.title.text_color = "black"

		p_bar.vbar(x=x_pos_ax, top=y_res_ax, width=0.5, bottom=0, color="blue")

		tab_stat2 = Panel(child=p_bar, title='Средний балл за позицию')
	else:

# shows a message if there's no data

		nodata = Div(
			text="""
			Играйте чаще, чтобы получить больше информации для аналитики. У нас нет записанных турниров, где сохранились ваши позиции по играм.
			""",
			width=800,
			height=100
			)
		lay = layout(
			[
				[nodata],
			]
			)
		tab_stat2 = Panel(child=lay, title='Средний балл за позицию')

# owerall times speaker got an amount of speaker points bar chart

	p_points_bar = figure(
			title='Сколько раз вы получали тот или иной балл:',
			tools=[HoverTool()],
			tooltips='Вы получили @x спикерских баллов @y раз',
			sizing_mode='stretch_width',
			height=450,
			x_axis_label='Баллы',
			y_axis_label='Количество'
			)

	p_points_bar.toolbar.autohide = True
	p_points_bar.title_location = 'above'
	p_points_bar.title.text_font_size = "25px"
	p_points_bar.title.align = "center"
	p_points_bar.title.text_color = "black"

	p_points_bar.vbar(x=x_points_ax, top=y_points_ax, width=0.5, bottom=0, color="blue")

	tab_stat1 = Panel(child=p_points_bar, title='Общее распределение спикерских')

	stat_result = Tabs(tabs=[tab_stat1, tab_stat2])

	script_stat, div_stat = components(stat_result)

	avg = round(sum(y_ax) / len(y_ax), 2)
	med = round(median(y_ax), 2)
	st_dev = round(round(stdev(y_ax), 2), 2)

	return_dict = {
		'div': div,
		'script': script,
		'div_stat': div_stat,
		'script_stat': script_stat,
		'avg': avg,
		'med': med,
		'st_dev': st_dev
	}

	return return_dict