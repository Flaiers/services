from aiogram.dispatcher.filters.state import StatesGroup, State


class Document(StatesGroup):
	price = State()


class Сhoice(StatesGroup):
	text_city = State()
	text_serv = State()
	text_exec = State()


class NewCity(StatesGroup):
	city = State()

	service1 = State()
	service2 = State()
	service3 = State()
	service4 = State()
	service5 = State()

# относящиеся к 1 сервису
	executor11_name = State()
	executor11_pay = State()
	executor11_info = State()
	executor11_sup = State()

	executor21_name = State()
	executor21_pay = State()
	executor21_info = State()
	executor21_sup = State()

	executor31_name = State()
	executor31_pay = State()
	executor31_info = State()
	executor31_sup = State()

# относящиеся ко 2 сервису
	executor12_name = State()
	executor12_pay = State()
	executor12_info = State()
	executor12_sup = State()

	executor22_name = State()
	executor22_pay = State()
	executor22_info = State()
	executor22_sup = State()

	executor32_name = State()
	executor32_pay = State()
	executor32_info = State()
	executor32_sup = State()

# относящиеся к 3 сервису
	executor13_name = State()
	executor13_pay = State()
	executor13_info = State()
	executor13_sup = State()

	executor23_name = State()
	executor23_pay = State()
	executor23_info = State()
	executor23_sup = State()

	executor33_name = State()
	executor33_pay = State()
	executor33_info = State()
	executor33_sup = State()

# относящиеся к 4 сервису
	executor14_name = State()
	executor14_pay = State()
	executor14_info = State()
	executor14_sup = State()

	executor24_name = State()
	executor24_pay = State()
	executor24_info = State()
	executor24_sup = State()

	executor34_name = State()
	executor34_pay = State()
	executor34_info = State()
	executor34_sup = State()

# относящиеся к 5 сервису
	executor15_name = State()
	executor15_pay = State()
	executor15_info = State()
	executor15_sup = State()

	executor25_name = State()
	executor25_pay = State()
	executor25_info = State()
	executor25_sup = State()

	executor35_name = State()
	executor35_pay = State()
	executor35_info = State()
	executor35_sup = State()