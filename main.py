import asyncio
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import tg_bot_token
# Create a bot instance and set up the dispatcher
bot = Bot(token=tg_bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Define a command handler for the /start command
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Welcome! Use /set_reminder to set a reminder.")

# Define a command handler for the /set_reminder command
@dp.message_handler(commands=['set_reminder'])
async def set_reminder_command(message: types.Message):
    await message.reply("Please enter the message and the time (in HH:MM format) for the reminder, separated by a space.")

@dp.message_handler()
async def set_reminder(message: types.Message):
    try:
        text, time = message.text.split(' ', 1)
        # Save the reminder details in a database or any other storage mechanism
        # Schedule a task to send the reminder at the specified time using asyncio.sleep()
        reminder_time = datetime.strptime(time, "%H:%M")
        current_time = datetime.now()
        time_difference = (reminder_time - current_time).total_seconds()
        if time_difference > 0:
            await asyncio.sleep(time_difference)
            await message.reply(f"Reminder: {text}")
        else:
            await message.reply("Invalid time. Please enter a future time.")
    except ValueError:
        await message.reply("Invalid format. Please enter the message and the time (in HH:MM format).")
async def main():
    await dp.start_polling()
    loop = asyncio.get_running_loop()
    loop.create_task(dp.start_polling())
    loop.run_forever()

# Start the bot
if __name__ == '__main__':
    asyncio.run(main())
