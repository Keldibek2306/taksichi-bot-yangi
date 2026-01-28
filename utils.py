"""
Yordamchi funksiyalar
"""
from aiogram import Bot
from config import CHANNELS, DIRECTIONS, POSTAL_DIRECTIONS, POSTAL_TYPES


async def check_user_subscription(bot: Bot, user_id: int) -> tuple[bool, list]:
    """
    Foydalanuvchining barcha kanallarga obuna bo'lganligini tekshirish
    
    Returns:
        tuple: (barcha_kanalga_obuna, obuna_bolmagan_kanallar)
    """
    not_subscribed = []
    
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel['id'], user_id=user_id)
            if member.status in ['left', 'kicked']:
                not_subscribed.append(channel)
        except Exception:
            not_subscribed.append(channel)
    
    return len(not_subscribed) == 0, not_subscribed


def format_direction(direction_key: str, mode: str = 'taxi') -> str:
    """Yo'nalishni formatlash"""
    if mode == 'postal':
        return POSTAL_DIRECTIONS.get(direction_key, direction_key)
    return DIRECTIONS.get(direction_key, direction_key)


def format_postal_type(postal_type_key: str) -> str:
    """Po'chta turini formatlash"""
    return POSTAL_TYPES.get(postal_type_key, postal_type_key)


def create_passenger_announcement(user_data: dict, user_full_name: str) -> str:
    """Yo'lovchi e'lonini yaratish"""
    direction = format_direction(user_data['direction'])
    count = user_data['count']
    phone = user_data['phone']
    comment = user_data.get('comment', '')
    
    text = f"""
🚗 <b>YO'LOVCHI QIDIRYAPTI</b>

👤 Ism: {user_full_name}
📍 Yo'nalish: {direction}
👥 Odamlar soni: {count} kishi
📱 Telefon: {phone}
"""
    
    if comment:
        text += f"\n💬 Qo'shimcha: {comment}"
    
    return text


def create_driver_announcement(user_data: dict, user_full_name: str) -> str:
    """Haydovchi e'lonini yaratish"""
    direction = format_direction(user_data['direction'])
    count = user_data['count']
    phone = user_data['phone']
    comment = user_data.get('comment', '')
    
    text = f"""
🚕 <b>TAKSICHI YO'LOVCHI QIDIRYAPTI</b>

👤 Haydovchi: {user_full_name}
📍 Yo'nalish: {direction}
💺 Bo'sh joylar: {count} kishi
📱 Telefon: {phone}
"""
    
    if comment:
        text += f"\n💬 Qo'shimcha: {comment}"
    
    return text


def create_postal_announcement(user_data: dict, user_full_name: str) -> str:
    """Po'chta e'lonini yaratish"""
    direction = format_direction(user_data['direction'], mode='postal')
    postal_type = format_postal_type(user_data['postal_type'])
    weight = user_data['weight']
    phone = user_data['phone']
    comment = user_data.get('comment', '')
    
    text = f"""
📦 <b>PO'CHTA JO'NATISH</b>

👤 Ism: {user_full_name}
📍 Yo'nalish: {direction}
📋 Turi: {postal_type}
⚖️ Og'irligi: {weight} kg
📱 Telefon: {phone}
"""
    
    if comment:
        text += f"\n💬 Qo'shimcha: {comment}"
    
    return text


def get_not_subscribed_message(not_subscribed_channels: list) -> str:
    """Obuna bo'lmagan kanallar haqida xabar"""
    if not not_subscribed_channels:
        return ""
    
    channels_text = "\n".join([f"• {channel['name']}" for channel in not_subscribed_channels])
    
    return f"""
❌ Siz quyidagi kanallarga obuna bo'lmagansiz:

{channels_text}

Iltimos, barcha kanallarga obuna bo'ling va "✅ Obunani tekshirish" tugmasini bosing.
"""
