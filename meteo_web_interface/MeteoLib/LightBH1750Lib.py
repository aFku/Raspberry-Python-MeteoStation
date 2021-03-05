from smbus2 import SMBus
from time import sleep

class BH1750:
	_address = 0x23 # I2C address
	_one_time_meas_05lx_res_mode = 0x21 # value to execute one time measurement with resolution 0.5lx . After that sensor set Power Down mode. Typical sleep = 120ms
	_data_bytes = 2 # Data are stored on 2 bytes

	def __init__(self, i2c_bus_number):
		self.i2c_bus_number = i2c_bus_number
		self.bus = SMBus(i2c_bus_number) # Use correct I2C bus

	def execute_measurement(self):
		self.bus.write_byte(BH1750._address, BH1750._one_time_meas_05lx_res_mode)
		sleep(0.13) # wait 130ms for sure. After that you can read result

	def read_light(self):
		self.execute_measurement()
		data = self.bus.read_i2c_block_data(BH1750._address, BH1750._one_time_meas_05lx_res_mode, self._data_bytes) # return list of two values
		light = data[0] << 8 | data[1] # move first 8 bits left and put second byte in their old location
		light = light / 1.2 # calculation from docs
		return light

	def __repr__(self):
		return f'<BH1750 I2C Bus: {self.i2c_bus_number}>'

	def __str__(self):
		return f'BH1750 light intensity sensor I2C bus: {self.i2c_bus_number}'

	def __int__(self):
		return self.read_light
