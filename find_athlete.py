import users
from datetime import datetime as dt
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import time

# Напишите модуль find_athlete.py поиска ближайшего к пользователю атлета. Логика работы модуля такова:

# запросить идентификатор пользователя;
# если пользователь с таким идентификатором существует в таблице user, 
# то вывести на экран двух атлетов: 
#	ближайшего по дате рождения к данному пользователю 
#	ближайшего по росту к данному пользователю;
# если пользователя с таким идентификатором нет, вывести соответствующее сообщение.

class Athlete(users.Base):
	# CREATE TABLE athelete(
	# "id" integer primary key autoincrement, 
	# "age" integer,
	# "birthdate" text,
	# "gender" text,
	# "height" real,
	# "name" text,
	# "weight" integer,
	# "gold_medals" integer,
	# "silver_medals" integer,
	# "bronze_medals" integer,
	# "total_medals" integer,
	# "sport" text,
	# "country" text);
	__tablename__ = 'athelete'
	id = sa.Column(sa.Integer, primary_key=True)
	age = sa.Column(sa.Integer)
	birthdate = sa.Column(sa.Text)
	gender = sa.Column(sa.Text)
	height = sa.Column(sa.Float)
	name = sa.Column(sa.Text)
	weight = sa.Column(sa.Integer)
	gold_medals = sa.Column(sa.Integer)
	silver_medals = sa.Column(sa.Integer)
	bronze_medals = sa.Column(sa.Integer)
	total_medals = sa.Column(sa.Integer)
	sport = sa.Column(sa.Text)
	country = sa.Column(sa.Text)

def get_elem_by_nearest(iterable, attr, value, ret_attr):
	nearest = None

	for _ in iterable:
		"""
		Если первый - берём его, или если текущий ближе к искомому - опять же берем его.
		Не умеет работать с датами - только типы у которых есть встроенное сравнение и вычитание.
		"""
		if nearest is None or (getattr(_, attr) is not None and abs(value - getattr(_, attr)) < abs(value - nearest["value"])):
			nearest = {"value": getattr(_, attr), "return": getattr(_, ret_attr)}

	return nearest["return"] if nearest else None		

def get_athlete_info_by_nearest_height(height):
	session = users.db_connect()
	athletes = session.query(Athlete)

	by_height = get_elem_by_nearest(athletes.all(), attr = "height", value = height, ret_attr = "id") # ищем подходящий id

	return session.query(Athlete).filter(Athlete.id == by_height).first() # ищем элемент с этим id


def get_athlete_info_by_nearest_birthdate(birthdate):
	birthdate = dt.strptime(birthdate, "%Y-%m-%d")

	session = users.db_connect()
	athletes = session.query(Athlete)

	nearest = None
	for athlete in athletes.all():
		if athlete.birthdate is not None:
			athlete_birth = dt.strptime(athlete.birthdate, "%Y-%m-%d")
			if nearest is None or abs(birthdate - athlete_birth) < abs(birthdate - nearest["value"]):				
				nearest = {"value": athlete_birth, "athlete": athlete}
	
	return nearest["athlete"] if nearest else None




def find_athletes():
	profile = users.get_user_by_id(int(input("Введите искомый id пользователя: ")))
	if not profile:
		print("Искомый пользователь в базе не найден.")
		return

	by_height = get_athlete_info_by_nearest_height(float(profile.height)) 
	by_birthdate = get_athlete_info_by_nearest_birthdate(profile.birthdate)

	print_attr = ["name", "gender", "birthdate", "height", "country", "sport", "total_medals"]

	print(f"Дата рождения пользователя - {profile.birthdate}, его рост - {float(profile.height)}.")

	print('Ближайший атлет по росту:')
	if by_height:
		print({attr: getattr(by_height, attr) for attr in print_attr})
	else:
		print('Вероятно база атлетов пуста.')

	print('Ближайший атлет по дате рождения:')
	if by_height:
		print({attr: getattr(by_birthdate, attr) for attr in print_attr})
	else:
		print('Вероятно база атлетов пуста.')
	


if __name__ == '__main__':
	find_athletes()