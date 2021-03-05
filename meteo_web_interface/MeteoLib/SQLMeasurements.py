import sqlalchemy as SA
from sqlalchemy.ext.declarative import declarative_base
import os
from collections import namedtuple

Base = declarative_base()

class Measurement(Base):
	__tablename__ = 'measurement'

	id = SA.Column(SA.Integer, primary_key=True)
	temperature = SA.Column(SA.Float)
	pressure = SA.Column(SA.Float)
	light = SA.Column(SA.Float)
	date_time = SA.Column(SA.DateTime)

	def __repr__(self):
		return f'<Measurement(Date: {self.date_time}, temp: {temperature}, pr: {pressure}, light: {light})>'


class DBManager:

	db_user = os.getenv('DB_USER')
	db_password = os.getenv('DB_PASSWORD')
	db_name = os.getenv('DB_NAME')
	db_host = os.getenv('DB_HOST')
	db_port = os.getenv('DB_PORT')

	def __init__(self):
		engine_url = f'postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'
		self.psql_engine = SA.create_engine(engine_url)
		Base.metadata.create_all(self.psql_engine) # create tables
		Session = SA.orm.sessionmaker(bind=self.psql_engine)
		self.session = Session()

	def add_measurement(self, temp, pressure, light, date):
		measur = Measurement(temperature=temp, pressure=pressure, light=light, date_time=date)
		self.session.add(measur)
		self.session.commit()

	def read_last_measurement(self):
		Data = namedtuple('last_row', ['id', 'date', 'temperature', 'pressure', 'light'])
		instance = self.session.query(Measurement).order_by(SA.desc(Measurement.date_time)).first()
		last_row = Data(instance.id, instance.date_time, instance.temperature, instance.pressure, instance.light)
		return last_row

	def read_all_temperature(self):
		Data = namedtuple('only_temperature', ['date', 'temperature'])
		result = []
		for temp, date in self.session.query(Measurement.temperature, Measurement.date_time):
			result.append(Data(date, temp))
		return result

	def read_all_pressure(self):
		Data = namedtuple('only_pressure', ['date', 'pressure'])
		result = []
		for pressure, date in self.session.query(Measurement.pressure, Measurement.date_time):
			result.append(Data(date, pressure))
		return result

	def read_all_light(self):
		Data = namedtuple('only_light', ['date', 'light'])
		result = []
		for light, date in self.session.query(Measurement.light, Measurement.date_time):
			result.append(Data(date, light))
		return result
