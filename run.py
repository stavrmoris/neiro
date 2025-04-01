import os
import asyncio
import logging
from datetime import datetime
from pytz import timezone

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import utils.database as db
from __init__ import setup
from config import TOKEN


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

# Функция для обновления лимитов пользователей
async def update_user_limits():
    logging.info("Запуск задачи обновления лимитов пользователей")
    now = datetime.now()
    users_list = db.get_user_list()

    for user in users_list:
        try:
            logging.debug(f"Обработка пользователя {user}")
            date_str = db.get_variable(user, 'data')
            if date_str is not None:
                date_to_compare = datetime.strptime(date_str, "%Y-%m-%d").date()
                if now.date() <= date_to_compare:
                    db.set_variable(user, 'gpt4o-usage', 100)
                    db.set_variable(user, 'dalle-usage', 30)
                    db.set_variable(user, 'gpt4omini-usage', 100000)
                    logging.info(f"Лимиты пользователя {user} обновлены")
                else:
                    db.set_variable(user, 'gpt4o-usage', 50)
                    db.set_variable(user, 'dalle-usage', 15)
                    db.set_variable(user, 'gpt4omini-usage', 100)
                    logging.info(f"Лимиты пользователя {user} установлены по умолчанию")
            else:
                db.set_variable(user, 'gpt4omini-usage', 50)
                logging.info(f"Лимиты пользователя {user} установлены по умолчанию (дата не указана)")
        except Exception as e:
            logging.error(f"Ошибка при обновлении лимитов пользователя {user}: {e}")

# Основная функция для запуска бота
async def main():
    # Инициализация бота и диспетчера
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    dp = Dispatcher(storage=MemoryStorage())
    setup(dp)

    # Настройка планировщика задач
    scheduler = AsyncIOScheduler(timezone=timezone('Europe/Moscow'))
    scheduler.add_job(update_user_limits, 'cron', hour=15, minute=34)  # Запуск каждый день в 19:23
    scheduler.start()
    logging.info("Планировщик задач запущен")

    try:
        # Запуск бота
        logging.info("Бот запущен")
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")
    finally:
        # Остановка планировщика и закрытие сессии бота
        scheduler.shutdown()
        await bot.session.close()
        logging.info("Бот остановлен")

# Точка входа
if __name__ == '__main__':
    asyncio.run(main())