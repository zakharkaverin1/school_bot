from keyboards import news_keyboard
from database import news_db
import os

num_of_new = -1
news_list = 0
last_id = 0
keyboard = news_keyboard.markup


async def show_news(update, context):
    global num_of_new, news_list, last_id, keyboard
    directory = "../images"
    images = os.listdir(directory)
    all = news_db.get_all_news()
    news = []
    for x in all:
        new = []
        for y in x:
            new.append(y)
        news.append(new)
    news_list = len(news)
    if num_of_new == -1:
        keyboard = news_keyboard.markup2
    elif num_of_new == -news_list:
        keyboard = news_keyboard.markup1
    else:
        keyboard = news_keyboard.markup
    if news[num_of_new][2] in images:
        await context.bot.send_photo(chat_id=update.message.chat_id, photo=f'../images/{news[num_of_new][2]}',
                                     parse_mode='html', reply_markup=keyboard,
                                     caption=f'''<b>{news[num_of_new][0]}</b>\n{news[num_of_new][1]}''')
        last_id = update.message.message_id - 1
    else:
        await update.message.reply_text(f'''<b>{news[num_of_new][0]}</b>\n{news[num_of_new][1]}''',
                                        parse_mode='html',
                                        reply_markup=keyboard)
        last_id = update.message.message_id - 1


async def list_news(update, context):
    global num_of_new, news_list, last_id
    if '➡️' in update.message.text:
        if num_of_new != -news_list:
            num_of_new -= 1
            await context.bot.deleteMessage(message_id=update.message.message_id - 1,
                                            chat_id=update.message.chat_id)
            await show_news(update, context)
    elif '⬅️' in update.message.text:
        if num_of_new < -1:
            num_of_new += 1
            await context.bot.deleteMessage(message_id=update.message.message_id - 1,
                                            chat_id=update.message.chat_id)
            await show_news(update, context)
