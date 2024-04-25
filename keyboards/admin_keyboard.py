from telegram import ReplyKeyboardMarkup

reply_keyboard = [['/add_news', '/delete_news'],
                  ['/add_schedule', '/change_schedule', '/delete_schedule', 'Вернуться назад']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
