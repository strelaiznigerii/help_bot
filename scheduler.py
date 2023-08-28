import asyncio
import logging
from datetime import datetime
from bot import dp, bot
from models import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters.builtin import Command
from aiogram import types, exceptions

scheduled_reminders = []

# Объявление состояний
class SetReminderState(StatesGroup):
    set_reminder = State()  # Состояние для ввода даты и времени уведомления
    set_text = State()      # Состояние для ввода текста уведомления

# Обработчик команды /set_reminder
@dp.message_handler(Command('set_reminder'))
async def cmd_set_reminder(message: types.Message):
    await message.answer("Введите дату и время для уведомления (в формате ДД.ММ.ГГГГ ЧЧ:ММ):")
    await SetReminderState.set_reminder.set()

@dp.message_handler(lambda message: message.text and '.' in message.text and ':' in message.text, state=SetReminderState.set_reminder)
async def set_reminder(message: types.Message, state: FSMContext):
    try:
        date_str, time_str = message.text.split()
        date_parts = date_str.split('.')
        time_parts = time_str.split(':')
        
        day, month, year = map(int, date_parts)
        hour, minute = map(int, time_parts)
        
        reminder_datetime = datetime(year, month, day, hour, minute)
        
        async with state.proxy() as data:
            data['reminder_datetime'] = reminder_datetime
        
        await message.answer("Введите текст уведомления:")
        await SetReminderState.set_text.set()
        
    except Exception as e:
        await message.answer("Неверный формат даты или время. Попробуйте ещё раз.")
        await state.finish()

@dp.message_handler(lambda message: message.text, state=SetReminderState.set_text)
async def save_reminder(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        reminder_datetime = data['reminder_datetime']
        reminder_text = message.text
        user_id = message.from_user.id
        
        # Сохранение уведомления в базе данных
        db = SessionLocal()
        db.add(Reminder(user_id=user_id, reminder_datetime=reminder_datetime))
        db.commit()
        db.close()
        
        await message.answer("Уведомление сохранено.")
        await state.finish()  # Завершение состояния после успешного сохранения

        # Запланировать отправку уведомления
        await schedule_reminder(reminder_datetime, user_id, reminder_text)

# Асинхронная функция для отправки уведомления
async def send_reminder(reminder_datetime, user_id, reminder_text):
    await asyncio.sleep((reminder_datetime - datetime.now()).seconds)
    try:
        await bot.send_message(user_id, f"Напоминание: {reminder_text}")
    except exceptions.BotBlocked:
        logging.warning(f"Target [ID:{user_id}]: blocked by user")

    # Удалите уведомление из списка запланированных
    for reminder in scheduled_reminders:
        if reminder['reminder_datetime'] == reminder_datetime and reminder['user_id'] == user_id and reminder['reminder_text'] == reminder_text:
            scheduled_reminders.remove(reminder)    

# Асинхронная функция для запланированной отправки уведомления
async def schedule_reminder(reminder_datetime, user_id, reminder_text):
    time_diff = (reminder_datetime - datetime.now()).seconds
    if time_diff > 0:
        scheduled_reminders.append({
            'reminder_datetime': reminder_datetime,
            'user_id': user_id,
            'reminder_text': reminder_text
        })
        await asyncio.sleep(time_diff)
        await send_reminder(reminder_datetime, user_id, reminder_text)

# Проверка и отправка запланированных уведомлений
async def check_scheduled_reminders():
    while True:
        for reminder in scheduled_reminders:
            reminder_datetime = reminder['reminder_datetime']
            user_id = reminder['user_id']
            reminder_text = reminder['reminder_text']
            
            if reminder_datetime <= datetime.now():
                await send_reminder(reminder_datetime, user_id, reminder_text)
                scheduled_reminders.remove(reminder)
        await asyncio.sleep(60)  # Проверка каждую минуту
