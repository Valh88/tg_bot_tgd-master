import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, Redis
from tgbot.handlers import echo
from tgbot.handlers import user
from tgbot.config import config
from tgbot.keyboards.main_menu import main_menu
from tgbot.middlewares.config_middleware import BaseMiddleware, CallbackMiddleware, ThrottlingMiddleware

# from tgbot.models.base import engine
# from tgbot.models.models import Base
logger = logging.getLogger(__name__)


async def main():
    # Base.metadata.create_all(bind=engine)

    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    await main_menu(bot)
    
    if config.tg_bot.use_redis:
        redis: Redis = Redis(host='localhost')
        storage: RedisStorage = RedisStorage(redis=redis)
    else:
        storage: MemoryStorage = MemoryStorage()

    dp: Dispatcher = Dispatcher(storage=storage)
    dp.include_router(echo.router)
    dp.include_router(user.router)
    dp.callback_query.middleware(ThrottlingMiddleware())
    # start
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        # await dp.storage.wait_closed()
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
