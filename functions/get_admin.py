import requests
from database import get_admin_db

code = ''
user_id = ''


async def activator(update, context):
    global code
    with open('../database/admin_code', 'r', encoding='utf-8') as f:
        code = f.read()


async def check_code(update, context):
    global code, user_id
    if update.message.text == code:
        user_id = update.message.chat_id
        get_admin_db.add_id(user_id)
        await update.message.reply_text('Вы успешно активировали режим админа.')
    else:
        await update.message.reply_text('Ваш код неверен.')

