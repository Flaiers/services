import database
import kb

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
                    InlineKeyboardMarkup, InlineKeyboardButton
from database import Item, Price
from states import NewCity, Сhoice, Document
from load_all import dp, bot


# страртовый диалог
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	await message.answer('Начать пользоваться, нажми /choice\n'
		'Узнать 📋 Прайс-лист, нажми на кнопку ниже',
		reply_markup=kb.reply_price)


@dp.message_handler(commands=['choice'])
async def show_items(message: types.Message):
    city1 = await Item.select('city').where(Item.id == 1).gino.scalar()
    city2 = await Item.select('city').where(Item.id == 2).gino.scalar()
    city3 = await Item.select('city').where(Item.id == 3).gino.scalar()

    button_city1 = KeyboardButton(f'{city1}')
    button_city2 = KeyboardButton(f'{city2}')
    button_city3 = KeyboardButton(f'{city3}')

    reply_city = ReplyKeyboardMarkup(resize_keyboard=True,
        one_time_keyboard=True).add(button_city1).add(button_city2, button_city3)
    await message.answer('Выбери город',
        reply_markup=reply_city)

    await Сhoice.text_city.set()

@dp.message_handler(state=Сhoice.text_city)
async def text_city(message: types.Message, state: FSMContext):
    text_city = message.text
    city1 = await Item.select('city').where(Item.id == 1).gino.scalar()
    city2 = await Item.select('city').where(Item.id == 2).gino.scalar()
    city3 = await Item.select('city').where(Item.id == 3).gino.scalar()

    serv11 = await Item.select('service1').where(Item.id == 1).gino.scalar()
    serv21 = await Item.select('service2').where(Item.id == 1).gino.scalar()
    serv31 = await Item.select('service3').where(Item.id == 1).gino.scalar()
    serv41 = await Item.select('service4').where(Item.id == 1).gino.scalar()
    serv51 = await Item.select('service5').where(Item.id == 1).gino.scalar()

    serv12 = await Item.select('service1').where(Item.id == 2).gino.scalar()
    serv22 = await Item.select('service2').where(Item.id == 2).gino.scalar()
    serv32 = await Item.select('service3').where(Item.id == 2).gino.scalar()
    serv42 = await Item.select('service4').where(Item.id == 2).gino.scalar()
    serv52 = await Item.select('service5').where(Item.id == 2).gino.scalar()

    serv13 = await Item.select('service1').where(Item.id == 3).gino.scalar()
    serv23 = await Item.select('service2').where(Item.id == 3).gino.scalar()
    serv33 = await Item.select('service3').where(Item.id == 3).gino.scalar()
    serv43 = await Item.select('service4').where(Item.id == 3).gino.scalar()
    serv53 = await Item.select('service5').where(Item.id == 3).gino.scalar()

    if text_city == city1:
        button_serv11 = KeyboardButton(f'{serv11}')
        button_serv21 = KeyboardButton(f'{serv21}')
        button_serv31 = KeyboardButton(f'{serv31}')
        button_serv41 = KeyboardButton(f'{serv41}')
        button_serv51 = KeyboardButton(f'{serv51}')
        reply_serv1 = ReplyKeyboardMarkup(resize_keyboard=True,
            one_time_keyboard=True).add(button_serv11).add(button_serv21, button_serv31).add(button_serv41, button_serv51)

        await message.answer(f'Ты выбрал город {city1}, сейчас выбери услугу',
            reply_markup=reply_serv1)

        await Сhoice.text_serv.set()
        await state.update_data(text_city1=text_city)

    elif text_city == city2:
        button_serv12 = KeyboardButton(f'{serv12}')
        button_serv22 = KeyboardButton(f'{serv22}')
        button_serv32 = KeyboardButton(f'{serv32}')
        button_serv42 = KeyboardButton(f'{serv42}')
        button_serv52 = KeyboardButton(f'{serv52}')
        reply_serv2 = ReplyKeyboardMarkup(resize_keyboard=True,
            one_time_keyboard=True).add(button_serv12).add(button_serv22, button_serv32).add(button_serv42, button_serv52)

        await message.answer(f'Ты выбрал город {city2}, сейчас выбери услугу',
            reply_markup=reply_serv2)

        await Сhoice.text_serv.set()
        await state.update_data(text_city2=text_city)
    
    elif text_city == city3:
        button_serv13 = KeyboardButton(f'{serv13}')
        button_serv23 = KeyboardButton(f'{serv23}')
        button_serv33 = KeyboardButton(f'{serv33}')
        button_serv43 = KeyboardButton(f'{serv43}')
        button_serv53 = KeyboardButton(f'{serv53}')
        reply_serv3 = ReplyKeyboardMarkup(resize_keyboard=True,
            one_time_keyboard=True).add(button_serv13).add(button_serv23, button_serv33).add(button_serv43, button_serv53)

        await message.answer(f'Ты выбрал город {city3}, сейчас выбери услугу',
            reply_markup=reply_serv3)

        await Сhoice.text_serv.set()
        await state.update_data(text_city3=text_city)


@dp.message_handler(state=Сhoice.text_serv)
async def text_serv(message: types.Message, state: FSMContext):
    text_serv = message.text
    serv11 = await Item.select('service1').where(Item.id == 1).gino.scalar()
    serv21 = await Item.select('service2').where(Item.id == 1).gino.scalar()
    serv31 = await Item.select('service3').where(Item.id == 1).gino.scalar()
    serv41 = await Item.select('service4').where(Item.id == 1).gino.scalar()
    serv51 = await Item.select('service5').where(Item.id == 1).gino.scalar()

    serv12 = await Item.select('service1').where(Item.id == 2).gino.scalar()
    serv22 = await Item.select('service2').where(Item.id == 2).gino.scalar()
    serv32 = await Item.select('service3').where(Item.id == 2).gino.scalar()
    serv42 = await Item.select('service4').where(Item.id == 2).gino.scalar()
    serv52 = await Item.select('service5').where(Item.id == 2).gino.scalar()

    serv13 = await Item.select('service1').where(Item.id == 3).gino.scalar()
    serv23 = await Item.select('service2').where(Item.id == 3).gino.scalar()
    serv33 = await Item.select('service3').where(Item.id == 3).gino.scalar()
    serv43 = await Item.select('service4').where(Item.id == 3).gino.scalar()
    serv53 = await Item.select('service5').where(Item.id == 3).gino.scalar()

# относящиеся к 1 сервису города 1
    exec111 = await Item.select('executor11_name').where(Item.id == 1).gino.scalar()
    exec211 = await Item.select('executor21_name').where(Item.id == 1).gino.scalar()
    exec311 = await Item.select('executor31_name').where(Item.id == 1).gino.scalar()
# относящиеся к 2 сервису города 1
    exec121 = await Item.select('executor12_name').where(Item.id == 1).gino.scalar()
    exec221 = await Item.select('executor22_name').where(Item.id == 1).gino.scalar()
    exec321 = await Item.select('executor32_name').where(Item.id == 1).gino.scalar()
# относящиеся к 3 сервису города 1
    exec131 = await Item.select('executor13_name').where(Item.id == 1).gino.scalar()
    exec231 = await Item.select('executor23_name').where(Item.id == 1).gino.scalar()
    exec331 = await Item.select('executor33_name').where(Item.id == 1).gino.scalar()
# относящиеся к 4 сервису города 1
    exec141 = await Item.select('executor14_name').where(Item.id == 1).gino.scalar()
    exec241 = await Item.select('executor24_name').where(Item.id == 1).gino.scalar()
    exec341 = await Item.select('executor34_name').where(Item.id == 1).gino.scalar()
# относящиеся к 5 сервису города 1
    exec151 = await Item.select('executor15_name').where(Item.id == 1).gino.scalar()
    exec251 = await Item.select('executor25_name').where(Item.id == 1).gino.scalar()
    exec351 = await Item.select('executor35_name').where(Item.id == 1).gino.scalar()

# относящиеся к 1 сервису города 2
    exec112 = await Item.select('executor11_name').where(Item.id == 2).gino.scalar()
    exec212 = await Item.select('executor21_name').where(Item.id == 2).gino.scalar()
    exec312 = await Item.select('executor31_name').where(Item.id == 2).gino.scalar()
# относящиеся к 2 сервису города 2
    exec122 = await Item.select('executor12_name').where(Item.id == 2).gino.scalar()
    exec222 = await Item.select('executor22_name').where(Item.id == 2).gino.scalar()
    exec322 = await Item.select('executor32_name').where(Item.id == 2).gino.scalar()
# относящиеся к 3 сервису города 2
    exec132 = await Item.select('executor13_name').where(Item.id == 2).gino.scalar()
    exec232 = await Item.select('executor23_name').where(Item.id == 2).gino.scalar()
    exec332 = await Item.select('executor33_name').where(Item.id == 2).gino.scalar()
# относящиеся к 4 сервису города 2
    exec142 = await Item.select('executor14_name').where(Item.id == 2).gino.scalar()
    exec242 = await Item.select('executor24_name').where(Item.id == 2).gino.scalar()
    exec342 = await Item.select('executor34_name').where(Item.id == 2).gino.scalar()
# относящиеся к 5 сервису города 2
    exec152 = await Item.select('executor15_name').where(Item.id == 2).gino.scalar()
    exec252 = await Item.select('executor25_name').where(Item.id == 2).gino.scalar()
    exec352 = await Item.select('executor35_name').where(Item.id == 2).gino.scalar()

# относящиеся к 1 сервису города 3
    exec113 = await Item.select('executor11_name').where(Item.id == 3).gino.scalar()
    exec213 = await Item.select('executor21_name').where(Item.id == 3).gino.scalar()
    exec313 = await Item.select('executor31_name').where(Item.id == 3).gino.scalar()
# относящиеся к 2 сервису города 3
    exec123 = await Item.select('executor12_name').where(Item.id == 3).gino.scalar()
    exec223 = await Item.select('executor22_name').where(Item.id == 3).gino.scalar()
    exec323 = await Item.select('executor32_name').where(Item.id == 3).gino.scalar()
# относящиеся к 3 сервису города 3
    exec133 = await Item.select('executor13_name').where(Item.id == 3).gino.scalar()
    exec233 = await Item.select('executor23_name').where(Item.id == 3).gino.scalar()
    exec333 = await Item.select('executor33_name').where(Item.id == 3).gino.scalar()
# относящиеся к 4 сервису города 3
    exec143 = await Item.select('executor14_name').where(Item.id == 3).gino.scalar()
    exec243 = await Item.select('executor24_name').where(Item.id == 3).gino.scalar()
    exec343 = await Item.select('executor34_name').where(Item.id == 3).gino.scalar()
# относящиеся к 5 сервису города 3
    exec153 = await Item.select('executor15_name').where(Item.id == 3).gino.scalar()
    exec253 = await Item.select('executor25_name').where(Item.id == 3).gino.scalar()
    exec353 = await Item.select('executor35_name').where(Item.id == 3).gino.scalar()

    if text_serv == serv11:
        button_exec111 = KeyboardButton(f'{exec111}')
        button_exec211 = KeyboardButton(f'{exec211}')
        button_exec311 = KeyboardButton(f'{exec311}')

        reply_exec11 = ReplyKeyboardMarkup(resize_keyboard=True,
            one_time_keyboard=True).add(button_exec111).add(button_exec211, button_exec311)
        await message.answer(f'Ты выбрал услугу {serv11}, сейчас выбери исполнителя',
            reply_markup=reply_exec11)

        await Сhoice.text_exec.set()
        await state.update_data(text_serv11=text_serv)

    elif text_serv == serv21:
        button_exec121 = KeyboardButton(f'{exec121}')
        button_exec221 = KeyboardButton(f'{exec221}')
        button_exec321 = KeyboardButton(f'{exec321}')

        reply_exec21 = ReplyKeyboardMarkup(resize_keyboard=True,
            one_time_keyboard=True).add(button_exec121).add(button_exec221, button_exec321)
        await message.answer(f'Ты выбрал услугу {serv21}, сейчас выбери исполнителя',
            reply_markup=reply_exec21)

        await Сhoice.text_exec.set()
        await state.update_data(text_serv21=text_serv)

    elif text_serv == serv31:
        button_exec131 = KeyboardButton(f'{exec131}')
        button_exec231 = KeyboardButton(f'{exec231}')
        button_exec331 = KeyboardButton(f'{exec331}')

        reply_exec31 = ReplyKeyboardMarkup(resize_keyboard=True,
            one_time_keyboard=True).add(button_exec131).add(button_exec231, button_exec331)
        await message.answer(f'Ты выбрал услугу {serv31}, сейчас выбери исполнителя',
            reply_markup=reply_exec31)

        await Сhoice.text_exec.set()
        await state.update_data(text_serv31=text_serv)

    elif text_serv == serv41:
        button_exec141 = KeyboardButton(f'{exec141}')
        button_exec241 = KeyboardButton(f'{exec241}')
        button_exec341 = KeyboardButton(f'{exec341}')

        reply_exec41 = ReplyKeyboardMarkup(resize_keyboard=True,
            one_time_keyboard=True).add(button_exec141).add(button_exec241, button_exec341)
        await message.answer(f'Ты выбрал услугу {serv41}, сейчас выбери исполнителя',
            reply_markup=reply_exec41)

        await Сhoice.text_exec.set()
        await state.update_data(text_serv41=text_serv)

    elif text_serv == serv51:
        button_exec151 = KeyboardButton(f'{exec151}')
        button_exec251 = KeyboardButton(f'{exec251}')
        button_exec351 = KeyboardButton(f'{exec351}')

        reply_exec51 = ReplyKeyboardMarkup(resize_keyboard=True,
            one_time_keyboard=True).add(button_exec151).add(button_exec251, button_exec351)
        await message.answer(f'Ты выбрал услугу {serv51}, сейчас выбери исполнителя',
            reply_markup=reply_exec51)

        await Сhoice.text_exec.set()
        await state.update_data(text_serv51=text_serv)

#####################################################################################################
#####################################################################################################


    elif text_serv == serv12:
        button_exec112 = KeyboardButton(f'{exec112}')
        button_exec212 = KeyboardButton(f'{exec212}')
        button_exec312 = KeyboardButton(f'{exec312}')

        reply_exec12 = ReplyKeyboardMarkup(resize_keyboard=True,
            one_time_keyboard=True).add(button_exec112).add(button_exec212, button_exec312)
        await message.answer(f'Ты выбрал услугу {serv12}, сейчас выбери исполнителя',
            reply_markup=reply_exec12)

        await Сhoice.text_exec.set()
        await state.update_data(text_serv12=text_serv)
    
    elif text_serv == serv22:
        button_exec122 = KeyboardButton(f'{exec122}')
        button_exec222 = KeyboardButton(f'{exec222}')
        button_exec322 = KeyboardButton(f'{exec322}')

        reply_exec22 = ReplyKeyboardMarkup(resize_keyboard=True,
            one_time_keyboard=True).add(button_exec122).add(button_exec222, button_exec322)
        await message.answer(f'Ты выбрал услугу {serv22}, сейчас выбери исполнителя',
            reply_markup=reply_exec22)

        await Сhoice.text_exec.set()
        await state.update_data(text_serv22=text_serv)

    elif text_serv == serv32:
        button_exec132 = KeyboardButton(f'{exec132}')
        button_exec232 = KeyboardButton(f'{exec232}')
        button_exec332 = KeyboardButton(f'{exec332}')

        reply_exec32 = ReplyKeyboardMarkup(resize_keyboard=True,
            one_time_keyboard=True).add(button_exec132).add(button_exec232, button_exec332)
        await message.answer(f'Ты выбрал услугу {serv32}, сейчас выбери исполнителя',
            reply_markup=reply_exec32)

        await Сhoice.text_exec.set()
        await state.update_data(text_serv32=text_serv)
    
    elif text_serv == serv42:
        button_exec142 = KeyboardButton(f'{exec142}')
        button_exec242 = KeyboardButton(f'{exec242}')
        button_exec342 = KeyboardButton(f'{exec342}')

        reply_exec42 = ReplyKeyboardMarkup(resize_keyboard=True,
            one_time_keyboard=True).add(button_exec142).add(button_exec242, button_exec342)
        await message.answer(f'Ты выбрал услугу {serv42}, сейчас выбери исполнителя',
            reply_markup=reply_exec42)

        await Сhoice.text_exec.set()
        await state.update_data(text_serv42=text_serv)

    elif text_serv == serv52:
        button_exec152 = KeyboardButton(f'{exec152}')
        button_exec252 = KeyboardButton(f'{exec252}')
        button_exec352 = KeyboardButton(f'{exec352}')

        reply_exec52 = ReplyKeyboardMarkup(resize_keyboard=True,
            one_time_keyboard=True).add(button_exec152).add(button_exec252, button_exec352)
        await message.answer(f'Ты выбрал услугу {serv52}, сейчас выбери исполнителя',
            reply_markup=reply_exec52)

        await Сhoice.text_exec.set()
        await state.update_data(text_serv52=text_serv)

#####################################################################################################
#####################################################################################################


    elif text_serv == serv13:
        button_exec113 = KeyboardButton(f'{exec113}')
        button_exec213 = KeyboardButton(f'{exec213}')
        button_exec313 = KeyboardButton(f'{exec313}')

        reply_exec13 = ReplyKeyboardMarkup(resize_keyboard=True,
            one_time_keyboard=True).add(button_exec113).add(button_exec213, button_exec313)
        await message.answer(f'Ты выбрал услугу {serv13}, сейчас выбери исполнителя',
            reply_markup=reply_exec13)

        await Сhoice.text_exec.set()
        await state.update_data(text_serv13=text_serv)
    
    elif text_serv == serv23:
        button_exec123 = KeyboardButton(f'{exec123}')
        button_exec223 = KeyboardButton(f'{exec223}')
        button_exec323 = KeyboardButton(f'{exec323}')

        reply_exec23 = ReplyKeyboardMarkup(resize_keyboard=True,
            one_time_keyboard=True).add(button_exec123).add(button_exec223, button_exec323)
        await message.answer(f'Ты выбрал услугу {serv22}, сейчас выбери исполнителя',
            reply_markup=reply_exec23)

        await Сhoice.text_exec.set()
        await state.update_data(text_serv23=text_serv)

    elif text_serv == serv33:
        button_exec133 = KeyboardButton(f'{exec133}')
        button_exec233 = KeyboardButton(f'{exec233}')
        button_exec333 = KeyboardButton(f'{exec333}')

        reply_exec33 = ReplyKeyboardMarkup(resize_keyboard=True,
            one_time_keyboard=True).add(button_exec133).add(button_exec233, button_exec333)
        await message.answer(f'Ты выбрал услугу {serv33}, сейчас выбери исполнителя',
            reply_markup=reply_exec33)

        await Сhoice.text_exec.set()
        await state.update_data(text_serv33=text_serv)
    
    elif text_serv == serv43:
        button_exec143 = KeyboardButton(f'{exec143}')
        button_exec243 = KeyboardButton(f'{exec243}')
        button_exec343 = KeyboardButton(f'{exec343}')

        reply_exec43 = ReplyKeyboardMarkup(resize_keyboard=True,
            one_time_keyboard=True).add(button_exec143).add(button_exec243, button_exec343)
        await message.answer(f'Ты выбрал услугу {serv43}, сейчас выбери исполнителя',
            reply_markup=reply_exec43)

        await Сhoice.text_exec.set()
        await state.update_data(text_serv43=text_serv)

    elif text_serv == serv53:
        button_exec153 = KeyboardButton(f'{exec153}')
        button_exec253 = KeyboardButton(f'{exec253}')
        button_exec353 = KeyboardButton(f'{exec353}')

        reply_exec53 = ReplyKeyboardMarkup(resize_keyboard=True,
            one_time_keyboard=True).add(button_exec153).add(button_exec253, button_exec353)
        await message.answer(f'Ты выбрал услугу {serv53}, сейчас выбери исполнителя',
            reply_markup=reply_exec53)

        await Сhoice.text_exec.set()
        await state.update_data(text_serv53=text_serv)


@dp.message_handler(state=Сhoice.text_exec)
async def text_exec(message: types.Message, state: FSMContext):
    text_exec = message.text

# относящиеся к 1 сервису города 1
    exec111 = await Item.select('executor11_name').where(Item.id == 1).gino.scalar()
    exec211 = await Item.select('executor21_name').where(Item.id == 1).gino.scalar()
    exec311 = await Item.select('executor31_name').where(Item.id == 1).gino.scalar()
# относящиеся к 2 сервису города 1
    exec121 = await Item.select('executor12_name').where(Item.id == 1).gino.scalar()
    exec221 = await Item.select('executor22_name').where(Item.id == 1).gino.scalar()
    exec321 = await Item.select('executor32_name').where(Item.id == 1).gino.scalar()
# относящиеся к 3 сервису города 1
    exec131 = await Item.select('executor13_name').where(Item.id == 1).gino.scalar()
    exec231 = await Item.select('executor23_name').where(Item.id == 1).gino.scalar()
    exec331 = await Item.select('executor33_name').where(Item.id == 1).gino.scalar()
# относящиеся к 4 сервису города 1
    exec141 = await Item.select('executor14_name').where(Item.id == 1).gino.scalar()
    exec241 = await Item.select('executor24_name').where(Item.id == 1).gino.scalar()
    exec341 = await Item.select('executor34_name').where(Item.id == 1).gino.scalar()
# относящиеся к 5 сервису города 1
    exec151 = await Item.select('executor15_name').where(Item.id == 1).gino.scalar()
    exec251 = await Item.select('executor25_name').where(Item.id == 1).gino.scalar()
    exec351 = await Item.select('executor35_name').where(Item.id == 1).gino.scalar()

# относящиеся к 1 сервису города 2
    exec112 = await Item.select('executor11_name').where(Item.id == 2).gino.scalar()
    exec212 = await Item.select('executor21_name').where(Item.id == 2).gino.scalar()
    exec312 = await Item.select('executor31_name').where(Item.id == 2).gino.scalar()
# относящиеся к 2 сервису города 2
    exec122 = await Item.select('executor12_name').where(Item.id == 2).gino.scalar()
    exec222 = await Item.select('executor22_name').where(Item.id == 2).gino.scalar()
    exec322 = await Item.select('executor32_name').where(Item.id == 2).gino.scalar()
# относящиеся к 3 сервису города 2
    exec132 = await Item.select('executor13_name').where(Item.id == 2).gino.scalar()
    exec232 = await Item.select('executor23_name').where(Item.id == 2).gino.scalar()
    exec332 = await Item.select('executor33_name').where(Item.id == 2).gino.scalar()
# относящиеся к 4 сервису города 2
    exec142 = await Item.select('executor14_name').where(Item.id == 2).gino.scalar()
    exec242 = await Item.select('executor24_name').where(Item.id == 2).gino.scalar()
    exec342 = await Item.select('executor34_name').where(Item.id == 2).gino.scalar()
# относящиеся к 5 сервису города 2
    exec152 = await Item.select('executor15_name').where(Item.id == 2).gino.scalar()
    exec252 = await Item.select('executor25_name').where(Item.id == 2).gino.scalar()
    exec352 = await Item.select('executor35_name').where(Item.id == 2).gino.scalar()

# относящиеся к 1 сервису города 3
    exec113 = await Item.select('executor11_name').where(Item.id == 3).gino.scalar()
    exec213 = await Item.select('executor21_name').where(Item.id == 3).gino.scalar()
    exec313 = await Item.select('executor31_name').where(Item.id == 3).gino.scalar()
# относящиеся к 2 сервису города 3
    exec123 = await Item.select('executor12_name').where(Item.id == 3).gino.scalar()
    exec223 = await Item.select('executor22_name').where(Item.id == 3).gino.scalar()
    exec323 = await Item.select('executor32_name').where(Item.id == 3).gino.scalar()
# относящиеся к 3 сервису города 3
    exec133 = await Item.select('executor13_name').where(Item.id == 3).gino.scalar()
    exec233 = await Item.select('executor23_name').where(Item.id == 3).gino.scalar()
    exec333 = await Item.select('executor33_name').where(Item.id == 3).gino.scalar()
# относящиеся к 4 сервису города 3
    exec143 = await Item.select('executor14_name').where(Item.id == 3).gino.scalar()
    exec243 = await Item.select('executor24_name').where(Item.id == 3).gino.scalar()
    exec343 = await Item.select('executor34_name').where(Item.id == 3).gino.scalar()
# относящиеся к 5 сервису города 3
    exec153 = await Item.select('executor15_name').where(Item.id == 3).gino.scalar()
    exec253 = await Item.select('executor25_name').where(Item.id == 3).gino.scalar()
    exec353 = await Item.select('executor35_name').where(Item.id == 3).gino.scalar()

    if text_exec == exec111:
        exec111 = await Item.select('executor11_name').where(Item.id == 1).gino.scalar()
        exec111_pay = await Item.select('executor11_pay').where(Item.id == 1).gino.scalar()
        exec111_info = await Item.select('executor11_info').where(Item.id == 1).gino.scalar()
        exec111_sup = await Item.select('executor11_sup').where(Item.id == 1).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec111}\n'
            f'Способы оплаты: {exec111_pay}\n'
            f'Контакт для связи: {exec111_info}\n'
            f'Support: {exec111_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')
    
    elif text_exec == exec211:
        exec211 = await Item.select('executor21_name').where(Item.id == 1).gino.scalar()
        exec211_pay = await Item.select('executor21_pay').where(Item.id == 1).gino.scalar()
        exec211_info = await Item.select('executor21_info').where(Item.id == 1).gino.scalar()
        exec211_sup = await Item.select('executor21_sup').where(Item.id == 1).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec211}\n'
            f'Способы оплаты: {exec211_pay}\n'
            f'Контакт для связи: {exec211_info}\n'
            f'Support: {exec211_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec311:
        exec311 = await Item.select('executor31_name').where(Item.id == 1).gino.scalar()
        exec311_pay = await Item.select('executor31_pay').where(Item.id == 1).gino.scalar()
        exec311_info = await Item.select('executor31_info').where(Item.id == 1).gino.scalar()
        exec311_sup = await Item.select('executor31_sup').where(Item.id == 1).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec311}\n'
            f'Способы оплаты: {exec311_pay}\n'
            f'Контакт для связи: {exec311_info}\n'
            f'Support: {exec311_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec121:
        exec121 = await Item.select('executor12_name').where(Item.id == 1).gino.scalar()
        exec121_pay = await Item.select('executor12_pay').where(Item.id == 1).gino.scalar()
        exec121_info = await Item.select('executor12_info').where(Item.id == 1).gino.scalar()
        exec121_sup = await Item.select('executor12_sup').where(Item.id == 1).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec121}\n'
            f'Способы оплаты: {exec121_pay}\n'
            f'Контакт для связи: {exec121_info}\n'
            f'Support: {exec121_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec221:
        exec221 = await Item.select('executor22_name').where(Item.id == 1).gino.scalar()
        exec221_pay = await Item.select('executor22_pay').where(Item.id == 1).gino.scalar()
        exec221_info = await Item.select('executor22_info').where(Item.id == 1).gino.scalar()
        exec221_sup = await Item.select('executor22_sup').where(Item.id == 1).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec221}\n'
            f'Способы оплаты: {exec221_pay}\n'
            f'Контакт для связи: {exec221_info}\n'
            f'Support: {exec221_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')
    
    elif text_exec == exec321:
        exec321 = await Item.select('executor32_name').where(Item.id == 1).gino.scalar()
        exec321_pay = await Item.select('executor32_pay').where(Item.id == 1).gino.scalar()
        exec321_info = await Item.select('executor32_info').where(Item.id == 1).gino.scalar()
        exec321_sup = await Item.select('executor32_sup').where(Item.id == 1).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec321}\n'
            f'Способы оплаты: {exec321_pay}\n'
            f'Контакт для связи: {exec321_info}\n'
            f'Support: {exec321_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec131:
        exec131 = await Item.select('executor13_name').where(Item.id == 1).gino.scalar()
        exec131_pay = await Item.select('executor13_pay').where(Item.id == 1).gino.scalar()
        exec131_info = await Item.select('executor13_info').where(Item.id == 1).gino.scalar()
        exec131_sup = await Item.select('executor13_sup').where(Item.id == 1).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec131}\n'
            f'Способы оплаты: {exec131_pay}\n'
            f'Контакт для связи: {exec131_info}\n'
            f'Support: {exec131_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec231:
        exec231 = await Item.select('executor23_name').where(Item.id == 1).gino.scalar()
        exec231_pay = await Item.select('executor23_pay').where(Item.id == 1).gino.scalar()
        exec231_info = await Item.select('executor23_info').where(Item.id == 1).gino.scalar()
        exec231_sup = await Item.select('executor23_sup').where(Item.id == 1).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec231}\n'
            f'Способы оплаты: {exec231_pay}\n'
            f'Контакт для связи: {exec231_info}\n'
            f'Support: {exec231_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec331:
        exec331 = await Item.select('executor33_name').where(Item.id == 1).gino.scalar()
        exec331_pay = await Item.select('executor33_pay').where(Item.id == 1).gino.scalar()
        exec331_info = await Item.select('executor33_info').where(Item.id == 1).gino.scalar()
        exec331_sup = await Item.select('executor33_sup').where(Item.id == 1).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec331}\n'
            f'Способы оплаты: {exec331_pay}\n'
            f'Контакт для связи: {exec331_info}\n'
            f'Support: {exec331_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')
    
    elif text_exec == exec141:
        exec141 = await Item.select('executor14_name').where(Item.id == 1).gino.scalar()
        exec141_pay = await Item.select('executor14_pay').where(Item.id == 1).gino.scalar()
        exec141_info = await Item.select('executor14_info').where(Item.id == 1).gino.scalar()
        exec141_sup = await Item.select('executor14_sup').where(Item.id == 1).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec141}\n'
            f'Способы оплаты: {exec141_pay}\n'
            f'Контакт для связи: {exec141_info}\n'
            f'Support: {exec141_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec241:
        exec241 = await Item.select('executor24_name').where(Item.id == 1).gino.scalar()
        exec241_pay = await Item.select('executor24_pay').where(Item.id == 1).gino.scalar()
        exec241_info = await Item.select('executor24_info').where(Item.id == 1).gino.scalar()
        exec241_sup = await Item.select('executor24_sup').where(Item.id == 1).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec241}\n'
            f'Способы оплаты: {exec241_pay}\n'
            f'Контакт для связи: {exec241_info}\n'
            f'Support: {exec241_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec341:
        exec341 = await Item.select('executor34_name').where(Item.id == 1).gino.scalar()
        exec341_pay = await Item.select('executor34_pay').where(Item.id == 1).gino.scalar()
        exec341_info = await Item.select('executor34_info').where(Item.id == 1).gino.scalar()
        exec341_sup = await Item.select('executor34_sup').where(Item.id == 1).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec341}\n'
            f'Способы оплаты: {exec341_pay}\n'
            f'Контакт для связи: {exec341_info}\n'
            f'Support: {exec341_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec151:
        exec151 = await Item.select('executor15_name').where(Item.id == 1).gino.scalar()
        exec151_pay = await Item.select('executor15_pay').where(Item.id == 1).gino.scalar()
        exec151_info = await Item.select('executor15_info').where(Item.id == 1).gino.scalar()
        exec151_sup = await Item.select('executor15_sup').where(Item.id == 1).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec151}\n'
            f'Способы оплаты: {exec151_pay}\n'
            f'Контакт для связи: {exec151_info}\n'
            f'Support: {exec151_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')
    
    elif text_exec == exec251:
        exec251 = await Item.select('executor25_name').where(Item.id == 1).gino.scalar()
        exec251_pay = await Item.select('executor25_pay').where(Item.id == 1).gino.scalar()
        exec251_info = await Item.select('executor25_info').where(Item.id == 1).gino.scalar()
        exec251_sup = await Item.select('executor25_sup').where(Item.id == 1).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec251}\n'
            f'Способы оплаты: {exec251_pay}\n'
            f'Контакт для связи: {exec251_info}\n'
            f'Support: {exec251_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')
    
    elif text_exec == exec351:
        exec351 = await Item.select('executor35_name').where(Item.id == 1).gino.scalar()
        exec351_pay = await Item.select('executor35_pay').where(Item.id == 1).gino.scalar()
        exec351_info = await Item.select('executor35_info').where(Item.id == 1).gino.scalar()
        exec351_sup = await Item.select('executor35_sup').where(Item.id == 1).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec351}\n'
            f'Способы оплаты: {exec351_pay}\n'
            f'Контакт для связи: {exec351_info}\n'
            f'Support: {exec351_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

#####################################################################################################
#####################################################################################################

    elif text_exec == exec112:
        exec112 = await Item.select('executor11_name').where(Item.id == 2).gino.scalar()
        exec112_pay = await Item.select('executor11_pay').where(Item.id == 2).gino.scalar()
        exec112_info = await Item.select('executor11_info').where(Item.id == 2).gino.scalar()
        exec112_sup = await Item.select('executor11_sup').where(Item.id == 2).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec112}\n'
            f'Способы оплаты: {exec112_pay}\n'
            f'Контакт для связи: {exec112_info}\n'
            f'Support: {exec112_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec212:
        exec212 = await Item.select('executor21_name').where(Item.id == 2).gino.scalar()
        exec212_pay = await Item.select('executor21_pay').where(Item.id == 2).gino.scalar()
        exec212_info = await Item.select('executor21_info').where(Item.id == 2).gino.scalar()
        exec212_sup = await Item.select('executor21_sup').where(Item.id == 2).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec212}\n'
            f'Способы оплаты: {exec212_pay}\n'
            f'Контакт для связи: {exec212_info}\n'
            f'Support: {exec212_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec312:
        exec312 = await Item.select('executor31_name').where(Item.id == 2).gino.scalar()
        exec312_pay = await Item.select('executor31_pay').where(Item.id == 2).gino.scalar()
        exec312_info = await Item.select('executor31_info').where(Item.id == 2).gino.scalar()
        exec312_sup = await Item.select('executor31_sup').where(Item.id == 2).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec312}\n'
            f'Способы оплаты: {exec312_pay}\n'
            f'Контакт для связи: {exec312_info}\n'
            f'Support: {exec312_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec122:
        exec122 = await Item.select('executor12_name').where(Item.id == 2).gino.scalar()
        exec122_pay = await Item.select('executor12_pay').where(Item.id == 2).gino.scalar()
        exec122_info = await Item.select('executor12_info').where(Item.id == 2).gino.scalar()
        exec122_sup = await Item.select('executor12_sup').where(Item.id == 2).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec122}\n'
            f'Способы оплаты: {exec122_pay}\n'
            f'Контакт для связи: {exec122_info}\n'
            f'Support: {exec122_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec222:
        exec222 = await Item.select('executor22_name').where(Item.id == 2).gino.scalar()
        exec222_pay = await Item.select('executor22_pay').where(Item.id == 2).gino.scalar()
        exec222_info = await Item.select('executor22_info').where(Item.id == 2).gino.scalar()
        exec222_sup = await Item.select('executor22_sup').where(Item.id == 2).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec222}\n'
            f'Способы оплаты: {exec222_pay}\n'
            f'Контакт для связи: {exec222_info}\n'
            f'Support: {exec222_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')
    
    elif text_exec == exec322:
        exec322 = await Item.select('executor32_name').where(Item.id == 2).gino.scalar()
        exec322_pay = await Item.select('executor32_pay').where(Item.id == 2).gino.scalar()
        exec322_info = await Item.select('executor32_info').where(Item.id == 2).gino.scalar()
        exec322_sup = await Item.select('executor32_sup').where(Item.id == 2).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec322}\n'
            f'Способы оплаты: {exec322_pay}\n'
            f'Контакт для связи: {exec322_info}\n'
            f'Support: {exec322_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec132:
        exec132 = await Item.select('executor13_name').where(Item.id == 2).gino.scalar()
        exec132_pay = await Item.select('executor13_pay').where(Item.id == 2).gino.scalar()
        exec132_info = await Item.select('executor13_info').where(Item.id == 2).gino.scalar()
        exec132_sup = await Item.select('executor13_sup').where(Item.id == 2).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec132}\n'
            f'Способы оплаты: {exec132_pay}\n'
            f'Контакт для связи: {exec132_info}\n'
            f'Support: {exec132_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec232:
        exec232 = await Item.select('executor23_name').where(Item.id == 2).gino.scalar()
        exec232_pay = await Item.select('executor23_pay').where(Item.id == 2).gino.scalar()
        exec232_info = await Item.select('executor23_info').where(Item.id == 2).gino.scalar()
        exec232_sup = await Item.select('executor23_sup').where(Item.id == 2).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec232}\n'
            f'Способы оплаты: {exec232_pay}\n'
            f'Контакт для связи: {exec232_info}\n'
            f'Support: {exec232_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec332:
        exec332 = await Item.select('executor33_name').where(Item.id == 2).gino.scalar()
        exec332_pay = await Item.select('executor33_pay').where(Item.id == 2).gino.scalar()
        exec332_info = await Item.select('executor33_info').where(Item.id == 2).gino.scalar()
        exec332_sup = await Item.select('executor33_sup').where(Item.id == 2).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec332}\n'
            f'Способы оплаты: {exec332_pay}\n'
            f'Контакт для связи: {exec332_info}\n'
            f'Support: {exec332_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')
    
    elif text_exec == exec142:
        exec142 = await Item.select('executor14_name').where(Item.id == 2).gino.scalar()
        exec142_pay = await Item.select('executor14_pay').where(Item.id == 2).gino.scalar()
        exec142_info = await Item.select('executor14_info').where(Item.id == 2).gino.scalar()
        exec142_sup = await Item.select('executor14_sup').where(Item.id == 2).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec142}\n'
            f'Способы оплаты: {exec142_pay}\n'
            f'Контакт для связи: {exec142_info}\n'
            f'Support: {exec142_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec242:
        exec242 = await Item.select('executor24_name').where(Item.id == 2).gino.scalar()
        exec242_pay = await Item.select('executor24_pay').where(Item.id == 2).gino.scalar()
        exec242_info = await Item.select('executor24_info').where(Item.id == 2).gino.scalar()
        exec242_sup = await Item.select('executor24_sup').where(Item.id == 2).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec242}\n'
            f'Способы оплаты: {exec242_pay}\n'
            f'Контакт для связи: {exec242_info}\n'
            f'Support: {exec242_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec342:
        exec342 = await Item.select('executor34_name').where(Item.id == 2).gino.scalar()
        exec342_pay = await Item.select('executor34_pay').where(Item.id == 2).gino.scalar()
        exec342_info = await Item.select('executor34_info').where(Item.id == 2).gino.scalar()
        exec342_sup = await Item.select('executor34_sup').where(Item.id == 2).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec342}\n'
            f'Способы оплаты: {exec342_pay}\n'
            f'Контакт для связи: {exec342_info}\n'
            f'Support: {exec342_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec152:
        exec152 = await Item.select('executor15_name').where(Item.id == 2).gino.scalar()
        exec152_pay = await Item.select('executor15_pay').where(Item.id == 2).gino.scalar()
        exec152_info = await Item.select('executor15_info').where(Item.id == 2).gino.scalar()
        exec152_sup = await Item.select('executor15_sup').where(Item.id == 2).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec152}\n'
            f'Способы оплаты: {exec152_pay}\n'
            f'Контакт для связи: {exec152_info}\n'
            f'Support: {exec152_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')
    
    elif text_exec == exec252:
        exec252 = await Item.select('executor25_name').where(Item.id == 2).gino.scalar()
        exec252_pay = await Item.select('executor25_pay').where(Item.id == 2).gino.scalar()
        exec252_info = await Item.select('executor25_info').where(Item.id == 2).gino.scalar()
        exec252_sup = await Item.select('executor25_sup').where(Item.id == 2).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec252}\n'
            f'Способы оплаты: {exec252_pay}\n'
            f'Контакт для связи: {exec252_info}\n'
            f'Support: {exec252_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')
    
    elif text_exec == exec352:
        exec352 = await Item.select('executor35_name').where(Item.id == 2).gino.scalar()
        exec352_pay = await Item.select('executor35_pay').where(Item.id == 2).gino.scalar()
        exec352_info = await Item.select('executor35_info').where(Item.id == 2).gino.scalar()
        exec352_sup = await Item.select('executor35_sup').where(Item.id == 2).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec352}\n'
            f'Способы оплаты: {exec352_pay}\n'
            f'Контакт для связи: {exec352_info}\n'
            f'Support: {exec352_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

#####################################################################################################
#####################################################################################################

    elif text_exec == exec113:
        exec113 = await Item.select('executor11_name').where(Item.id == 3).gino.scalar()
        exec113_pay = await Item.select('executor11_pay').where(Item.id == 3).gino.scalar()
        exec113_info = await Item.select('executor11_info').where(Item.id == 3).gino.scalar()
        exec113_sup = await Item.select('executor11_sup').where(Item.id == 3).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec113}\n'
            f'Способы оплаты: {exec113_pay}\n'
            f'Контакт для связи: {exec113_info}\n'
            f'Support: {exec113_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec213:
        exec213 = await Item.select('executor21_name').where(Item.id == 3).gino.scalar()
        exec213_pay = await Item.select('executor21_pay').where(Item.id == 3).gino.scalar()
        exec213_info = await Item.select('executor21_info').where(Item.id == 3).gino.scalar()
        exec213_sup = await Item.select('executor21_sup').where(Item.id == 3).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec213}\n'
            f'Способы оплаты: {exec213_pay}\n'
            f'Контакт для связи: {exec213_info}\n'
            f'Support: {exec213_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec313:
        exec313 = await Item.select('executor31_name').where(Item.id == 3).gino.scalar()
        exec313_pay = await Item.select('executor31_pay').where(Item.id == 3).gino.scalar()
        exec313_info = await Item.select('executor31_info').where(Item.id == 3).gino.scalar()
        exec313_sup = await Item.select('executor31_sup').where(Item.id == 3).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec313}\n'
            f'Способы оплаты: {exec313_pay}\n'
            f'Контакт для связи: {exec313_info}\n'
            f'Support: {exec313_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec123:
        exec123 = await Item.select('executor12_name').where(Item.id == 3).gino.scalar()
        exec123_pay = await Item.select('executor12_pay').where(Item.id == 3).gino.scalar()
        exec123_info = await Item.select('executor12_info').where(Item.id == 3).gino.scalar()
        exec123_sup = await Item.select('executor12_sup').where(Item.id == 3).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec123}\n'
            f'Способы оплаты: {exec123_pay}\n'
            f'Контакт для связи: {exec123_info}\n'
            f'Support: {exec123_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec223:
        exec223 = await Item.select('executor22_name').where(Item.id == 3).gino.scalar()
        exec223_pay = await Item.select('executor22_pay').where(Item.id == 3).gino.scalar()
        exec223_info = await Item.select('executor22_info').where(Item.id == 3).gino.scalar()
        exec223_sup = await Item.select('executor22_sup').where(Item.id == 3).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec223}\n'
            f'Способы оплаты: {exec223_pay}\n'
            f'Контакт для связи: {exec223_info}\n'
            f'Support: {exec223_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')
    
    elif text_exec == exec323:
        exec323 = await Item.select('executor32_name').where(Item.id == 3).gino.scalar()
        exec323_pay = await Item.select('executor32_pay').where(Item.id == 3).gino.scalar()
        exec323_info = await Item.select('executor32_info').where(Item.id == 3).gino.scalar()
        exec323_sup = await Item.select('executor32_sup').where(Item.id == 3).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec323}\n'
            f'Способы оплаты: {exec323_pay}\n'
            f'Контакт для связи: {exec323_info}\n'
            f'Support: {exec323_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec133:
        exec133 = await Item.select('executor13_name').where(Item.id == 3).gino.scalar()
        exec133_pay = await Item.select('executor13_pay').where(Item.id == 3).gino.scalar()
        exec133_info = await Item.select('executor13_info').where(Item.id == 3).gino.scalar()
        exec133_sup = await Item.select('executor13_sup').where(Item.id == 3).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec133}\n'
            f'Способы оплаты: {exec133_pay}\n'
            f'Контакт для связи: {exec133_info}\n'
            f'Support: {exec133_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec233:
        exec233 = await Item.select('executor23_name').where(Item.id == 3).gino.scalar()
        exec233_pay = await Item.select('executor23_pay').where(Item.id == 3).gino.scalar()
        exec233_info = await Item.select('executor23_info').where(Item.id == 3).gino.scalar()
        exec233_sup = await Item.select('executor23_sup').where(Item.id == 3).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec233}\n'
            f'Способы оплаты: {exec233_pay}\n'
            f'Контакт для связи: {exec233_info}\n'
            f'Support: {exec233_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec333:
        exec333 = await Item.select('executor33_name').where(Item.id == 3).gino.scalar()
        exec333_pay = await Item.select('executor33_pay').where(Item.id == 3).gino.scalar()
        exec333_info = await Item.select('executor33_info').where(Item.id == 3).gino.scalar()
        exec333_sup = await Item.select('executor33_sup').where(Item.id == 3).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec333}\n'
            f'Способы оплаты: {exec333_pay}\n'
            f'Контакт для связи: {exec333_info}\n'
            f'Support: {exec333_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')
    
    elif text_exec == exec142:
        exec143 = await Item.select('executor14_name').where(Item.id == 3).gino.scalar()
        exec143_pay = await Item.select('executor14_pay').where(Item.id == 3).gino.scalar()
        exec143_info = await Item.select('executor14_info').where(Item.id == 3).gino.scalar()
        exec143_sup = await Item.select('executor14_sup').where(Item.id == 3).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec143}\n'
            f'Способы оплаты: {exec143_pay}\n'
            f'Контакт для связи: {exec143_info}\n'
            f'Support: {exec143_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec243:
        exec243 = await Item.select('executor24_name').where(Item.id == 3).gino.scalar()
        exec243_pay = await Item.select('executor24_pay').where(Item.id == 3).gino.scalar()
        exec243_info = await Item.select('executor24_info').where(Item.id == 3).gino.scalar()
        exec243_sup = await Item.select('executor24_sup').where(Item.id == 3).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec243}\n'
            f'Способы оплаты: {exec243_pay}\n'
            f'Контакт для связи: {exec243_info}\n'
            f'Support: {exec243_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec343:
        exec343 = await Item.select('executor34_name').where(Item.id == 3).gino.scalar()
        exec343_pay = await Item.select('executor34_pay').where(Item.id == 3).gino.scalar()
        exec343_info = await Item.select('executor34_info').where(Item.id == 3).gino.scalar()
        exec343_sup = await Item.select('executor34_sup').where(Item.id == 3).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec343}\n'
            f'Способы оплаты: {exec343_pay}\n'
            f'Контакт для связи: {exec343_info}\n'
            f'Support: {exec343_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')

    elif text_exec == exec153:
        exec153 = await Item.select('executor15_name').where(Item.id == 3).gino.scalar()
        exec153_pay = await Item.select('executor15_pay').where(Item.id == 3).gino.scalar()
        exec153_info = await Item.select('executor15_info').where(Item.id == 3).gino.scalar()
        exec153_sup = await Item.select('executor15_sup').where(Item.id == 3).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec153}\n'
            f'Способы оплаты: {exec153_pay}\n'
            f'Контакт для связи: {exec153_info}\n'
            f'Support: {exec153_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')
    
    elif text_exec == exec253:
        exec253 = await Item.select('executor25_name').where(Item.id == 3).gino.scalar()
        exec253_pay = await Item.select('executor25_pay').where(Item.id == 3).gino.scalar()
        exec253_info = await Item.select('executor25_info').where(Item.id == 3).gino.scalar()
        exec253_sup = await Item.select('executor25_sup').where(Item.id == 3).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec253}\n'
            f'Способы оплаты: {exec253_pay}\n'
            f'Контакт для связи: {exec253_info}\n'
            f'Support: {exec253_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')
    
    elif text_exec == exec353:
        exec353 = await Item.select('executor35_name').where(Item.id == 3).gino.scalar()
        exec353_pay = await Item.select('executor35_pay').where(Item.id == 3).gino.scalar()
        exec353_info = await Item.select('executor35_info').where(Item.id == 3).gino.scalar()
        exec353_sup = await Item.select('executor35_sup').where(Item.id == 3).gino.scalar()
        await message.answer('Данные:\n'
            f'Ты выбрал исполнителя {exec353}\n'
            f'Способы оплаты: {exec353_pay}\n'
            f'Контакт для связи: {exec353_info}\n'
            f'Support: {exec353_sup}')
        await state.reset_state()
        await message.answer('Перейди в стартовое меню, нажав /start')


@dp.message_handler()
async def message(message: types.Message):
    if message.text == '📋 Прайс-лист':
        url = await Price.select('url').where(Price.id == 1).gino.scalar()
        await message.answer(url)
        await message.answer('Начать пользоваться, нажми /choice\n'
            'Узнать 📋 Прайс-лист, нажми на кнопку ниже',
            reply_markup=kb.reply_price)