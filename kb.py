from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
					InlineKeyboardMarkup, InlineKeyboardButton

# текст кнопок
button_next = KeyboardButton('Следующий шаг')
button_ed = KeyboardButton('✏️ Редактировать')
button_end = KeyboardButton('🔚 Закончить добавление')
button_price = KeyboardButton('📋 Прайс-лист')
button_back = KeyboardButton('🔙 Назад')

# включение в работу кнопок
reply_next = ReplyKeyboardMarkup(resize_keyboard=True, 
	one_time_keyboard=True).add(button_next)

reply_ed = ReplyKeyboardMarkup(resize_keyboard=True, 
	one_time_keyboard=True).add(button_ed)

reply_ed_next = ReplyKeyboardMarkup(resize_keyboard=True, 
	one_time_keyboard=True).add(button_ed).add(button_next)

reply_ed_end = ReplyKeyboardMarkup(resize_keyboard=True, 
	one_time_keyboard=True).add(button_ed).add(button_end)

reply_ed_next_end = ReplyKeyboardMarkup(resize_keyboard=True, 
	one_time_keyboard=True).add(button_ed).add(button_next).add(button_end)

reply_price = ReplyKeyboardMarkup(resize_keyboard=True, 
	one_time_keyboard=True).add(button_price)

reply_back = ReplyKeyboardMarkup(resize_keyboard=True, 
	one_time_keyboard=True).add(button_back)