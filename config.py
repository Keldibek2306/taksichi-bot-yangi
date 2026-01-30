"""
Bot konfiguratsiya fayli
Bu yerda bot sozlamalari, kanal ID lari va konstantalar saqlanadi
"""

import os
from enum import IntEnum
from dotenv import load_dotenv

# .env faylidan o'zgaruvchilarni yuklash
load_dotenv()

# Bot tokeni
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Kanal ID lari va linklari
CHANNEL_1_ID = int(os.getenv("CHANNEL_1_ID"))
CHANNEL_1_LINK = os.getenv("CHANNEL_1_LINK")

CHANNEL_2_ID = int(os.getenv("CHANNEL_2_ID"))
CHANNEL_2_LINK = os.getenv("CHANNEL_2_LINK")

CHANNEL_3_ID = int(os.getenv("CHANNEL_3_ID"))
CHANNEL_3_LINK = os.getenv("CHANNEL_3_LINK")

# Asosiy guruh ID si
MAIN_GROUP_ID = int(os.getenv("MAIN_GROUP_ID"))

# Barcha kanallar ro'yxati
REQUIRED_CHANNELS = [
    {"id": CHANNEL_1_ID, "link": CHANNEL_1_LINK, "name": "UZ Dasturlash Asosi"},
    {"id": CHANNEL_2_ID, "link": CHANNEL_2_LINK, "name": "UZ Dasturlash Asosi"},
    {"id": CHANNEL_3_ID, "link": CHANNEL_3_LINK, "name": "Bizning Kanal"},
]

# Admin ma'lumotlari
ADMIN_USERNAME = "u019db"
ADMIN_PHONE = "+998 93 603 88 15"

DEVELOPER_USERNAME = "Dasturchi_101"
DEVELOPER_PHONE = "+998 99 565 41 04"

# Yo'nalishlar
DIRECTIONS = {
    "beshariq_toshkent": "Beshariq → Toshkent",
    "toshkent_beshariq": "Toshkent → Beshariq"
}

# Pochta turlari
PACKAGE_TYPES = {
    "document": "📄 Hujjat",
    "package": "📦 Paket",
    "electronics": "📱 Elektronika",
    "other": "📋 Boshqa"
}

# Conversation state lari
class States(IntEnum):
    """Conversation davomida foydalaniladigan holatlar (IntEnum)"""
    # Umumiy
    START = 0
    
    # Yo'lovchi holatlari
    PASSENGER_DIRECTION = 1
    PASSENGER_COUNT = 2
    PASSENGER_PHONE = 3
    PASSENGER_COMMENT_CHOICE = 4
    PASSENGER_COMMENT = 5
    PASSENGER_CONFIRM = 6
    
    # Taksichi holatlari
    DRIVER_DIRECTION = 7
    DRIVER_SEATS = 8
    DRIVER_PHONE = 9
    DRIVER_COMMENT_CHOICE = 10
    DRIVER_COMMENT = 11
    DRIVER_CONFIRM = 12
    
    # Pochta holatlari
    PACKAGE_DIRECTION = 13
    PACKAGE_TYPE = 14
    PACKAGE_WEIGHT = 15
    PACKAGE_PHONE = 16
    PACKAGE_COMMENT_CHOICE = 17
    PACKAGE_COMMENT = 18
    PACKAGE_CONFIRM = 19

# Reklama xabari matni (MAIN_GROUP uchun)
AD_MESSAGE = """🚖 TAKSI VA POCHTA XIZMATI

Beshariq ↔️ Toshkent yo'nalishida:
✅ Taksi chaqirish
✅ Yo'lovchi topish  
✅ Pochta jo'natish

🤖 Bu guruhda elon yaratish uchun bu bo't dan foydalaning 👉  @beshariq_tax_bot """

# Avtomatik javob xabarlari (admin bo'lgan guruh/kanallar uchun)
AUTO_REPLY_MESSAGES = {
    "taksi": """🚖 TEZ VA OSON TAKSI TOPISH UCHUN!

Bizning bot orqali:
✅ Tez taksi chaqiring
✅ Yo'lovchilar bilan bog'laning
✅ Ishonchli xizmat

🤖 @{bot_username}  bo'tdan foydalaning """,
    
    "yolovchi": """👥 TEZ VA OSON YO'LOVCHI TOPISH UCHUN!

Bizning bot orqali:
✅ Yo'lovchilarni toping
✅ Tez buyurtma bering
✅ Qulay narxlar

🤖 @{bot_username} bo'tdan foydalaning """,
    
    "umumiy": """🚖 TAKSI VA YO'LOVCHI TOPISH UCHUN!

Bizning bot orqali:
✅ Tez taksi chaqiring
✅ Yo'lovchilarni toping
✅ Pochta jo'nating

🤖 @{bot_username} bo'tdan foydalaning """
}

# Reklama intervali (soniyalarda)
MAIN_GROUP_AD_INTERVAL = 400  # 15 minut (MAIN_GROUP uchun)
ALL_GROUPS_AD_INTERVAL = 700  # 5 minut (barcha admin bo'lgan guruhlar uchun)

# Avtomatik javob uchun kalit so'zlar
AUTO_REPLY_KEYWORDS = {
    "taksi": ["taksi", "taxi", "mashina", "haydovchi", "driver"],
    "yolovchi": ["yo'lovchi", "yolovchi", "passenger", "odam", "joy"],
    "umumiy": ["pochta", "paket", "yuborish", "jo'natish", "xizmat", "service"]
}