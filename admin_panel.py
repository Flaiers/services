import database
import kb

from aiogram import types
from aiogram.dispatcher import FSMContext
from config import admin_id
from load_all import dp, bot
from states import NewCity, Document
from database import Item, Price


@dp.message_handler(user_id=admin_id, commands=['admin'])
async def admin(message: types.Message):
    await message.answer('Вот список ваших команд:\n'
        '/add_city — добавить новый город, и прописать остальные зависимости в нём\n'
        '/add_price — добавить новый прайс-лист\n'
        '/cancel — отменить добавление в БД города\n\n'
        'Список терминов:\n'
        '        БД — База данных то, откуда пользовательская сторона берёт информацию\n'
        '        Следующий шаг — Пропустить добавление текущих параметров, перейти к добавлению следующих\n'
        '✏️ Редактировать — Вернуться на одно действие назад и изменить параметр\n'
        '🔚 Закончить добавление — Перенести все введённые параметры в БД')


@dp.message_handler(user_id=admin_id, commands=['cancel'], state=NewCity)
async def cancel(message: types.Message, state: FSMContext):
    await message.answer('Вы отменили создание')
    await state.reset_state()


@dp.message_handler(user_id=admin_id, commands=['add_price'])
async def add_price(message: types.Message):
	await message.answer('Отправьте мне ссылку на статью telegra.ph'
		'\nХотите вернуться назад, нажмите на кнопку',
		reply_markup=kb.reply_back)
	await Document.price.set()


@dp.message_handler(user_id=admin_id, state=Document.price)
async def enter_price(message: types.Message, state: FSMContext):
	url = message.text
	if url == '🔙 Назад':
		await message.answer('Вот список ваших команд:\n'
		'/add_city — добавить новый город, и прописать остальные зависимости в нём\n'
		'/add_price — добавить новый прайс-лист\n'
		'/cancel — отменить добавление в БД города\n\n'
		'Список терминов:\n'
		'        БД — База данных то, откуда пользовательская сторона берёт информацию\n'
		'        Следующий шаг — Пропустить добавление текущих параметров, перейти к добавлению следующих\n'
		'✏️ Редактировать — Вернуться на одно действие назад и изменить параметр\n'
		'🔚 Закончить добавление — Перенести все введённые параметры в БД')
		await state.reset_state()
	else:
		price = Price()
		price.url = url

		await message.answer('Введёные вами данные успешно добавлены!\n'
			'Нажми на /admin, чтобы вернуться в начало')

		await state.update_data(price=price)
		await price.create()
		data = await state.get_data()
		price: Price = data.get('price')
		await state.reset_state()


@dp.message_handler(user_id=admin_id, commands=['add_city'])
async def add_city(message: types.Message):
    await message.answer('Введите название города или нажмите /cancel')
    await NewCity.city.set()


@dp.message_handler(user_id=admin_id, state=NewCity.city)
async def enter_city(message: types.Message, state: FSMContext):
    city = message.text
    item = Item()
    item.city = city

    await message.answer(f'Название города {city}\n'
        'Пришлите мне вид услуги №1, если их несколько, то пришлите по порядку\n'
        'Хотите отредактировать название города, нажмите ✏️ Редактировать',
        reply_markup=kb.reply_ed)

    await NewCity.service1.set()
    await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.service1)
async def enter_service1(message: types.Message, state: FSMContext):
    service1 = message.text
    if service1 == '✏️ Редактировать':
        await message.answer('Введите название города снова')
        await NewCity.city.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.service1 = service1

        await message.answer(f'Услуга {service1} добавлена\n'
            'Чтобы добавить услугу №2, отправьте её мне. Если добавлять ничего не нужно, нажмите — Следующий шаг\n'
            'Хотите отредактировать название услуги №1, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed_next)

        await NewCity.service2.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.service2)
async def enter_service2(message: types.Message, state: FSMContext):
    service2 = message.text
    if service2 == 'Следующий шаг':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне имя исполнителя №1 услуги {item.service1}')
        await NewCity.executor11_name.set()
        await state.update_data(item=item)
    elif service2 == '✏️ Редактировать':
        await message.answer('Пришлите мне вид услуги №1 снова')
        await NewCity.service1.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.service2 = service2

        await message.answer(f'Услуга {service2} добавлена\n'
            'Чтобы добавить услугу №3, отправьте её мне. Если добавлять ничего не нужно, нажмите — Следующий шаг\n'
            'Хотите отредактировать название услуги №2, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed_next)

        await NewCity.service3.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.service3)
async def enter_service3(message: types.Message, state: FSMContext):
    service3 = message.text
    if service3 == 'Следующий шаг':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне имя исполнителя №1 услуги {item.service1}')
        await NewCity.executor11_name.set()
        await state.update_data(item=item)
    elif service3 == '✏️ Редактировать':
        await message.answer('Пришлите мне вид услуги №2 снова')
        await NewCity.service2.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.service3 = service3

        await message.answer(f'Услуга {service3} добавлена\n'
            'Чтобы добавить услугу №4, отправьте её мне. Если добавлять ничего не нужно, нажмите — Следующий шаг\n'
            'Хотите отредактировать название услуги №3, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed_next)

        await NewCity.service4.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.service4)
async def enter_service4(message: types.Message, state: FSMContext):
    service4 = message.text
    if service4 == 'Следующий шаг':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне имя исполнителя №1 услуги {item.service1}')
        await NewCity.executor11_name.set()
        await state.update_data(item=item)
    elif service4 == '✏️ Редактировать':
        await message.answer('Пришлите мне вид услуги №3 снова')
        await NewCity.service3.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.service4 = service4

        await message.answer(f'Услуга {service4} добавлена\n'
            'Чтобы добавить услугу №5, отправьте её мне. Если добавлять ничего не нужно, нажмите — Следующий шаг\n'
            'Хотите отредактировать название услуги №4, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed_next)

        await NewCity.service5.set()
        await state.update_data(item=item)

@dp.message_handler(user_id=admin_id, state=NewCity.service5)
async def enter_service5(message: types.Message, state: FSMContext):
    service5 = message.text
    if service5 == 'Следующий шаг':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне имя исполнителя №1 услуги {item.service1}')
        await NewCity.executor11_name.set()
        await state.update_data(item=item)
    elif service5 == '✏️ Редактировать':
        await message.answer('Пришлите мне вид услуги №4 снова')
        await NewCity.service4.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.service5 = service5

        await message.answer(f'Услуга {service5} добавлена\n'
            f'Пришлите мне имя исполнителя №1 услуги {item.service1}\n'
            'Хотите отредактировать название услуги №5, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed_next)

        await NewCity.executor11_name.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor11_name)
async def enter_executor11_name(message: types.Message, state: FSMContext):
    executor11_name = message.text
    if executor11_name == '✏️ Редактировать':
        await message.answer('Пришлите мне вид услуги №5 снова')
        await NewCity.service4.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor11_name = executor11_name

        await message.answer(f'Имя исполнителя №1 услуги {item.service1} — {executor11_name}\n'
            f'Пришлите мне способ оплаты исполнителя {executor11_name} услуги {item.service1}\n'
            f'Хотите отредактировать имя исполнителя №1 услуги {item.service1}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor11_pay.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor11_pay)
async def enter_executor11_pay(message: types.Message, state: FSMContext):
    executor11_pay = message.text
    if executor11_pay == '✏️ Редактировать':
        await message.answer('Пришлите мне имя исполнителя №1 снова')
        await NewCity.executor11_name.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor11_pay = executor11_pay

        await message.answer(f'Cпособ оплаты исполнителя {item.executor11_name} услуги {item.service1} — {executor11_pay}\n'
            f'Пришлите мне контакт для связи с исполнителем {item.executor11_name} услуги {item.service1}\n'
            f'Хотите отредактировать cпособ оплаты исполнителя {item.executor11_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor11_info.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor11_info)
async def enter_executor11_info(message: types.Message, state: FSMContext):
    executor11_info = message.text
    if executor11_info == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне cпособ оплаты исполнителя {item.executor11_name} снова')
        await NewCity.executor11_pay.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor11_info = executor11_info

        await message.answer(f'Контакт для связи с исполнителем {item.executor11_name} услуги {item.service1} — {executor11_info}\n'
            f'Пришлите мне контакт менеджера исполнителя {item.executor11_name} услуги {item.service1}\n'
            f'Хотите отредактировать контакт для связи с исполнителем {item.executor11_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor11_sup.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor11_sup)
async def enter_executor11_sup(message: types.Message, state: FSMContext):
    executor11_sup = message.text
    if executor11_sup == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне контакт для связи с исполнителем {item.executor11_name} снова')
        await NewCity.executor11_info.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor11_sup = executor11_sup

        await message.answer(f'Контакт менеджера исполнителя {item.executor11_name} услуги {item.service1} — {executor11_sup}\n'
            f'Чтобы добавить исполнителя №2 услуги {item.service1}, напишите его имя. Если добавлять не нужно, нажмите — Следующий шаг\n'
            f'Хотите отредактировать контакт менеджера исполнителя {item.executor11_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed_next)

        await NewCity.executor21_name.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor21_name)
async def enter_executor21_name(message: types.Message, state: FSMContext):
    executor21_name = message.text
    if executor21_name == 'Следующий шаг':
        data = await state.get_data()
        item: Item = data.get("item")
        await message.answer(f'Чтобы добавить исполнителя №1 услуги {item.service2}, напишите его имя. Если услуги нет, нажмите — 🔚 Закончить добавление',
            reply_markup=kb.reply_ed_end)
        await NewCity.executor12_name.set()
        await state.update_data(item=item)
    elif executor21_name == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне контакт менеджера исполнителя {item.executor11_name} снова')
        await NewCity.executor11_sup.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor21_name = executor21_name

        await message.answer(f'Имя исполнителя №2 услуги {item.service1} — {executor21_name}\n'
        f'Пришлите мне способ оплаты исполнителя {executor21_name} услуги {item.service1}\n'
        'Хотите отредактировать имя исполнителя №2, нажмите ✏️ Редактировать',
        reply_markup=kb.reply_ed)

        await NewCity.executor21_pay.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor21_pay)
async def enter_executor21_pay(message: types.Message, state: FSMContext):
    executor21_pay = message.text
    if executor21_pay == '✏️ Редактировать':
        await message.answer('Пришлите мне имя исполнителя №2 снова')
        await NewCity.executor21_name.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor21_pay = executor21_pay

        await message.answer(f'Cпособ оплаты исполнителя {item.executor21_name} услуги {item.service1} — {executor21_pay}\n'
            f'Пришлите мне контакт для связи с исполнителем {item.executor21_name} услуги {item.service1}\n'
            f'Хотите отредактировать cпособ оплаты исполнителя {item.executor21_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor21_info.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor21_info)
async def enter_executor21_info(message: types.Message, state: FSMContext):
    executor21_info = message.text
    if executor21_info == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне cпособ оплаты исполнителя {item.executor21_name} снова')
        await NewCity.executor21_pay.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor21_info = executor21_info

        await message.answer(f'Контакт для связи с исполнителем {item.executor21_name} услуги {item.service1} — {executor21_info}\n'
            f'Пришлите мне контакт менеджера исполнителя {item.executor21_name} услуги {item.service1}\n'
            f'Хотите отредактировать контакт для связи с исполнителем {item.executor21_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor21_sup.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor21_sup)
async def enter_executor21_sup(message: types.Message, state: FSMContext):
    executor21_sup = message.text
    if executor21_sup == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне контакт для связи с исполнителем {item.executor21_name} снова')
        await NewCity.executor21_info.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor21_sup = executor21_sup

        await message.answer(f'Контакт менеджера исполнителя {item.executor21_name} услуги {item.service1} — {executor21_sup}\n'
            f'Чтобы добавить исполнителя №3, напишите его имя. Если добавлять не нужно, нажмите — Следующий шаг\n'
            f'Хотите отредактировать контакт менеджера исполнителя {item.executor21_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed_next)

        await NewCity.executor31_name.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor31_name)
async def enter_executor31_name(message: types.Message, state: FSMContext):
    executor31_name = message.text
    if executor31_name == 'Следующий шаг':
        data = await state.get_data()
        item: Item = data.get("item")
        await message.answer(f'Чтобы добавить исполнителя №1 услуги {item.service2}, напишите его имя. Если услуги нет, нажмите — 🔚 Закончить добавление',
            reply_markup=kb.reply_ed_end)
        await NewCity.executor12_name.set()
        await state.update_data(item=item)
    elif executor31_name == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне контакт менеджера исполнителя {item.executor21_name} снова')
        await NewCity.executor21_sup.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor31_name = executor31_name

        await message.answer(f'Имя исполнителя №3 услуги {item.service1} — {executor31_name}\n'
        f'Пришлите мне способ оплаты исполнителя {executor31_name} услуги {item.service1}\n'
        'Хотите отредактировать имя исполнителя №3, нажмите ✏️ Редактировать',
        reply_markup=kb.reply_ed)

        await NewCity.executor31_pay.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor31_pay)
async def enter_executor31_pay(message: types.Message, state: FSMContext):
    executor31_pay = message.text
    if executor31_pay == '✏️ Редактировать':
        await message.answer('Пришлите мне имя исполнителя №3 снова')
        await NewCity.executor31_name.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor31_pay = executor31_pay

        await message.answer(f'Cпособ оплаты исполнителя {item.executor31_name} услуги {item.service1} — {executor31_pay}\n'
            f'Пришлите мне контакт для связи с исполнителем {item.executor31_name} услуги {item.service1}\n'
            f'Хотите отредактировать cпособ оплаты исполнителя {item.executor31_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor31_info.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor31_info)
async def enter_executor31_info(message: types.Message, state: FSMContext):
    executor31_info = message.text
    if executor31_info == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне cпособ оплаты исполнителя {item.executor31_name} снова')
        await NewCity.executor31_pay.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor31_info = executor31_info

        await message.answer(f'Контакт для связи с исполнителем {item.executor31_name} услуги {item.service1} — {executor31_info}\n'
            f'Пришлите мне контакт менеджера исполнителя {item.executor31_name} услуги {item.service1}\n'
            f'Хотите отредактировать контакт для связи с исполнителем {item.executor31_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor31_sup.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor31_sup)
async def enter_executor31_sup(message: types.Message, state: FSMContext):
    executor31_sup = message.text
    if executor31_sup == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне контакт для связи с исполнителем {item.executor31_name} снова')
        await NewCity.executor31_info.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor31_sup = executor31_sup

        await message.answer(f'Контакт менеджера исполнителя {item.executor31_name} услуги {item.service1} — {executor31_sup}\n'
            f'Чтобы добавить исполнителя №1 услуги {item.service2}, напишите его имя. Если услуги нет, нажмите — 🔚 Закончить добавление\n'
            f'Хотите отредактировать контакт менеджера исполнителя {item.executor31_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed_end)

        await NewCity.executor12_name.set()
        await state.update_data(item=item)


##########################################################################################################
##########################################################################################################


@dp.message_handler(user_id=admin_id, state=NewCity.executor12_name)
async def enter_executor12_name(message: types.Message, state: FSMContext):
    executor12_name = message.text
    if executor12_name == '🔚 Закончить добавление':
        data = await state.get_data()
        item: Item = data.get("item")
        await item.create()
        await message.answer('Введёные вами данные успешно добавлены!\n'
			'Нажми на /admin, чтобы вернуться в начало')
        await state.reset_state()
    elif executor12_name == '✏️ Редактировать':
        await message.answer(f'Пришлите мне контакт менеджера исполнителя {item.executor31_name} снова')
        await NewCity.executor31_sup.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor12_name = executor12_name

        await message.answer(f'Имя исполнителя №1 услуги {item.service2} — {executor12_name}\n'
            f'Пришлите мне способ оплаты исполнителя {executor12_name} услуги {item.service2}\n'
            f'Хотите отредактировать имя исполнителя №1 услуги {item.service2}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor12_pay.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor12_pay)
async def enter_executor12_pay(message: types.Message, state: FSMContext):
    executor12_pay = message.text
    if executor12_pay == '✏️ Редактировать':
        await message.answer('Пришлите мне имя исполнителя №1 снова')
        await NewCity.executor12_name.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor12_pay = executor12_pay

        await message.answer(f'Cпособ оплаты исполнителя {item.executor12_name} услуги {item.service2} — {executor12_pay}\n'
            f'Пришлите мне контакт для связи с исполнителем {item.executor12_name} услуги {item.service2}\n'
            f'Хотите отредактировать cпособ оплаты исполнителя {item.executor12_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor12_info.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor12_info)
async def enter_executor12_info(message: types.Message, state: FSMContext):
    executor12_info = message.text
    if executor12_info == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне cпособ оплаты исполнителя {item.executor12_name} снова')
        await NewCity.executor12_pay.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor12_info = executor12_info

        await message.answer(f'Контакт для связи с исполнителем {item.executor12_name} услуги {item.service2} — {executor12_info}\n'
            f'Пришлите мне контакт менеджера исполнителя {item.executor12_name} услуги {item.service2}\n'
            f'Хотите отредактировать контакт для связи с исполнителем {item.executor12_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor12_sup.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor12_sup)
async def enter_executor12_sup(message: types.Message, state: FSMContext):
    executor12_sup = message.text
    if executor12_sup == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне контакт для связи с исполнителем {item.executor12_name} снова')
        await NewCity.executor12_info.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor12_sup = executor12_sup

        await message.answer(f'Контакт менеджера исполнителя {item.executor12_name} услуги {item.service2} — {executor12_sup}\n'
            f'Чтобы добавить исполнителя №2 услуги {item.service2}, напишите его имя. Если добавлять не нужно, нажмите — Следующий шаг\n'
            f'Хотите отредактировать контакт менеджера исполнителя {item.executor12_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed_next)

        await NewCity.executor22_name.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor22_name)
async def enter_executor22_name(message: types.Message, state: FSMContext):
    executor22_name = message.text
    if executor22_name == 'Следующий шаг':
        data = await state.get_data()
        item: Item = data.get("item")
        await message.answer(f'Чтобы добавить исполнителя №1 услуги {item.service3}, напишите его имя. Если услуги нет, нажмите — 🔚 Закончить добавление',
            reply_markup=kb.reply_ed_end)
        await NewCity.executor13_name.set()
        await state.update_data(item=item)
    elif executor22_name == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне контакт менеджера исполнителя {item.executor12_name} снова')
        await NewCity.executor12_sup.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor22_name = executor22_name

        await message.answer(f'Имя исполнителя №2 услуги {item.service2} — {executor22_name}\n'
        f'Пришлите мне способ оплаты исполнителя {executor22_name} услуги {item.service2}\n'
        'Хотите отредактировать имя исполнителя №2, нажмите ✏️ Редактировать',
        reply_markup=kb.reply_ed)

        await NewCity.executor22_pay.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor22_pay)
async def enter_executor22_pay(message: types.Message, state: FSMContext):
    executor22_pay = message.text
    if executor22_pay == '✏️ Редактировать':
        await message.answer('Пришлите мне имя исполнителя №2 снова')
        await NewCity.executor22_name.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor22_pay = executor22_pay

        await message.answer(f'Cпособ оплаты исполнителя {item.executor22_name} услуги {item.service2} — {executor22_pay}\n'
            f'Пришлите мне контакт для связи с исполнителем {item.executor22_name} услуги {item.service2}\n'
            f'Хотите отредактировать cпособ оплаты исполнителя {item.executor22_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor22_info.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor22_info)
async def enter_executor22_info(message: types.Message, state: FSMContext):
    executor22_info = message.text
    if executor22_info == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне cпособ оплаты исполнителя {item.executor22_name} снова')
        await NewCity.executor22_pay.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor22_info = executor22_info

        await message.answer(f'Контакт для связи с исполнителем {item.executor22_name} услуги {item.service2} — {executor22_info}\n'
            f'Пришлите мне контакт менеджера исполнителя {item.executor22_name} услуги {item.service2}\n'
            f'Хотите отредактировать контакт для связи с исполнителем {item.executor22_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor22_sup.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor22_sup)
async def enter_executor22_sup(message: types.Message, state: FSMContext):
    executor22_sup = message.text
    if executor22_sup == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне контакт для связи с исполнителем {item.executor22_name} снова')
        await NewCity.executor22_info.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor22_sup = executor22_sup

        await message.answer(f'Контакт менеджера исполнителя {item.executor22_name} услуги {item.service2} — {executor22_sup}\n'
            f'Чтобы добавить исполнителя №3, напишите его имя. Если добавлять не нужно, нажмите — Следующий шаг\n'
            f'Хотите отредактировать контакт менеджера исполнителя {item.executor22_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed_next)

        await NewCity.executor32_name.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor32_name)
async def enter_executor32_name(message: types.Message, state: FSMContext):
    executor32_name = message.text
    if executor32_name == 'Следующий шаг':
        data = await state.get_data()
        item: Item = data.get("item")
        await message.answer(f'Чтобы добавить исполнителя №1 услуги {item.service3}, напишите его имя. Если услуги нет, нажмите — 🔚 Закончить добавление',
            reply_markup=kb.reply_ed_end)
        await NewCity.executor13_name.set()
        await state.update_data(item=item)
    elif executor32_name == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне контакт менеджера исполнителя {item.executor22_name} снова')
        await NewCity.executor22_sup.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor32_name = executor32_name

        await message.answer(f'Имя исполнителя №3 услуги {item.service2} — {executor32_name}\n'
        f'Пришлите мне способ оплаты исполнителя {executor32_name} услуги {item.service2}\n'
        'Хотите отредактировать имя исполнителя №3, нажмите ✏️ Редактировать',
        reply_markup=kb.reply_ed)

        await NewCity.executor32_pay.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor32_pay)
async def enter_executor32_pay(message: types.Message, state: FSMContext):
    executor32_pay = message.text
    if executor32_pay == '✏️ Редактировать':
        await message.answer('Пришлите мне имя исполнителя №3 снова')
        await NewCity.executor32_name.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor32_pay = executor32_pay

        await message.answer(f'Cпособ оплаты исполнителя {item.executor32_name} услуги {item.service2} — {executor32_pay}\n'
            f'Пришлите мне контакт для связи с исполнителем {item.executor32_name} услуги {item.service2}\n'
            f'Хотите отредактировать cпособ оплаты исполнителя {item.executor32_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor32_info.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor32_info)
async def enter_executor32_info(message: types.Message, state: FSMContext):
    executor32_info = message.text
    if executor32_info == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне cпособ оплаты исполнителя {item.executor32_name} снова')
        await NewCity.executor32_pay.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor32_info = executor32_info

        await message.answer(f'Контакт для связи с исполнителем {item.executor32_name} услуги {item.service2} — {executor32_info}\n'
            f'Пришлите мне контакт менеджера исполнителя {item.executor32_name} услуги {item.service2}\n'
            f'Хотите отредактировать контакт для связи с исполнителем {item.executor32_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor32_sup.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor32_sup)
async def enter_executor32_sup(message: types.Message, state: FSMContext):
    executor32_sup = message.text
    if executor32_sup == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне контакт для связи с исполнителем {item.executor32_name} снова')
        await NewCity.executor32_info.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor32_sup = executor32_sup

        await message.answer(f'Контакт менеджера исполнителя {item.executor32_name} услуги {item.service2} — {executor32_sup}\n'
            f'Чтобы добавить исполнителя №1 услуги {item.service3}, напишите его имя. Если услуги нет, нажмите — 🔚 Закончить добавление\n'
            f'Хотите отредактировать контакт менеджера исполнителя {item.executor32_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed_end)

        await NewCity.executor13_name.set()
        await state.update_data(item=item)


##########################################################################################################
##########################################################################################################


@dp.message_handler(user_id=admin_id, state=NewCity.executor13_name)
async def enter_executor13_name(message: types.Message, state: FSMContext):
    executor13_name = message.text
    if executor13_name == '🔚 Закончить добавление':
        data = await state.get_data()
        item: Item = data.get("item")
        await item.create()
        await message.answer('Введёные вами данные успешно добавлены!\n'
			'Нажми на /admin, чтобы вернуться в начало')
        await state.reset_state()
    elif executor13_name == '✏️ Редактировать':
        await message.answer(f'Пришлите мне контакт менеджера исполнителя {item.executor32_name} снова')
        await NewCity.executor32_sup.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor13_name = executor13_name

        await message.answer(f'Имя исполнителя №1 услуги {item.service3} — {executor13_name}\n'
            f'Пришлите мне способ оплаты исполнителя {executor13_name} услуги {item.service3}\n'
            f'Хотите отредактировать имя исполнителя №1 услуги {item.service3}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor13_pay.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor13_pay)
async def enter_executor13_pay(message: types.Message, state: FSMContext):
    executor13_pay = message.text
    if executor13_pay == '✏️ Редактировать':
        await message.answer('Пришлите мне имя исполнителя №1 снова')
        await NewCity.executor13_name.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor13_pay = executor13_pay

        await message.answer(f'Cпособ оплаты исполнителя {item.executor13_name} услуги {item.service3} — {executor13_pay}\n'
            f'Пришлите мне контакт для связи с исполнителем {item.executor13_name} услуги {item.service3}\n'
            f'Хотите отредактировать cпособ оплаты исполнителя {item.executor13_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor13_info.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor13_info)
async def enter_executor13_info(message: types.Message, state: FSMContext):
    executor13_info = message.text
    if executor13_info == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне cпособ оплаты исполнителя {item.executor13_name} снова')
        await NewCity.executor13_pay.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor13_info = executor13_info

        await message.answer(f'Контакт для связи с исполнителем {item.executor13_name} услуги {item.service3} — {executor13_info}\n'
            f'Пришлите мне контакт менеджера исполнителя {item.executor13_name} услуги {item.service3}\n'
            f'Хотите отредактировать контакт для связи с исполнителем {item.executor13_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor13_sup.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor13_sup)
async def enter_executor13_sup(message: types.Message, state: FSMContext):
    executor13_sup = message.text
    if executor13_sup == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне контакт для связи с исполнителем {item.executor13_name} снова')
        await NewCity.executor13_info.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor13_sup = executor13_sup

        await message.answer(f'Контакт менеджера исполнителя {item.executor13_name} услуги {item.service3} — {executor13_sup}\n'
            f'Чтобы добавить исполнителя №2 услуги {item.service3}, напишите его имя. Если добавлять не нужно, нажмите — Следующий шаг\n'
            f'Хотите отредактировать контакт менеджера исполнителя {item.executor13_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed_next)

        await NewCity.executor23_name.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor23_name)
async def enter_executor23_name(message: types.Message, state: FSMContext):
    executor23_name = message.text
    if executor23_name == 'Следующий шаг':
        data = await state.get_data()
        item: Item = data.get("item")
        await message.answer(f'Чтобы добавить исполнителя №1 услуги {item.service4}, напишите его имя. Если услуги нет, нажмите — 🔚 Закончить добавление',
            reply_markup=kb.reply_ed_end)
        await NewCity.executor14_name.set()
        await state.update_data(item=item)
    elif executor23_name == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне контакт менеджера исполнителя {item.executor13_name} снова')
        await NewCity.executor13_sup.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor23_name = executor23_name

        await message.answer(f'Имя исполнителя №2 услуги {item.service3} — {executor23_name}\n'
        f'Пришлите мне способ оплаты исполнителя {executor23_name} услуги {item.service3}\n'
        'Хотите отредактировать имя исполнителя №2, нажмите ✏️ Редактировать',
        reply_markup=kb.reply_ed)

        await NewCity.executor23_pay.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor23_pay)
async def enter_executor23_pay(message: types.Message, state: FSMContext):
    executor23_pay = message.text
    if executor23_pay == '✏️ Редактировать':
        await message.answer('Пришлите мне имя исполнителя №2 снова')
        await NewCity.executor23_name.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor23_pay = executor23_pay

        await message.answer(f'Cпособ оплаты исполнителя {item.executor23_name} услуги {item.service3} — {executor23_pay}\n'
            f'Пришлите мне контакт для связи с исполнителем {item.executor23_name} услуги {item.service3}\n'
            f'Хотите отредактировать cпособ оплаты исполнителя {item.executor23_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor23_info.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor23_info)
async def enter_executor23_info(message: types.Message, state: FSMContext):
    executor23_info = message.text
    if executor23_info == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне cпособ оплаты исполнителя {item.executor23_name} снова')
        await NewCity.executor23_pay.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor23_info = executor23_info

        await message.answer(f'Контакт для связи с исполнителем {item.executor23_name} услуги {item.service3} — {executor23_info}\n'
            f'Пришлите мне контакт менеджера исполнителя {item.executor23_name} услуги {item.service3}\n'
            f'Хотите отредактировать контакт для связи с исполнителем {item.executor23_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor23_sup.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor23_sup)
async def enter_executor23_sup(message: types.Message, state: FSMContext):
    executor23_sup = message.text
    if executor23_sup == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне контакт для связи с исполнителем {item.executor23_name} снова')
        await NewCity.executor23_info.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor23_sup = executor23_sup

        await message.answer(f'Контакт менеджера исполнителя {item.executor23_name} услуги {item.service3} — {executor23_sup}\n'
            f'Чтобы добавить исполнителя №3, напишите его имя. Если добавлять не нужно, нажмите — Следующий шаг\n'
            f'Хотите отредактировать контакт менеджера исполнителя {item.executor23_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed_next)

        await NewCity.executor33_name.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor33_name)
async def enter_executor33_name(message: types.Message, state: FSMContext):
    executor33_name = message.text
    if executor33_name == 'Следующий шаг':
        data = await state.get_data()
        item: Item = data.get("item")
        await message.answer(f'Чтобы добавить исполнителя №1 услуги {item.service4}, напишите его имя. Если услуги нет, нажмите — 🔚 Закончить добавление',
            reply_markup=kb.reply_ed_end)
        await NewCity.executor14_name.set()
        await state.update_data(item=item)
    elif executor33_name == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне контакт менеджера исполнителя {item.executor23_name} снова')
        await NewCity.executor23_sup.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor33_name = executor33_name

        await message.answer(f'Имя исполнителя №3 услуги {item.service3} — {executor33_name}\n'
        f'Пришлите мне способ оплаты исполнителя {executor33_name} услуги {item.service3}\n'
        'Хотите отредактировать имя исполнителя №3, нажмите ✏️ Редактировать',
        reply_markup=kb.reply_ed)

        await NewCity.executor33_pay.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor33_pay)
async def enter_executor33_pay(message: types.Message, state: FSMContext):
    executor33_pay = message.text
    if executor33_pay == '✏️ Редактировать':
        await message.answer('Пришлите мне имя исполнителя №3 снова')
        await NewCity.executor33_name.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor33_pay = executor33_pay

        await message.answer(f'Cпособ оплаты исполнителя {item.executor33_name} услуги {item.service3} — {executor33_pay}\n'
            f'Пришлите мне контакт для связи с исполнителем {item.executor33_name} услуги {item.service3}\n'
            f'Хотите отредактировать cпособ оплаты исполнителя {item.executor33_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor33_info.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor33_info)
async def enter_executor33_info(message: types.Message, state: FSMContext):
    executor33_info = message.text
    if executor33_info == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне cпособ оплаты исполнителя {item.executor33_name} снова')
        await NewCity.executor33_pay.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor33_info = executor33_info

        await message.answer(f'Контакт для связи с исполнителем {item.executor33_name} услуги {item.service3} — {executor33_info}\n'
            f'Пришлите мне контакт менеджера исполнителя {item.executor33_name} услуги {item.service3}\n'
            f'Хотите отредактировать контакт для связи с исполнителем {item.executor33_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor33_sup.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor33_sup)
async def enter_executor33_sup(message: types.Message, state: FSMContext):
    executor33_sup = message.text
    if executor33_sup == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне контакт для связи с исполнителем {item.executor33_name} снова')
        await NewCity.executor33_info.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor33_sup = executor33_sup

        await message.answer(f'Контакт менеджера исполнителя {item.executor33_name} услуги {item.service3} — {executor33_sup}\n'
            f'Чтобы добавить исполнителя №1 услуги {item.service4}, напишите его имя. Если услуги нет, нажмите — 🔚 Закончить добавление\n'
            f'Хотите отредактировать контакт менеджера исполнителя {item.executor33_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed_end)

        await NewCity.executor14_name.set()
        await state.update_data(item=item)


##########################################################################################################
##########################################################################################################


@dp.message_handler(user_id=admin_id, state=NewCity.executor14_name)
async def enter_executor14_name(message: types.Message, state: FSMContext):
    executor14_name = message.text
    if executor14_name == '🔚 Закончить добавление':
        data = await state.get_data()
        item: Item = data.get("item")
        await item.create()
        await message.answer('Введёные вами данные успешно добавлены!\n'
			'Нажми на /admin, чтобы вернуться в начало')
        await state.reset_state()
    elif executor14_name == '✏️ Редактировать':
        await message.answer(f'Пришлите мне контакт менеджера исполнителя {item.executor33_name} снова')
        await NewCity.executor33_sup.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor14_name = executor14_name

        await message.answer(f'Имя исполнителя №1 услуги {item.service4} — {executor14_name}\n'
            f'Пришлите мне способ оплаты исполнителя {executor14_name} услуги {item.service4}\n'
            f'Хотите отредактировать имя исполнителя №1 услуги {item.service4}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor14_pay.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor14_pay)
async def enter_executor14_pay(message: types.Message, state: FSMContext):
    executor14_pay = message.text
    if executor14_pay == '✏️ Редактировать':
        await message.answer('Пришлите мне имя исполнителя №1 снова')
        await NewCity.executor14_name.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor14_pay = executor14_pay

        await message.answer(f'Cпособ оплаты исполнителя {item.executor14_name} услуги {item.service4} — {executor14_pay}\n'
            f'Пришлите мне контакт для связи с исполнителем {item.executor14_name} услуги {item.service4}\n'
            f'Хотите отредактировать cпособ оплаты исполнителя {item.executor14_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor14_info.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor14_info)
async def enter_executor14_info(message: types.Message, state: FSMContext):
    executor14_info = message.text
    if executor14_info == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне cпособ оплаты исполнителя {item.executor14_name} снова')
        await NewCity.executor14_pay.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor14_info = executor14_info

        await message.answer(f'Контакт для связи с исполнителем {item.executor14_name} услуги {item.service4} — {executor14_info}\n'
            f'Пришлите мне контакт менеджера исполнителя {item.executor14_name} услуги {item.service4}\n'
            f'Хотите отредактировать контакт для связи с исполнителем {item.executor14_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor14_sup.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor14_sup)
async def enter_executor14_sup(message: types.Message, state: FSMContext):
    executor14_sup = message.text
    if executor14_sup == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне контакт для связи с исполнителем {item.executor14_name} снова')
        await NewCity.executor14_info.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor14_sup = executor14_sup

        await message.answer(f'Контакт менеджера исполнителя {item.executor14_name} услуги {item.service4} — {executor14_sup}\n'
            f'Чтобы добавить исполнителя №2 услуги {item.service4}, напишите его имя. Если добавлять не нужно, нажмите — Следующий шаг\n'
            f'Хотите отредактировать контакт менеджера исполнителя {item.executor14_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed_next)

        await NewCity.executor24_name.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor24_name)
async def enter_executor24_name(message: types.Message, state: FSMContext):
    executor24_name = message.text
    if executor24_name == 'Следующий шаг':
        data = await state.get_data()
        item: Item = data.get("item")
        await message.answer(f'Чтобы добавить исполнителя №1 услуги {item.service5}, напишите его имя. Если услуги нет, нажмите — 🔚 Закончить добавление',
            reply_markup=kb.reply_ed_end)
        await NewCity.executor15_name.set()
        await state.update_data(item=item)
    elif executor24_name == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне контакт менеджера исполнителя {item.executor14_name} снова')
        await NewCity.executor14_sup.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor24_name = executor24_name

        await message.answer(f'Имя исполнителя №2 услуги {item.service4} — {executor24_name}\n'
        f'Пришлите мне способ оплаты исполнителя {executor24_name} услуги {item.service4}\n'
        'Хотите отредактировать имя исполнителя №2, нажмите ✏️ Редактировать',
        reply_markup=kb.reply_ed)

        await NewCity.executor24_pay.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor24_pay)
async def enter_executor24_pay(message: types.Message, state: FSMContext):
    executor24_pay = message.text
    if executor24_pay == '✏️ Редактировать':
        await message.answer('Пришлите мне имя исполнителя №2 снова')
        await NewCity.executor24_name.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor24_pay = executor24_pay

        await message.answer(f'Cпособ оплаты исполнителя {item.executor24_name} услуги {item.service4} — {executor24_pay}\n'
            f'Пришлите мне контакт для связи с исполнителем {item.executor24_name} услуги {item.service4}\n'
            f'Хотите отредактировать cпособ оплаты исполнителя {item.executor24_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor24_info.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor24_info)
async def enter_executor24_info(message: types.Message, state: FSMContext):
    executor24_info = message.text
    if executor24_info == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне cпособ оплаты исполнителя {item.executor24_name} снова')
        await NewCity.executor24_pay.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor24_info = executor24_info

        await message.answer(f'Контакт для связи с исполнителем {item.executor24_name} услуги {item.service4} — {executor24_info}\n'
            f'Пришлите мне контакт менеджера исполнителя {item.executor24_name} услуги {item.service4}\n'
            f'Хотите отредактировать контакт для связи с исполнителем {item.executor24_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor24_sup.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor24_sup)
async def enter_executor24_sup(message: types.Message, state: FSMContext):
    executor24_sup = message.text
    if executor24_sup == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне контакт для связи с исполнителем {item.executor24_name} снова')
        await NewCity.executor24_info.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor24_sup = executor24_sup

        await message.answer(f'Контакт менеджера исполнителя {item.executor24_name} услуги {item.service4} — {executor24_sup}\n'
            f'Чтобы добавить исполнителя №3, напишите его имя. Если добавлять не нужно, нажмите — Следующий шаг\n'
            f'Хотите отредактировать контакт менеджера исполнителя {item.executor24_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed_next)

        await NewCity.executor34_name.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor34_name)
async def enter_executor34_name(message: types.Message, state: FSMContext):
    executor34_name = message.text
    if executor34_name == 'Следующий шаг':
        data = await state.get_data()
        item: Item = data.get("item")
        await message.answer(f'Чтобы добавить исполнителя №1 услуги {item.service5}, напишите его имя. Если услуги нет, нажмите — 🔚 Закончить добавление',
            reply_markup=kb.reply_ed_end)
        await NewCity.executor15_name.set()
        await state.update_data(item=item)
    elif executor34_name == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне контакт менеджера исполнителя {item.executor24_name} снова')
        await NewCity.executor24_sup.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor34_name = executor34_name

        await message.answer(f'Имя исполнителя №3 услуги {item.service4} — {executor34_name}\n'
        f'Пришлите мне способ оплаты исполнителя {executor34_name} услуги {item.service4}\n'
        'Хотите отредактировать имя исполнителя №3, нажмите ✏️ Редактировать',
        reply_markup=kb.reply_ed)

        await NewCity.executor34_pay.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor34_pay)
async def enter_executor34_pay(message: types.Message, state: FSMContext):
    executor34_pay = message.text
    if executor34_pay == '✏️ Редактировать':
        await message.answer('Пришлите мне имя исполнителя №3 снова')
        await NewCity.executor34_name.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor34_pay = executor34_pay

        await message.answer(f'Cпособ оплаты исполнителя {item.executor34_name} услуги {item.service4} — {executor34_pay}\n'
            f'Пришлите мне контакт для связи с исполнителем {item.executor34_name} услуги {item.service4}\n'
            f'Хотите отредактировать cпособ оплаты исполнителя {item.executor34_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor34_info.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor34_info)
async def enter_executor34_info(message: types.Message, state: FSMContext):
    executor34_info = message.text
    if executor34_info == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне cпособ оплаты исполнителя {item.executor34_name} снова')
        await NewCity.executor34_pay.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor34_info = executor34_info

        await message.answer(f'Контакт для связи с исполнителем {item.executor34_name} услуги {item.service4} — {executor34_info}\n'
            f'Пришлите мне контакт менеджера исполнителя {item.executor34_name} услуги {item.service4}\n'
            f'Хотите отредактировать контакт для связи с исполнителем {item.executor34_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor34_sup.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor34_sup)
async def enter_executor34_sup(message: types.Message, state: FSMContext):
    executor34_sup = message.text
    if executor34_sup == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне контакт для связи с исполнителем {item.executor34_name} снова')
        await NewCity.executor34_info.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor34_sup = executor34_sup

        await message.answer(f'Контакт менеджера исполнителя {item.executor34_name} услуги {item.service4} — {executor34_sup}\n'
            f'Чтобы добавить исполнителя №1 услуги {item.service5}, напишите его имя. Если услуги нет, нажмите — 🔚 Закончить добавление\n'
            f'Хотите отредактировать контакт менеджера исполнителя {item.executor34_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed_end)

        await NewCity.executor15_name.set()
        await state.update_data(item=item)


##########################################################################################################
##########################################################################################################


@dp.message_handler(user_id=admin_id, state=NewCity.executor15_name)
async def enter_executor15_name(message: types.Message, state: FSMContext):
    executor15_name = message.text
    if executor15_name == '🔚 Закончить добавление':
        data = await state.get_data()
        item: Item = data.get("item")
        await item.create()
        await message.answer('Введёные вами данные успешно добавлены!\n'
			'Нажми на /admin, чтобы вернуться в начало')
        await state.reset_state()
    elif executor15_name == '✏️ Редактировать':
        await message.answer(f'Пришлите мне контакт менеджера исполнителя {item.executor34_name} снова')
        await NewCity.executor34_sup.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor15_name = executor15_name

        await message.answer(f'Имя исполнителя №1 услуги {item.service5} — {executor15_name}\n'
            f'Пришлите мне способ оплаты исполнителя {executor15_name} услуги {item.service5}\n'
            f'Хотите отредактировать имя исполнителя №1 услуги {item.service5}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor15_pay.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor15_pay)
async def enter_executor15_pay(message: types.Message, state: FSMContext):
    executor15_pay = message.text
    if executor15_pay == '✏️ Редактировать':
        await message.answer('Пришлите мне имя исполнителя №1 снова')
        await NewCity.executor15_name.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor15_pay = executor15_pay

        await message.answer(f'Cпособ оплаты исполнителя {item.executor15_name} услуги {item.service5} — {executor15_pay}\n'
            f'Пришлите мне контакт для связи с исполнителем {item.executor15_name} услуги {item.service5}\n'
            f'Хотите отредактировать cпособ оплаты исполнителя {item.executor15_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor15_info.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor15_info)
async def enter_executor15_info(message: types.Message, state: FSMContext):
    executor15_info = message.text
    if executor15_info == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне cпособ оплаты исполнителя {item.executor15_name} снова')
        await NewCity.executor15_pay.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor15_info = executor15_info

        await message.answer(f'Контакт для связи с исполнителем {item.executor15_name} услуги {item.service5} — {executor15_info}\n'
            f'Пришлите мне контакт менеджера исполнителя {item.executor15_name} услуги {item.service5}\n'
            f'Хотите отредактировать контакт для связи с исполнителем {item.executor15_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor15_sup.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor15_sup)
async def enter_executor15_sup(message: types.Message, state: FSMContext):
    executor15_sup = message.text
    if executor15_sup == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне контакт для связи с исполнителем {item.executor15_name} снова')
        await NewCity.executor15_info.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor15_sup = executor15_sup

        await message.answer(f'Контакт менеджера исполнителя {item.executor15_name} услуги {item.service5} — {executor15_sup}\n'
            f'Чтобы добавить исполнителя №2 услуги {item.service5}, напишите его имя. Если добавлять не нужно, нажмите — 🔚 Закончить добавление\n'
            f'Хотите отредактировать контакт менеджера исполнителя {item.executor15_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed_end)

        await NewCity.executor25_name.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor25_name)
async def enter_executor25_name(message: types.Message, state: FSMContext):
    executor25_name = message.text
    if executor25_name == '🔚 Закончить добавление':
        data = await state.get_data()
        item: Item = data.get("item")
        await item.create()
        await message.answer('Введёные вами данные успешно добавлены!\n'
			'Нажми на /admin, чтобы вернуться в начало')
        await state.reset_state()
    elif executor25_name == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне контакт менеджера исполнителя {item.executor15_name} снова')
        await NewCity.executor15_sup.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor25_name = executor25_name

        await message.answer(f'Имя исполнителя №2 услуги {item.service5} — {executor25_name}\n'
        f'Пришлите мне способ оплаты исполнителя {executor25_name} услуги {item.service5}\n'
        'Хотите отредактировать имя исполнителя №2, нажмите ✏️ Редактировать',
        reply_markup=kb.reply_ed)

        await NewCity.executor25_pay.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor25_pay)
async def enter_executor25_pay(message: types.Message, state: FSMContext):
    executor25_pay = message.text
    if executor25_pay == '✏️ Редактировать':
        await message.answer('Пришлите мне имя исполнителя №2 снова')
        await NewCity.executor25_name.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor25_pay = executor25_pay

        await message.answer(f'Cпособ оплаты исполнителя {item.executor25_name} услуги {item.service5} — {executor25_pay}\n'
            f'Пришлите мне контакт для связи с исполнителем {item.executor25_name} услуги {item.service5}\n'
            f'Хотите отредактировать cпособ оплаты исполнителя {item.executor25_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor25_info.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor25_info)
async def enter_executor25_info(message: types.Message, state: FSMContext):
    executor25_info = message.text
    if executor25_info == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне cпособ оплаты исполнителя {item.executor25_name} снова')
        await NewCity.executor25_pay.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor25_info = executor25_info

        await message.answer(f'Контакт для связи с исполнителем {item.executor25_name} услуги {item.service5} — {executor25_info}\n'
            f'Пришлите мне контакт менеджера исполнителя {item.executor25_name} услуги {item.service5}\n'
            f'Хотите отредактировать контакт для связи с исполнителем {item.executor25_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor25_sup.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor25_sup)
async def enter_executor25_sup(message: types.Message, state: FSMContext):
    executor25_sup = message.text
    if executor25_sup == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне контакт для связи с исполнителем {item.executor25_name} снова')
        await NewCity.executor25_info.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor25_sup = executor25_sup

        await message.answer(f'Контакт менеджера исполнителя {item.executor25_name} услуги {item.service5} — {executor25_sup}\n'
            f'Чтобы добавить исполнителя №3, напишите его имя. Если добавлять не нужно, нажмите — 🔚 Закончить добавление\n'
            f'Хотите отредактировать контакт менеджера исполнителя {item.executor25_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed_end)

        await NewCity.executor35_name.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor35_name)
async def enter_executor35_name(message: types.Message, state: FSMContext):
    executor35_name = message.text
    if executor35_name == '🔚 Закончить добавление':
        data = await state.get_data()
        item: Item = data.get("item")
        await item.create()
        await message.answer('Введёные вами данные успешно добавлены!\n'
			'Нажми на /admin, чтобы вернуться в начало')
        await state.reset_state()
    elif executor35_name == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне контакт менеджера исполнителя {item.executor25_name} снова')
        await NewCity.executor25_sup.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor35_name = executor35_name

        await message.answer(f'Имя исполнителя №3 услуги {item.service5} — {executor35_name}\n'
        f'Пришлите мне способ оплаты исполнителя {executor35_name} услуги {item.service5}\n'
        'Хотите отредактировать имя исполнителя №3, нажмите ✏️ Редактировать',
        reply_markup=kb.reply_ed)

        await NewCity.executor35_pay.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor35_pay)
async def enter_executor35_pay(message: types.Message, state: FSMContext):
    executor35_pay = message.text
    if executor35_pay == '✏️ Редактировать':
        await message.answer('Пришлите мне имя исполнителя №3 снова')
        await NewCity.executor35_name.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor35_pay = executor35_pay

        await message.answer(f'Cпособ оплаты исполнителя {item.executor35_name} услуги {item.service5} — {executor35_pay}\n'
            f'Пришлите мне контакт для связи с исполнителем {item.executor35_name} услуги {item.service5}\n'
            f'Хотите отредактировать cпособ оплаты исполнителя {item.executor35_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor35_info.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor35_info)
async def enter_executor35_info(message: types.Message, state: FSMContext):
    executor35_info = message.text
    if executor35_info == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне cпособ оплаты исполнителя {item.executor35_name} снова')
        await NewCity.executor35_pay.set()
    else:
        data = await state.get_data()
        item: Item = data.get('item')
        item.executor35_info = executor35_info

        await message.answer(f'Контакт для связи с исполнителем {item.executor35_name} услуги {item.service5} — {executor35_info}\n'
            f'Пришлите мне контакт менеджера исполнителя {item.executor35_name} услуги {item.service5}, изменить его будет нвозможно\n'
            f'Хотите отредактировать контакт для связи с исполнителем {item.executor35_name}, нажмите ✏️ Редактировать',
            reply_markup=kb.reply_ed)

        await NewCity.executor35_sup.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewCity.executor35_sup)
async def enter_executor35_sup(message: types.Message, state: FSMContext):
    executor35_sup = message.text
    if executor35_sup == '✏️ Редактировать':
        data = await state.get_data()
        item: Item = data.get('item')
        await message.answer(f'Пришлите мне контакт для связи с исполнителем {item.executor35_name} снова')
        await NewCity.executor35_info.set()
    else:
        data = await state.get_data()
        item: Item = data.get("item")
        item.executor35_sup = executor35_sup
        await state.update_data(item=item)
        await item.create()
        await message.answer('Введёные вами данные успешно добавлены!\n'
            'Нажми на /admin, чтобы вернуться в начало')
        await state.reset_state()