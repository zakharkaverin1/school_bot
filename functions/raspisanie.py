from database import schedule_db
import sqlite3

class_number = 0
class_letter = ''


async def hi(update, context):
    await update.message.reply_text('Напишите командy /print_schedule, добавив номер и букву вашего класса (раздельно)')
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


async def print_schedule(update, context):
    try:
        global class_number, class_letter
        info = context.args
        class_number = info[0]
        class_letter = info[1].lower()
        itog = list(schedule_db.schedule_printing(class_number, class_letter)[0])
        await update.message.reply_text(f'''Расписание {class_number} {class_letter} класса:
Первый урок: {itog[2]}
Второй урок: {itog[3]}
Третий урок: {itog[4]}
Четвертый урок: {itog[5]}
Пятый урок: {itog[6]}
Шестой урок: {itog[7]}
Седьмой урок: {itog[8]}
Восьмой урок: {itog[9]}
''')
    except IndexError:
        await update.message.reply_text(
            f'Возможно, введеные вами данные некорректны. Убедитесь что такой класс существует и попробуйте ещё раз.')
    except Exception:
        await update.message.reply_text('Возникла непредвиденная ошибка.')
