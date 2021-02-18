from gino import Gino
from gino.schema import GinoSchemaVisitor
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy import sql

from config import db_user, db_pass, host

db = Gino()

class Price(db.Model):
    __tablename__ = 'price'
    query: sql.Select

    id = Column(Integer(), Sequence('user_id_seq'), primary_key=True)
    url = Column(String(50))

    def __repr__(self):
        return "<Price(id='{}', url='{}')>".format(self.id, self.url)


class Item(db.Model):
    __tablename__ = 'items'
    query: sql.Select

    id = Column(Integer(), Sequence('user_id_seq'), primary_key=True)
    
    city = Column(String(20))

    service1 = Column(String(20))
    service2 = Column(String(20), default='Параметра нет')
    service3 = Column(String(20), default='Параметра нет')
    service4 = Column(String(20), default='Параметра нет')
    service5 = Column(String(20), default='Параметра нет')

# относящиеся к 1 сервису
    executor11_name = Column(String(20))
    executor11_pay = Column(String(20))
    executor11_info = Column(String(20))
    executor11_sup = Column(String(20))

    executor21_name = Column(String(20), default='Параметра нет')
    executor21_pay = Column(String(20), default='Параметра нет')
    executor21_info = Column(String(20), default='Параметра нет')
    executor21_sup = Column(String(20), default='Параметра нет')

    executor31_name = Column(String(20), default='Параметра нет')
    executor31_pay = Column(String(20), default='Параметра нет')
    executor31_info = Column(String(20), default='Параметра нет')
    executor31_sup = Column(String(20), default='Параметра нет')

# относящиеся ко 2 сервису
    executor12_name = Column(String(20), default='Параметра нет')
    executor12_pay = Column(String(20), default='Параметра нет')
    executor12_info = Column(String(20), default='Параметра нет')
    executor12_sup = Column(String(20), default='Параметра нет')

    executor22_name = Column(String(20), default='Параметра нет')
    executor22_pay = Column(String(20), default='Параметра нет')
    executor22_info = Column(String(20), default='Параметра нет')
    executor22_sup = Column(String(20), default='Параметра нет')

    executor32_name = Column(String(20), default='Параметра нет')
    executor32_pay = Column(String(20), default='Параметра нет')
    executor32_info = Column(String(20), default='Параметра нет')
    executor32_sup = Column(String(20), default='Параметра нет')

# относящиеся к 3 сервису
    executor13_name = Column(String(20), default='Параметра нет')
    executor13_pay = Column(String(20), default='Параметра нет')
    executor13_info = Column(String(20), default='Параметра нет')
    executor13_sup = Column(String(20), default='Параметра нет')

    executor23_name = Column(String(20), default='Параметра нет')
    executor23_pay = Column(String(20), default='Параметра нет')
    executor23_info = Column(String(20), default='Параметра нет')
    executor23_sup = Column(String(20), default='Параметра нет')

    executor33_name = Column(String(20), default='Параметра нет')
    executor33_pay = Column(String(20), default='Параметра нет')
    executor33_info = Column(String(20), default='Параметра нет')
    executor33_sup = Column(String(20), default='Параметра нет')

# относящиеся к 4 сервису
    executor14_name = Column(String(20), default='Параметра нет')
    executor14_pay = Column(String(20), default='Параметра нет')
    executor14_info = Column(String(20), default='Параметра нет')
    executor14_sup = Column(String(20), default='Параметра нет')

    executor24_name = Column(String(20), default='Параметра нет')
    executor24_pay = Column(String(20), default='Параметра нет')
    executor24_info = Column(String(20), default='Параметра нет')
    executor24_sup = Column(String(20), default='Параметра нет')

    executor34_name = Column(String(20), default='Параметра нет')
    executor34_pay = Column(String(20), default='Параметра нет')
    executor34_info = Column(String(20), default='Параметра нет')
    executor34_sup = Column(String(20), default='Параметра нет')

# относящиеся к 4 сервису
    executor15_name = Column(String(20), default='Параметра нет')
    executor15_pay = Column(String(20), default='Параметра нет')
    executor15_info = Column(String(20), default='Параметра нет')
    executor15_sup = Column(String(20), default='Параметра нет')

    executor25_name = Column(String(20), default='Параметра нет')
    executor25_pay = Column(String(20), default='Параметра нет')
    executor25_info = Column(String(20), default='Параметра нет')
    executor25_sup = Column(String(20), default='Параметра нет')

    executor35_name = Column(String(20), default='Параметра нет')
    executor35_pay = Column(String(20), default='Параметра нет')
    executor35_info = Column(String(20), default='Параметра нет')
    executor35_sup = Column(String(20), default='Параметра нет')

    def __repr__(self):
        return "<Item(id='{}', city='{}', service1='{}', service2='{}', service3='{}', service4='{}', service5='{}', executor11_name='{}', executor11_pay='{}', executor11_info='{}', executor11_sup='{}', executor21_name='{}', executor21_pay='{}', executor21_info='{}', executor21_sup='{}', executor31_name='{}', executor31_pay='{}', executor31_info='{}', executor31_sup='{}', executor12_name='{}', executor12_pay='{}', executor12_info='{}', executor12_sup='{}', executor22_name='{}', executor22_pay='{}', executor22_info='{}', executor22_sup='{}', executor32_name='{}', executor32_pay='{}', executor32_info='{}', executor32_sup='{}', executor13_name='{}', executor13_pay='{}', executor13_info='{}', executor13_sup='{}', executor23_name='{}', executor23_pay='{}', executor23_info='{}', executor23_sup='{}', executor33_name='{}', executor33_pay='{}', executor33_info='{}', executor33_sup='{}', executor14_name='{}', executor14_pay='{}', executor14_info='{}', executor14_sup='{}', executor24_name='{}', executor24_pay='{}', executor24_info='{}', executor24_sup='{}', executor34_name='{}', executor34_pay='{}', executor34_info='{}', executor34_sup='{}', executor15_name='{}', executor15_pay='{}', executor15_info='{}', executor15_sup='{}', executor25_name='{}', executor25_pay='{}', executor25_info='{}', executor25_sup='{}', executor35_name='{}', executor35_pay='{}', executor35_info='{}', executor35_sup='{}')>".format(
            self.id, self.city, self.service1, self.service2, self.service3, self.service4, self.service5, self.executor11_name, self.executor11_pay, self.executor11_info, self.executor11_sup, self.executor21_name, self.executor21_pay, self.executor21_info, self.executor21_sup, self.executor31_name, self.executor31_pay, self.executor31_info, self.executor31_sup, 
            self.executor12_name, self.executor12_pay, self.executor12_info, self.executor12_sup, self.executor22_name, self.executor22_pay, self.executor22_info, self.executor22_sup, self.executor32_name, self.executor32_pay, self.executor32_info, self.executor32_sup, self.executor13_name, self.executor13_pay, self.executor13_info, self.executor13_sup,
            self.executor23_name, self.executor23_pay, self.executor23_info, self.executor23_sup, self.executor33_name, self.executor33_pay, self.executor33_info, self.executor33_sup, self.executor14_name, self.executor14_pay, self.executor14_info, self.executor14_sup, self.executor24_name, self.executor24_pay, self.executor24_info, self.executor24_sup,
            self.executor34_name, self.executor34_pay, self.executor34_info, self.executor34_sup, self.executor15_name, self.executor15_pay, self.executor15_info, self.executor15_sup, self.executor25_name, self.executor25_pay, self.executor25_info, self.executor25_sup, self.executor35_name, self.executor35_pay, self.executor35_info, self.executor35_sup)

async def create_db():
    await db.set_bind(f'postgresql://{db_user}:{db_pass}@{host}/gino')
    # Create tables
    db.gino: GinoSchemaVisitor
    await db.gino.drop_all()
    await db.gino.create_all()