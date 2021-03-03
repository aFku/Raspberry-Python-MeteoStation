import sqlalchemy as SA
from sqlalchemy.ext.declarative import declarative_base
import os

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
