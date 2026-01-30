"""
Kanal obunasini tekshirish handler moduli
/start buyrug'i va kanal obunasini tekshirish funksiyalari
"""

from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from config import REQUIRED_CHANNELS
from keyboards.main_keyboards import (
    get_channel_subscription_keyboard,
    get_main_menu_keyboard
)
from utils.order_manager import order_manager

async def check_user_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """
    Foydalanuvchining barcha kanallarga obuna bo'lganligini tekshirish
    
    Returns:
        bool: True - barcha kanallarga obuna, False - obuna emas
    """
    user_id = update.effective_user.id
    
    for channel in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(
                chat_id=channel["id"],
                user_id=user_id
            )
            # Agar foydalanuvchi kanalda emas yoki ban qilingan bo'lsa
            if member.status in ["left", "kicked"]:
                return False
        except TelegramError:
            # Xatolik bo'lsa, obuna yo'q deb hisoblaymiz
            return False
    
    return True

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /start buyrug'ini qayta ishlash
    
    Oqim:
    1. Faqat shaxsiy chatda ishlaydi
    2. Obunani tekshirish
    3. Agar obuna bo'lmasa - kanal linklari ko'rsatish
    4. Agar obuna bo'lsa - bosh menyuni ko'rsatish
    """
    # Faqat shaxsiy chatda ishlash
    if update.effective_chat.type != "private":
        return
    
    user = update.effective_user
    
    # Foydalanuvchini /start bosganlar ro'yxatiga qo'shish
    order_manager.add_started_user(user.id)
    
    # Oldingi holatlarni tozalash
    order_manager.clear_user_data(user.id)
    
    # Obunani tekshirish
    is_subscribed = await check_user_subscription(update, context)
    
    if not is_subscribed:
        # Obuna bo'lmagan
        await update.message.reply_text(
            "🔔 Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:",
            reply_markup=get_channel_subscription_keyboard()
        )
    else:
        # Obuna bo'lgan - bosh menyuni ko'rsatish
        welcome_text = f"👋 Assalomu alaykum, {user.first_name}!\n\n"
        welcome_text += "🚖 Taksi va Pochta xizmati botiga xush kelibsiz!\n\n"
        welcome_text += "Quyidagi xizmatlardan birini tanlang:"
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=get_main_menu_keyboard()
        )

async def check_subscription_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    "Obunani tekshirish" tugmasi bosilganda
    
    Faqat shaxsiy chatda ishlaydi
    Obunani qayta tekshirish va natijasiga qarab haraket qilish
    """
    query = update.callback_query
    await query.answer()
    
    # Faqat shaxsiy chatda ishlash
    if update.effective_chat.type != "private":
        return
    
    user = query.from_user
    
    # Obunani tekshirish
    is_subscribed = await check_user_subscription(update, context)
    
    if not is_subscribed:
        # Hali ham obuna bo'lmagan
        # Qaysi kanallarga obuna bo'lmaganligini aniqlash
        not_subscribed = []
        
        for channel in REQUIRED_CHANNELS:
            try:
                member = await context.bot.get_chat_member(
                    chat_id=channel["id"],
                    user_id=user.id
                )
                if member.status in ["left", "kicked"]:
                    not_subscribed.append(channel["name"])
            except TelegramError:
                not_subscribed.append(channel["name"])
        
        # Xabar yaratish
        channels_text = ", ".join(not_subscribed)
        await query.edit_message_text(
            f"❌ Siz {channels_text} kanallariga obuna bo'lmadingiz.\n\n"
            f"Iltimos, barcha kanallarga obuna bo'lib qayta urinib ko'ring:",
            reply_markup=get_channel_subscription_keyboard()
        )
    else:
        # Barcha kanallarga obuna bo'lgan
        welcome_text = f"✅ Obuna tasdiqlandi!\n\n"
        welcome_text += f"👋 Xush kelibsiz, {user.first_name}!\n\n"
        welcome_text += "Quyidagi xizmatlardan birini tanlang:"
        
        await query.edit_message_text(
            welcome_text,
            reply_markup=get_main_menu_keyboard()
        )

async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Bosh menyuga qaytish callback funksiyasi
    Faqat shaxsiy chatda ishlaydi
    """
    query = update.callback_query
    await query.answer()
    
    # Faqat shaxsiy chatda ishlash
    if update.effective_chat.type != "private":
        return
    
    user = query.from_user
    
    # Foydalanuvchi ma'lumotlarini tozalash
    order_manager.clear_user_data(user.id)
    
    menu_text = "🏠 Bosh menyu\n\n"
    menu_text += "Quyidagi xizmatlardan birini tanlang:"
    
    await query.edit_message_text(
        menu_text,
        reply_markup=get_main_menu_keyboard()
    )
