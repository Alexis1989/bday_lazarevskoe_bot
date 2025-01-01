import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.handlers import router, set_scheduler

from config_data.config import Config, load_config

# Загружаем конфиг в переменную config
config: Config = load_config()

dp = Dispatcher()


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=config.tg_bot.token)
    dp.include_router(router)

    scheduler_task = asyncio.create_task(
        set_scheduler(bot))  # создаём фоновую задачу
    try:
        await dp.start_polling(bot)
    finally:
        scheduler_task.cancel()  # сигналим о прерывании фоновой задачи
        try:
            await scheduler_task  # даём фоновой задаче шанс обработать сигнал о прерывании
        except asyncio.CancelledError:
            pass  # если всё отработало как надо, то await выкинет CancelledError

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Error')
