import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils import markdown
from aiogram.enums import ParseMode
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.utils import find_birthdays

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather
BOT_TOKEN = '8178973869:AAHP6jnoiNcRRlrIKKYQrf2J5dqGxnfD9xg'

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

# Этот хэндлер будет срабатывать на команду "/start"


@dp.message(CommandStart())
async def process_start_command(message: Message):
    # scheduler.add_job(send_birthday_cron, trigger='cron', hour=21, minute=57, start_date=datetime.now(),
    #                  kwargs={'bot': bot, 'user_id': -1001719812219})
    # scheduler.start()
    await message.answer(
        'Привет!\nЭтот бот присылает дни рождения сотрудников\n\n'
        'Отправь /birthday, чтобы узнать у кого сегодня день рождение'
    )


async def send_birthday_cron(bot: Bot, user_id: int):
    birthdays_today, anniversary_today = find_birthdays()
    result = ""

    if len(birthdays_today) > 0:
        result += f"Сегодня день рождения {'отмечают наши замечательные коллеги' if len(
            birthdays_today) > 1 else 'отмечает наш прекрасный коллега'} 🎂:\n\n"
        for item in birthdays_today:
            result += markdown.text(
                f"🔸 <b>{item['name']}</b>\n         <i>{item['position']}</i>\n\n")
    if len(anniversary_today) > 0:
        result += f"Сегодня {'отмечают юбилей наши коллеги' if len(
            anniversary_today) > 1 else 'отмечает юбилей наш коллега'} 🎉:\n\n"
        for item in anniversary_today:
            result += markdown.text(
                f"🔸 <b>{item['name']}</b>\n         <i>{item['position']}</i>\n\n")

    if len(result) > 0:
        await bot.send_message(chat_id=user_id, text=result, parse_mode=ParseMode.HTML)


@dp.message(Command("birthday"))
async def process_birthday_command(message: Message):
    birthdays_today, anniversary_today = find_birthdays()
    result = ""

    if len(birthdays_today) > 0:
        result += f"Сегодня день рождения {'отмечают наши замечательные коллеги' if len(
            birthdays_today) > 1 else 'отмечает наш прекрасный коллега'} 🎂:\n\n"
        for item in birthdays_today:
            result += markdown.text(
                f"🔸 <b>{item['name']}</b>\n         <i>{item['position']}</i>\n\n")
    if len(anniversary_today) > 0:
        result += f"Сегодня {'отмечают юбилей наши коллеги' if len(
            anniversary_today) > 1 else 'отмечает юбилей наш коллега'} 🎉:\n\n"
        for item in anniversary_today:
            result += markdown.text(
                f"🔸 <b>{item['name']}</b>\n         <i>{item['position']}</i>\n\n")

    if len(result) > 0:
        await message.answer(result, parse_mode=ParseMode.HTML)
    else:
        await message.answer('Сегодня нет дней рождений', parse_mode=ParseMode.HTML)


async def set_scheduler():
    scheduler.add_job(send_birthday_cron, trigger='cron', hour=9, minute=5, start_date=datetime.now(),
                      kwargs={'bot': bot, 'user_id': -1001719812219})
    scheduler.start()


async def main():
    # logging.basicConfig(level=logging.INFO)
    scheduler_task = asyncio.create_task(
        set_scheduler())  # создаём фоновую задачу
    try:
        await dp.start_polling(bot)
    finally:
        scheduler_task.cancel()  # сигналим о прерывании фоновой задачи
        try:
            await scheduler_task  # даём фоновой задаче шанс обработать сигнал о прерывании
        except asyncio.CancelledError:
            pass  # если всё отработало как надо, то await выкинет CancelledError

if __name__ == '__main__':
    asyncio.run(main())
    # dp.run_polling(bot)
