from celery import shared_task
from MeteoLib.SQLMeasurements import DBManager
from MeteoLib.ExecuteMeasur import execute_measurements

@shared_task
def routine_measur():
	data = execute_measurements()
	db = DBManager()
	db.add_measurement(data.temperature, data.pressure, data.light, data.date)
