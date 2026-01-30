"""
Admin bilan bog'lanish handler moduli
Admin va dasturchi ma'lumotlarini ko'rsatish
"""

from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_USERNAME, ADMIN_PHONE, DEVELOPER_USERNAME, DEVELOPER_PHONE
from keyboards.main_keyboards import get_back_to_menu_keyboard

async def contact_admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Admin bilan bog'lanish xabarini ko'rsatish
    Faqat shaxsiy chatda ishlaydi
    
    Admin va dasturchi ma'lumotlarini chiqaradi
    """
    query = update.callback_query
    await query.answer()
    
    # Faqat shaxsiy chatda ishlash
    if update.effective_chat.type != "private":
        return
    
    text = "👨‍💼 ADMIN BILAN BOG'LANISH\n\n"
    text += f"📱 Admin: @{ADMIN_USERNAME}\n"
    text += f"📞 Telefon: {ADMIN_PHONE}\n\n"
    text += f"👨‍💻 Dasturchi: @{DEVELOPER_USERNAME}\n"
    text += f"📞 Telefon: {DEVELOPER_PHONE}"
    
    await query.edit_message_text(
        text,
        reply_markup=get_back_to_menu_keyboard()
    )
