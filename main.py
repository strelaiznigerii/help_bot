import asyncio
from aiogram.utils import executor
from scheduler import (
    cmd_set_reminder,
    check_scheduled_reminders,
    Command
)
from bot import dp

# Обработчики команд

dp.register_message_handler(cmd_set_reminder, Command('set_reminder'))

if __name__ == '__main__':
    
    loop = asyncio.loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    loop.create_task(check_scheduled_reminders())

    executor.start_polling(dp, skip_updates=True)
