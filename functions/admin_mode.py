import requests
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters
from keyboards import start_keyboard as sk
from keyboards import admin_keyboard
from database import update_db
import sqlite3

spisok = []


async def admin_start(update, context):
    await update.message.reply_text(
        '''Добро пожаловать в режим администратора. Здесь вы можете редактировать, добавлять, изменять расписание или новости.''',
        reply_markup=admin_keyboard.markup)


async def add_schedule(update, context):
    try:
        if not context.args:
            await update.message.reply_text(
                "Напишите эту же команду, но добавьте номер, букву класса, а также все занятия через запятую без пробелов")
            await update.message.reply_text(f'Внимание! Предметы, в названии которых 2+ слов, писать без пробелов!!!')
        else:
            args = context.args[0].split(',')
            lessons = ['Нет', 'Нет', 'Нет', 'Нет', 'Нет', 'Нет', 'Нет', 'Нет', 'Нет', 'Нет']
            for x in range(9):
                if x == len(args):
                    break
                else:
                    lessons.pop(x)
                    lessons.insert(x, args[x])
            con = sqlite3.connect("../database/school_db.sqlite")
            cur = con.cursor()
            result = cur.execute(
                f"""INSERT INTO schedule (number, letter, lesson1, lesson2, lesson3, lesson4, lesson5, lesson6, 
                lesson7,lesson8) VALUES ({int(lessons[0])}, '{lessons[1].lower()}', '{lessons[2]}', '{lessons[3]}',
                '{lessons[4]}', '{lessons[5]}', '{lessons[6]}', '{lessons[7]}','{lessons[8]}', '{lessons[9]}');""").fetchall()
            con.commit()
            cur.close()
            await update.message.reply_text('Операция прошла успешно.')
            update_db.db_updating()
    except Exception:
        await update.message.reply_text('Произошла непревиденная ошибка. Повторите ещё раз')


async def change_schedule(update, context):
    try:
        if not context.args:
            await update.message.reply_text(
                "Напишите эту команду снова, а после номер, букву класса и все занятия через запятую без пробелов.")
            con = sqlite3.connect("../database/school_db.sqlite")
            cur = con.cursor()
            result = cur.execute(f"""SELECT number, letter FROM schedule """).fetchall()
            cur.close()
            con.close()
            classes = []
            for x in sorted(result):
                a = f'{x[0]} {x[1]}'
                classes.append(a)

            a = f'''Доступны расписания для этих классов:'''
            for x in classes:
                if x != classes[-1]:
                    a += f'{x}, '
                else:
                    a += x
            await update.message.reply_text(f'{a}')
            await update.message.reply_text(f'Внимание! Предметы, в названии которых 2+ слов, писать без пробелов!!!')
        else:
            args = context.args[0].split(',')
            lessons = ['Нет', 'Нет', 'Нет', 'Нет', 'Нет', 'Нет', 'Нет', 'Нет', 'Нет', 'Нет']
            for x in range(9):
                if x == len(args):
                    break
                else:
                    lessons.pop(x)
                    lessons.insert(x, args[x])
            con = sqlite3.connect("../database/school_db.sqlite")
            cur = con.cursor()
            result = cur.execute(
                f"""UPDATE schedule SET lesson1 = '{lessons[2]}', lesson2 = '{lessons[3]}', lesson3 = '{lessons[4]}',
                    lesson4 = '{lessons[5]}', lesson5 = '{lessons[6]}', lesson6 = '{lessons[7]}', lesson7 = '{lessons[8]}',
                    lesson8 = '{lessons[9]}'WHERE number = {int(lessons[0])} AND letter = '{lessons[1].lower()}';""").fetchall()
            con.commit()
            cur.close()
            update_db.db_updating()
            await update.message.reply_text('Операция прошла успешно.')
    except Exception:
        await update.message.reply_text('Возникла непредвиденная ошибка.')


async def delete_schedule(update, context):
    if not context.args:
        await update.message.reply_text(
            "Напишите эту команду снова, а после номер и букву класса, расписание для которого вы хотите удалить.")
        con = sqlite3.connect("../database/school_db.sqlite")
        cur = con.cursor()
        result = cur.execute(f"""SELECT number, letter FROM schedule """).fetchall()
        cur.close()
        con.close()
        classes = []
        for x in sorted(result):
            a = f'{x[0]} {x[1]}'
            classes.append(a)

        a = f'''Доступны расписания для этих классов:'''
        for x in classes:
            if x != classes[-1]:
                a += f'{x}, '
            else:
                a += x
        await update.message.reply_text(f'{a}')
    else:
        info = context.args
        class_number = info[0]
        class_letter = info[1].lower()
        con = sqlite3.connect("../database/school_db.sqlite")
        cur = con.cursor()
        result = cur.execute(
            f"""DELETE FROM schedule WHERE letter = '{class_letter}' AND number = {int(class_number)} ;""").fetchall()
        con.commit()
        cur.close()
        update_db.db_updating()
        await update.message.reply_text('Операция прошла успешно.')


new = []


async def add_news(update, context):
    await update.message.reply_text('Напишите заголовок новости')
    return 1


async def add_news_content(update, context):
    global new
    new.append(update.message.text)
    await update.message.reply_text('Напишите текст новости')
    return 2


async def ask_image(update, context):
    new.append(update.message.text)
    await update.message.reply_text('Хотите добавить фото? да/нет')
    return 3


async def handler(update, context):
    global new
    if update.message.text == 'Нет' or update.message.text == 'нет':
        con = sqlite3.connect("../database/school_db.sqlite")
        cur = con.cursor()
        result = cur.execute(
            f"""INSERT INTO news (title, content) VALUES ('{new[0]}', '{new[1]}');""").fetchall()
        con.commit()
        cur.close()
        update_db.db_updating()
        await update.message.reply_text('Операция прошла успешно.')
        return ConversationHandler.END
    elif update.message.text == 'Да' or update.message.text == 'да':
        return 4


async def add_news_image(update, context):
    await update.message.reply_text(
        '''Отправьте одну фотогорафию новости.
Если таковой нет, то напишите "нет"(если напишите любое другое слово, возможно появления ошибки!!!)''')
    return 5


async def add_to_db(update, context):
    global new
    ab = ''
    if type(update.message.text) != 'str':
        ab = update.message.photo[-1].file_id
        file_path = await context.bot.get_file(update.message.photo[-1].file_id)
        image_url = f'https://api.telegram.org/file/bot7004000633:AAGsS_tAo_2iJe-DJ5G6YjcL8Sy_2-Rk8K4/{file_path}'
        image_data = requests.get(image_url)
        with open(f'../images/{ab}.png', 'wb') as f:
            f.write(image_data.content)
    else:
        ab = None
    con = sqlite3.connect("../database/school_db.sqlite")
    cur = con.cursor()
    result = cur.execute(
        f"""INSERT INTO news (title, content, image) VALUES ('{new[0]}', '{new[1]}', '{ab}.png');""").fetchall()
    con.commit()
    cur.close()
    update_db.db_updating()
    await update.message.reply_text('Операция прошла успешно.')


async def stop(update, context):
    await update.message.reply_text(f'Добро пожаловать в официального telegram-бота нашей старшей школы!',
                                    reply_markup=sk.markup)
    return ConversationHandler.END


async def delete_news(update, context):
    if not context.args:
        await update.message.reply_text(
            "Напишите эту команду снова, а после заголовок новости, которую вы хотите удалить.")
        con = sqlite3.connect("../database/school_db.sqlite")
        cur = con.cursor()
        result = cur.execute(f"""SELECT title FROM news""").fetchall()
        cur.close()
        con.close()

        a = f'''Заголовки новостей:'''
        for x in result:
            for y in x:
                if y != result[-1][-1]:
                    a += f'{y}, '
                else:
                    a += y
        await update.message.reply_text(f'{a}')
    else:
        info = context.args
        title = info[0]
        con = sqlite3.connect("../database/school_db.sqlite")
        cur = con.cursor()
        result = cur.execute(
            f"""DELETE FROM news WHERE title = '{title}' ;""").fetchall()
        con.commit()
        cur.close()
        update_db.db_updating()
        await update.message.reply_text('Операция прошла успешно.')


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('add_news', add_news)],
    states={
        1: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_news_content)],
        2: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_image)],
        3: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler)],
        4: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_news_image)],
        5: [MessageHandler(filters.PHOTO, add_to_db)]
    },

    fallbacks=[CommandHandler('start', stop)]
)
