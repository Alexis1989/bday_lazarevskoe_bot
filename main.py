import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.utils import markdown
from aiogram.enums import ParseMode
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from environs import Env

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config_data.config import Config, load_config

from utils.utils import find_birthdays, find_contacts

router = Router()
# Загружаем конфиг в переменную config
config: Config = load_config()

bot = Bot(token=config.tg_bot.token)

# env = Env()  # Создаем экземпляр класса Env
# env.read_env()  # Методом read_env() читаем файл .env и загружаем из него переменные в окружение

# BOT_TOKEN = env('BOT_TOKEN')

# Создаем объекты бота и диспетчера
# bot = Bot(token=BOT_TOKEN)
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


@dp.message(Command("find_contacts"))
async def process_birthday_command(message: Message, command: CommandObject):
    find_str = command.args.split()
    result = find_contacts(find_str[0])

    await message.answer('Найдены контакты сотрудников', reply_markup=kb_names(result))


def kb_names(names):
    keyboard = InlineKeyboardBuilder()

    for name in names:
        keyboard.row(InlineKeyboardButton(
            text=f"{name}", callback_data=f"name_{name.replace(" ", "_")}"))

    return keyboard.as_markup()


@dp.callback_query(F.data.startswith('name_'))
async def get_contact(callback: CallbackQuery):
    name = callback.data.split('_')[1].replace("_", " ")
    await callback.message.answer(f'name')


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
    # dp.include_router(router)
    # dp.run_polling(bot)
