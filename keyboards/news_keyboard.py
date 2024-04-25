from telegram import ReplyKeyboardMarkup

reply_keyboard = [['⬅️(Новое)', '➡️(Старое)'], ['Вернуться назад']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

reply_keyboard1 = [['⬅️(Новое)', 'Вернуться назад']]
markup1 = ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=False)

reply_keyboard2 = [['➡️(Старое)', 'Вернуться назад']]
markup2 = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=False)
