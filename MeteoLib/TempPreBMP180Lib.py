from smbus2 import SMBus
from copy import deepcopy
from time import sleep


class BMP180:
	_address = 0x77 # Sensor I2C address
	_reg_size = 2
	_ctrl_reg = 0xF4
	_result_reg_first = 0xF6
	_OSS = 1 # oversampling, standard mode

	_cal_reg_addr = {
		'ac1': (0xAA, "signed"),
		'ac2': (0xAC, "signed"),
		'ac3': (0xAE, "signed"),
		'ac4': (0xB0, "unsigned"),
		'ac5': (0xB2, "unsigned"),
		'ac6': (0xB4, "unsigned"),
		'b1': (0xB6, "signed"),
		'b2': (0xB8, "signed"),
		'mb': (0xBA, "signed"),
		'mc': (0xBC, "signed"),
		'md': (0xBE, "signed"),
	} # Addresses of regs that contain values required to callibrate sensor

	def __init__(self, i2c_bus_number):
		self.i2c_bus_number = i2c_bus_number
		self.bus = SMBus(i2c_bus_number) # Use correct I2C bus
		self.cal_values = self.read_calibration_data()

	def _read_short_number_signed(self, offset):
		# Read given amount of registers (BMP180.reg_size), beginning from first (offest), from sensor with addres (BMP180._address)
		msb, lsb = self.bus.read_i2c_block_data(BMP180._address, offset, BMP180._reg_size)

		return int.from_bytes(bytes((msb,lsb)), byteorder='big', signed=True) # return signed 16 bit int

	def _read_short_number_unsigned(self, offset):
		msb, lsb = self.bus.read_i2c_block_data(BMP180._address, offset, BMP180._reg_size)

		return int.from_bytes(bytes((msb, lsb)), byteorder='big', signed=False) # return unsigned 16 bit int

	def read_calibration_data(self):
		cal_values = {}
		for cal_var, reg_data in BMP180._cal_reg_addr.items():
			if reg_data[1] == "signed":
				cal_values[cal_var] = self._read_short_number_signed(reg_data[0]) # Read int hidden behind register given in self._cal_reg_addr
			else:
				cal_values[cal_var] = self._read_short_number_unsigned(reg_data[0])
		return cal_values

	def get_uncompensated_temperature(self):
		self.bus.write_byte_data(BMP180._address, BMP180._ctrl_reg, 0x2E) # Signal that we want temperature data

		sleep(0.005) # wait 5ms

		u_temp = self._read_short_number_unsigned(BMP180._result_reg_first)
		return u_temp

	def get_uncompensated_pressure(self):
		self.bus.write_byte_data(BMP180._address, BMP180._ctrl_reg, 0x34 + (BMP180._OSS << 6))

		sleep(0.008) # wait 8ms for sure, 7.5ms for standard mode OSS=1

		msb_lsb = self._read_short_number_unsigned(BMP180._result_reg_first)
		xlsb = self.bus.read_byte_data(BMP180._address, BMP180._result_reg_first + 2)

		return (msb_lsb << 8 | xlsb) >> (8 - BMP180._OSS)

	def get_temperature(self):
		u_temp = self.get_uncompensated_temperature()
		x1 = (u_temp - self.cal_values.get('ac6')) * self.cal_values.get('ac5') / pow(2,15)
		x2 = (self.cal_values.get('mc') * pow(2,11)) / (x1 + self.cal_values.get('md'))
		b5 = x1 + x2
		return (b5 + 8) / pow(2,4) / 10 # temp in 0.1 C so we need to divide by 10 to get 1 C

	def get_pressure(self):
		# variables from calculating temperature are required to calculate pressure (actually b5 is only required but you need u_temp, x1, x2 to calculate this)
		u_temp = self.get_uncompensated_temperature()
		x1 = (u_temp - self.cal_values.get('ac6')) * self.cal_values.get('ac5') / pow(2,15)
		x2 = (self.cal_values.get('mc') * pow(2,11)) / (x1 + self.cal_values.get('md'))
		b5 = x1 + x2

		b6 = b5 - 4000
		x1 = (self.cal_values.get('b1') * (b6 * b6 / pow(2,12)))/ pow(2,11)
		x2 = self.cal_values.get('ac2') * b6 / pow(2,11)
		x3 = x1 + x2

		b3 = (((self.cal_values.get('ac1') * 4 + int(x3)) << BMP180._OSS) + 2) / 4
		x1 = self.cal_values.get('ac3') * b6 / pow(2,13)
		x2 = (self.cal_values.get('b1') * (b6 * b6 / pow(2,12))) / pow(2,16)
		x3 = ((x1 + x2) + 2) / pow(2, 2)

		b4 = self.cal_values.get('ac4') * (x3 + 32768) / pow(2,15)
		u_pr = self.get_uncompensated_pressure()
		b7 = (u_pr - b3) * (50000 >> BMP180._OSS )
		if b7 < 0x80000000:
			p = (b7 * 2) / b4
		else:
			p = (b7 / b4) * 2

		x1 = (p / pow(2,8)) * (p / pow(2,8))
		x1 = (x1 * 3038) / pow(2,16)
		x2 = (-7357 * p) / pow(2,16)

		return p + (x1 + x2 + 3791) / pow(2,4)

	def __repr__(self):
		return f'<BMP180 I2C Bus: {self.i2c_bus_number}>'

	def __str__(self):
		return f'BMP180 light intensity sensor I2C bus: {self.i2c_bus_number}'
