from MeteoLib.LightBH1750Lib import BH1750
from MeteoLib.TempPreBMP180Lib import BMP180
from MeteoLib.SQLMeasurements import DBManager
import datetime

bmp180 = BMP180(1)
bh1750 = BH1750(1)

dec2_light = round(bh1750.read_light(), 2) # 1 lx
dec2_temp = round(bmp180.get_temperature(), 2) # 1 C
dec2_pressure = round(bmp180.get_pressure(), 2) # 1 Pa

print('Light intensity:', dec2_light, 'lx')
print('Temperature:', dec2_temp, 'C')
print('Pressure:', round(dec2_pressure * 0.01, 2), 'hPa')

db = DBManager()
db.add_measurement(dec2_temp, dec2_pressure, dec2_light, datetime.datetime.now())
