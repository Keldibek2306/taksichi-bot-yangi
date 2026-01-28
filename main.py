"""
Telegram Bot - Taksi va Po'chta Xizmati
Versiya: 1.0
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from handlers import router
from scheduler import start_scheduler

# Logging sozlamalari
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Bot asosiy funksiyasi"""
    # Bot va Dispatcher yaratish
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    # Routerni ro'yxatdan o'tkazish
    dp.include_router(router)
    
    # Rejalashtiruvchini ishga tushirish
    start_scheduler(bot)
    
    logger.info("Bot ishga tushdi!")
    
    try:
        # Botni ishga tushirish
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=True
        )
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot to'xtatildi")
    except Exception as e:
        logger.error(f"Xatolik yuz berdi: {e}")
