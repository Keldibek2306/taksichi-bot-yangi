"""
Avtomatik xabarlar uchun rejalashtiruvchi
"""
import asyncio
from aiogram import Bot
from config import MAIN_GROUP_ID, MESSAGE_INTERVAL


async def send_periodic_message(bot: Bot):
    """Har 15 daqiqada guruhga xabar yuborish"""
    while True:
        try:
            await asyncio.sleep(MESSAGE_INTERVAL)
            
            message_text = """
🚕 <b>TAKSI VA YO'LOVCHI TOPISH</b>

Tezkor va qulay yo'l-yo'riq uchun botimizdan foydalaning!

👉 Botni ishga tushirish: /start

📌 Xizmatlar:
• Yo'lovchi sifatida sayohat qilish
• Taksichi sifatida yo'lovchi topish
• Po'chta jo'natish

Botni bosing va buyurtma bering! 👇
"""
            
            await bot.send_message(
                chat_id=MAIN_GROUP_ID,
                text=message_text
            )
        except Exception as e:
            print(f"Xatolik: Periodic message - {e}")
            await asyncio.sleep(60)  # Xatolik bo'lsa 1 daqiqa kutib qayta urinish


def start_scheduler(bot: Bot):
    """Rejalashtiruvchini ishga tushirish"""
    asyncio.create_task(send_periodic_message(bot))
