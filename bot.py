from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # Импорт MemoryStorage
#from config import API_TOKEN
from aiogram.dispatcher.filters import Command, Text
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import logging
from aiogram.dispatcher.filters.builtin import Command


logging.basicConfig(level=logging.INFO)
API_TOKEN = "6133666647:AAH_lL-XcBRF3BPah4NqLKKbe2AlLfaP7n0"
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()  # Инициализация хранилища
dp = Dispatcher(bot, storage=storage)  # Передача хранилища в диспетчер
dp.middleware.setup(LoggingMiddleware())

# Обработчик команды /start
@dp.message_handler(Command('start'))
async def cmd_start(message: types.Message):
    formatted_text = f'Привет, {message.from_user.first_name}! \n' \
                     'Я бот, который ответит на все вопросы, которые могут возникнуть у сотрудника УРК. \n' \
                     'Если хочешь открыть меню, то набери команду /menu и выбери кнопку по интересующему тебя вопросу.' 
    await message.answer(formatted_text)

# Обработчик кнопки "Ответы на все вопросы УРК"
@dp.message_handler(Command('menu'))
async def btn_show_text(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Отпуск')
    btn2 = types.KeyboardButton('Расписание')
    btn3 = types.KeyboardButton('Больничные')
    btn4 = types.KeyboardButton('Мотивация')
    btn5 = types.KeyboardButton('ЗП')
    btn6 = types.KeyboardButton('Ревью')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    
    await message.answer("Ответы на все вопросы УРК", reply_markup=markup)

# Обработчик кнопки "Кнопка 1"
@dp.message_handler(Text(equals='Отпуск'))
async def btn1_handler(message: types.Message):
    formatted_text = '<b>Отпуск</b> \n\n' \
    'График составляется на год вперед (28 дней должны быть отгуляны обязательно).\n' \
    'Самое главное: вы сами должны помнить, когда у вас отпуск, чтобы ровно за 2 недели отправить заявление на согласование через ЭДО. Согласующий - ваш любименький РГ.\n' \
    'Проверяйте периодически график и наличие активности в расписании в WFM. Если активности нет – говорите РГ, заводите задачу через forge/mytinkoff.\n' \
    'Помимо основных 28 дней из-за ненормированного графика копится еще 3 дополнительных дня отпуска в год, которые можно прибавить потом к основному.\n' \
    'Доп дни согласуются с руководством. Они могут быть проставлены вами заранее на год вперед.\n'\
    'Но посреди года только по согласованию, если есть какая-то действительно в этом необходимость.\nНо вы можете получить деньгами за доп дни.\n' \
    'Нельзя брать отпуск в последние 2 недели декабря и первые 2 недели января после выхода. Так как там всегда потенциально большая нагрузка на наш Департамент.'

    await message.answer(formatted_text, parse_mode=types.ParseMode.HTML)
# Обработчик кнопки "Кнопка 2"
@dp.message_handler(Text(equals='Расписание'))
async def btn2_handler(message: types.Message):
    formatted_text = '<b>Расписание</b> \n\n' \
                     'Расписание мы смотрим в WFM. \n' \
                     'Пожелания к расписанию нужно указывать обязательно, о начале сбора приходит новость в новости Twork. \n' \
                     'У нас плавающий график (выходные могут быть рабочими), а сам рабочий день ненормированный. \n' \
                     'Есть также свободные часы (это время, когда работать не надо), отслеживай их в своем графике и не пропускай, так как они не переносятся.'   

    await message.answer(formatted_text, parse_mode=types.ParseMode.HTML)

# Обработчик кнопки "Кнопка 3"
@dp.message_handler(Text(equals='Больничные'))
async def btn3_handler(message: types.Message):
    formatted_text = '<b>Больничные</b> \n\n' \
                     'Если вы заболели, предупредите РГ и отправляетесь к врачу или вызывайте его на дом. \n' \
                     'После того, как врач озвучил вам даты БЛ, вам надо завести задачу [добавить текст]. \n' \
                     'После закрытия БЛ надо выполнить еще несколько действий[описать действия]. \n'

    await message.answer(formatted_text, parse_mode=types.ParseMode.HTML)

# Обработчик кнопки "Кнопка 4"
@dp.message_handler(Text(equals='Мотивация'))
async def btn4_handler(message: types.Message):
    formatted_text = '[Нужно описать блок]'
    await message.answer(formatted_text, parse_mode=types.ParseMode.HTML)

# Обработчик кнопки "Кнопка 5"
@dp.message_handler(Text(equals='ЗП'))
async def btn5_handler(message: types.Message):
    formatted_text = '<b>ЗП</b> \n\n' \
                     'ЗП приходит 3 и 17. Если 3 и 17 – выходные, то в последний рабочий день перед этими датами. \n' \
                     'Премия приходит с 10 по 15 (за предыдущий месяц). \n' \
                     'Отпускные приходят в ПН (за неделю до отпуска) или в ЧТ/ПТ (за 3 дня до отпуска). \n'
    await message.answer(formatted_text, parse_mode=types.ParseMode.HTML)

# Обработчик кнопки "Кнопка 6"
@dp.message_handler(Text(equals='Ревью'))
async def btn6_handler(message: types.Message):
    formatted_text = '<b>Ревью</b> \n\n' \
                     'Ревью – это цели на квартал. В году 4 квартала. \n' \
                     'С 1 по 15 число (января, апреля, июля, октября) надо составить ревью: минимум 1 рабочая задача и минимум 1 задача на развитие. \n' \
                     'Перед составлением ревью, обязательно следуйте рекомендациям.'
    await message.answer(formatted_text, parse_mode=types.ParseMode.HTML)    

'''if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)'''
