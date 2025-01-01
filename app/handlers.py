from aiogram import Router, Bot, F
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.utils import markdown
from aiogram.enums import ParseMode
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import app.keyboards as kb
from app.utils import find_birthdays, find_contacts

router = Router()
scheduler = AsyncIOScheduler(timezone='Europe/Moscow')


@router.message(CommandStart())
async def process_start_command(message: Message):
    # scheduler.add_job(send_birthday_cron, trigger='cron', hour=21, minute=57, start_date=datetime.now(),
    #                  kwargs={'bot': bot, 'user_id': -1001719812219})
    # scheduler.start()
    await message.answer(
        'Привет!\nЭтот бот присылает дни рождения сотрудников\n\n'
        'Отправь /birthday, чтобы узнать у кого сегодня день рождение'
    )


# Получить дни рождения сотрудников по текущей дате /birthday
@router.message(Command("birthday"))
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


@router.message(Command("find_contacts"))
async def process_birthday_command(message: Message, command: CommandObject):
    find_str = command.args.split()
    result = find_contacts(find_str[0])

    await message.answer('Найдены контакты сотрудников', reply_markup=kb.kb_names(result))


@router.callback_query(F.data.startswith('name_'))
async def get_contact(callback: CallbackQuery):
    name = callback.data.split('_')[1].replace("_", " ")
    await callback.message.answer(f'name')


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


async def set_scheduler(bot: Bot):
    scheduler.add_job(send_birthday_cron, trigger='cron', hour=22, minute=33, start_date=datetime.now(),
                      kwargs={'bot': bot, 'user_id': -1001719812219})
    scheduler.start()
