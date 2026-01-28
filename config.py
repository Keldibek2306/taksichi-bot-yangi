"""
Bot konfiguratsiya sozlamalari
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Bot asosiy sozlamalari
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Majburiy kanallar
CHANNELS = [
    {
        'id': int(os.getenv('CHANNEL_1_ID')),
        'name': os.getenv('CHANNEL_1_NAME'),
        'link': os.getenv('CHANNEL_1_LINK')
    },
    {
        'id': int(os.getenv('CHANNEL_2_ID')),
        'name': os.getenv('CHANNEL_2_NAME'),
        'link': os.getenv('CHANNEL_2_LINK')
    },
    {
        'id': int(os.getenv('CHANNEL_3_ID')),
        'name': os.getenv('CHANNEL_3_NAME'),
        'link': os.getenv('CHANNEL_3_LINK')
    }
]

# Guruh ID
MAIN_GROUP_ID = int(os.getenv('MAIN_GROUP_ID'))

# Admin ma'lumotlari
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PHONE = os.getenv('ADMIN_PHONE')
DEVELOPER_USERNAME = os.getenv('DEVELOPER_USERNAME')
DEVELOPER_PHONE = os.getenv('DEVELOPER_PHONE')

# Yo'nalishlar
DIRECTIONS = {
    'beshariq_toshkent': '🚕 Beshariq ➡️ Toshkent',
    'toshkent_beshariq': '🚕 Toshkent ➡️ Beshariq'
}

# Po'chta yo'nalishlari
POSTAL_DIRECTIONS = {
    'beshariq_toshkent': '📦 Beshariq ➡️ Toshkent',
    'toshkent_beshariq': '📦 Toshkent ➡️ Beshariq'
}

# Po'chta turlari
POSTAL_TYPES = {
    'document': '📄 Hujjat',
    'package': '📦 Paket',
    'electronics': '💻 Elektronika',
    'other': '📋 Boshqa'
}

# Odamlar soni
PASSENGER_COUNTS = [1, 2, 3, 4]

# Og'irlik diapazoni (kg)
WEIGHT_RANGE = list(range(1, 31))

# Xabar yuborish intervali (15 daqiqa)
MESSAGE_INTERVAL = 900  # sekund
