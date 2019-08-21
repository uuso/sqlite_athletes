import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

BASE_PATH = "sqlite:///sochi_athletes.sqlite3"

Base = declarative_base()

	# CREATE TABLE user(
	# "id" integer primary key autoincrement, 
	# "first_name" text, 
	# "last_name" text, 
	# "gender" text, 
	# "email" text, 
	# "birthdate" text, 
	# "height" real);

def db_connect():
	engine = sa.create_engine(BASE_PATH)
	Base.metadata.create_all(engine)
	session = sessionmaker(engine)
	return session()

class User(Base):
	__tablename__ = 'user'
	id = sa.Column(sa.Integer, primary_key = True)
	first_name = sa.Column(sa.Text)
	last_name = sa.Column(sa.Text)
	gender = sa.Column(sa.Text)
	email = sa.Column(sa.Text)
	birthdate = sa.Column(sa.Text)
	height = sa.Column(sa.Float)

def new_user():
	print('Were going to add new object. Please answer these questions:')
	first_name = input("Enter first_name: ")
	last_name = input("Enter last_name: ")
	gender = input("Enter gender: ")
	email = input("Enter email: ")
	birthdate = input("Enter birthdate [YYYY-MM-DD]: ")
	height = input("Enter height [1.76]: ")
	return User(
		first_name=first_name,
		last_name=last_name,
		gender=gender,
		email=email,
		birthdate=birthdate,
		height=height
		)


def add_user_to_db():
	session = db_connect()
	session.add(new_user())
	session.commit()
	print('OK')

def get_user_by_id(id):
	session = db_connect()
	return session.query(User).filter(User.id == id).first()

if __name__ == '__main__':
	add_user_to_db()
