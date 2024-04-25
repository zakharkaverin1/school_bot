from telegram.ext import Application, CommandHandler, filters, MessageHandler
from keyboards import start_keyboard as sk
from raspisanie import hi, print_schedule
from get_admin import activator, check_code
from admin_mode import admin_start, add_schedule, change_schedule, delete_schedule, conv_handler, delete_news
from database import check_admins
from check_news import show_news, list_news

code_asking = False


async def start(update, context):
    await update.message.reply_text(f'Добро пожаловать в официального telegram-бота нашей старшей школы!',
                                    reply_markup=sk.markup)


async def schedule(update, context):
    await hi(update, context)


async def messageHandler(update, context):
    global code_asking
    if update.message.text == 'Вернуться назад':
        await start(update, context)
    elif code_asking:
        await check_code(update, context)
        code_asking = False
    if '⬅️' in update.message.text or '➡️' in update.message.text:
        await context.bot.deleteMessage(message_id=update.message.message_id, chat_id=update.message.chat_id)
        await list_news(update, context)


async def get_admin(update, context):
    global code_asking
    yes_or_no = False
    for x in check_admins.check_admins():
        if update.message.chat_id == x[0]:
            yes_or_no = True
            break
    if not yes_or_no:
        code_asking = True
        await activator(update, context)
        await update.message.reply_text(f'Введите код.')
    else:
        await update.message.reply_text(f'Вы уже активировали администраторский режим.')


async def adminka(update, context):
    yes_or_no = False
    for x in check_admins.check_admins():
        if update.message.chat_id == x[0]:
            yes_or_no = True
            break
    if yes_or_no:
        await admin_start(update, context)
    else:
        await update.message.reply_text(f'Вы не активировали администраторский режим.')


async def news(update, context):
    await show_news(update, context)


application = Application.builder().token('7004000633:AAGsS_tAo_2iJe-DJ5G6YjcL8Sy_2-Rk8K4').build()
if __name__ == '__main__':
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("schedule", schedule))
    application.add_handler(CommandHandler('print_schedule', print_schedule))
    application.add_handler(CommandHandler('news', news))
    application.add_handler(CommandHandler("admin_activator", get_admin))
    application.add_handler(CommandHandler('admin_mode', adminka))
    application.add_handler(CommandHandler("add_schedule", add_schedule))
    application.add_handler(CommandHandler("change_schedule", change_schedule))
    application.add_handler(CommandHandler("delete_schedule", delete_schedule))
    application.add_handler(CommandHandler("delete_news", delete_news))
    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.TEXT, messageHandler))
    application.run_polling()
