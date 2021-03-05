from django.shortcuts import render
import MeteoLib.SQLMeasurements as ML
from MeteoLib.CalculateStats import calculate_average, narrow_date_range
from MeteoLib.ExecuteMeasur import execute_measurements
import datetime


def temperature_view(request):
	db = ML.DBManager()
	data = db.read_all_temperature()

	measur_now = execute_measurements()

	# dates
	now = datetime.datetime.now()
	today = now.replace(hour=0, minute=0, second=0, microsecond=0)
	start_yesterday = today - datetime.timedelta(days=1)
	finish_yesterday = start_yesterday.replace(hour=23, minute=59, second=59, microsecond=999)
	start_week = (now - datetime.timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
	start_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
	start_year = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

	# avg
	# today
	avg_today = calculate_average(narrow_date_range(data, today, now) , 1)
	# yesterday
	avg_yesterday = calculate_average(narrow_date_range(data, start_yesterday, finish_yesterday) , 1)
	# this week
	avg_week = calculate_average(narrow_date_range(data, start_week, now) , 1)
	# this month
	avg_month = calculate_average(narrow_date_range(data, start_month, now) , 1)
	# this year
	avg_year = calculate_average(narrow_date_range(data, start_year, now) , 1)
	return render(request, 'index.html', context={'data': data, 'title': 'Temperature measurements',
							'avg_today': round(avg_today, 2),
							'avg_yesterday': round(avg_yesterday, 2),
							'avg_week': round(avg_week, 2),
							'avg_month': round(avg_month, 2),
							'avg_year': round(avg_year, 2),
							'all_title': 'Temperature measurement',
							'avg_title': 'Average temperature',
							'unit': '&#176;C',
							'main_title': 'Temperature',
							'last': measur_now})

def pressure_view(request):
        db = ML.DBManager()
        data = db.read_all_pressure()

        measur_now = execute_measurements()

        # dates
        now = datetime.datetime.now()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start_yesterday = today - datetime.timedelta(days=1)
        finish_yesterday = start_yesterday.replace(hour=23, minute=59, second=59, microsecond=999)
        start_week = (now - datetime.timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        start_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        start_year = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

        # avg
        # today
        avg_today = calculate_average(narrow_date_range(data, today, now) , 1)
        # yesterday
        avg_yesterday = calculate_average(narrow_date_range(data, start_yesterday, finish_yesterday) , 1)
        # this week
        avg_week = calculate_average(narrow_date_range(data, start_week, now) , 1)
        # this month
        avg_month = calculate_average(narrow_date_range(data, start_month, now) , 1)
        # this year
        avg_year = calculate_average(narrow_date_range(data, start_year, now) , 1)
        return render(request, 'index.html', context={'data': data, 'title': 'Pressure measurements',
                                                        'avg_today': round(avg_today, 2),
                                                        'avg_yesterday': round(avg_yesterday, 2),
                                                        'avg_week': round(avg_week, 2),
                                                        'avg_month': round(avg_month, 2),
                                                        'avg_year': round(avg_year, 2),
                                                        'all_title': 'Pressure measurement',
                                                        'avg_title': 'Average pressure',
                                                        'unit': 'Pa',
                                                        'main_title': 'Pressure',
							'last': measur_now})

def light_view(request):
        db = ML.DBManager()
        data = db.read_all_light()

        measur_now = execute_measurements()

        # dates
        now = datetime.datetime.now()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start_yesterday = today - datetime.timedelta(days=1)
        finish_yesterday = start_yesterday.replace(hour=23, minute=59, second=59, microsecond=999)
        start_week = (now - datetime.timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        start_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        start_year = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

        # avg
        # today
        avg_today = calculate_average(narrow_date_range(data, today, now) , 1)
        # yesterday
        avg_yesterday = calculate_average(narrow_date_range(data, start_yesterday, finish_yesterday) , 1)
        # this week
        avg_week = calculate_average(narrow_date_range(data, start_week, now) , 1)
        # this month
        avg_month = calculate_average(narrow_date_range(data, start_month, now) , 1)
        # this year
        avg_year = calculate_average(narrow_date_range(data, start_year, now) , 1)
        return render(request, 'index.html', context={'data': data, 'title': 'Light measurements',
                                                        'avg_today': round(avg_today, 2),
                                                        'avg_yesterday': round(avg_yesterday, 2),
                                                        'avg_week': round(avg_week, 2),
                                                        'avg_month': round(avg_month, 2),
                                                        'avg_year': round(avg_year, 2),
                                                        'all_title': 'Light intensity measurement',
                                                        'avg_title': 'Average light intensity',
                                                        'unit': 'lx',
                                                        'main_title': 'Light intensity',
							'last': measur_now})
