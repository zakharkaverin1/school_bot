from telegram import ReplyKeyboardMarkup

reply_keyboard = [['/schedule', '/news'], ['/admin_mode', '/admin_activator', 'Вернуться назад']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
