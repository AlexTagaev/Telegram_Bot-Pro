# импорт модулей
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
import os

# загружаем переменные окружения
load_dotenv('.env_example')

# токен бота
TOKEN = os.getenv('TG_TOKEN')

# создаем кнопки
buttons = [
    InlineKeyboardButton('Русский', callback_data = 'ru'),
    InlineKeyboardButton('English', callback_data = 'en'),
    ]  

# форма inline клавиатуры
form_ver = False
if form_ver:    # если вертикальное расположение
    inline_frame = [
        [buttons[0]], [buttons[1]]
    ]
else:
    inline_frame = [
        [buttons[0], buttons[1]]
    ]    

# создаем inline клавиатуру
inline_keyboard = InlineKeyboardMarkup(inline_frame)

# функция-обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # прикрепляем inline клавиатуру к сообщению
    await update.message.reply_text('Выберите язык общения.', reply_markup=inline_keyboard)
    
# функция-обработчик нажатий на кнопки
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # получаем callback query из update
    query = update.callback_query
    
    context.user_data['lang'] = query.data
    
    # Убираем кнопки
    await update.callback_query.message.edit_reply_markup(None)

    # редактируем сообщение после нажатия
    await query.edit_message_text(text = f'Вы выбрали язык общения: {query.data}')

# функция-обработчик текстовых сообщений
async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    if 'lang' in context.user_data and context.user_data['lang'] == 'ru': 
        await update.message.reply_text('Текстовое сообщение получено!')
    else:
        await update.message.reply_text('We’ve received a message from you!')

# функция-обработчик сообщений с изображениями
async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    if 'lang' in context.user_data and context.user_data['lang'] == 'ru': 
        await update.message.reply_text('Фотография сохранена!')
    else:
        await update.message.reply_text('Photo saved!')
    
    # получаем изображение из апдейта
    quality = -1 # качество -1 - высокое, 0 - низкое
    file = await update.message.photo[quality].get_file()
    
    # сохраняем изображение на диск
    await file.download_to_drive('photos/save.jpg')

# функция-обработчик голосовых сообщений
async def voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    if 'lang' in context.user_data and context.user_data['lang'] == 'ru': 
        await update.message.reply_photo('photos/Gmfn.jpeg', caption = 'Голосовое сообщение получено!')
    else:
        await update.message.reply_photo('photos/Gmfn.jpeg', caption = 'We’ve received a voice message from you!')

# функция "Запуск бота"
def main():

    # создаем приложение и передаем в него токен
    application = Application.builder().token(TOKEN).build()

    # добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))
    
    # добавляем CallbackQueryHandler (для inline кнопок)
    application.add_handler(CallbackQueryHandler(button))
    
    # добавляем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT, text))

    # добавляем обработчик сообщений с фотографиями
    application.add_handler(MessageHandler(filters.PHOTO, image))

    # добавляем обработчик голосовых сообщений
    application.add_handler(MessageHandler(filters.VOICE, voice))

    # запускаем бота (нажать Ctrl-C для остановки бота)
    print('Бот запущен...')    
    application.run_polling()
    print('Бот остановлен')

# проверяем режим запуска модуля
if __name__ == "__main__":      # если модуль запущен как основная программа

    # запуск бота
    main()