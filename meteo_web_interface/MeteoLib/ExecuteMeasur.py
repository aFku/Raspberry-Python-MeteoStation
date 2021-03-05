from .LightBH1750Lib import BH1750
from .TempPreBMP180Lib import BMP180
import datetime
from collections import namedtuple

def execute_measurements():
	# init sensors controllers
	bh1750 = BH1750(1)
	bmp180 = BMP180(1)

	# measur
	light = round(bh1750.read_light(), 2)
	temperature = round(bmp180.get_temperature(), 2)
	pressure = round(bmp180.get_pressure(), 2)

	#meta-data
	date = datetime.datetime.now()

	Data = namedtuple('measurement', ['date', 'temperature', 'pressure', 'light'])
	return Data(date, temperature, pressure, light)
