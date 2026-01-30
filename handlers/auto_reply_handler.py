"""
Avtomatik javob berish handler moduli
Bot admin bo'lgan guruh va kanallarda xabarlarga avtomatik javob beradi
"""

from telegram import Update, Chat
from telegram.ext import ContextTypes
from telegram.error import TelegramError
import logging

from config import AUTO_REPLY_MESSAGES, AUTO_REPLY_KEYWORDS

logger = logging.getLogger(__name__)

# Global o'zgaruvchi - admin bo'lgan guruhlar
ADMIN_CHATS = set()

def detect_keyword_type(text: str) -> str:
    """
    Xabardagi kalit so'zlarni aniqlash va mos javob turini qaytarish
    """
    if not text:
        return None
    
    text_lower = text.lower()
    
    # Taksi kalit so'zlarini tekshirish
    for keyword in AUTO_REPLY_KEYWORDS["taksi"]:
        if keyword in text_lower:
            return "taksi"
    
    # Yo'lovchi kalit so'zlarini tekshirish
    for keyword in AUTO_REPLY_KEYWORDS["yolovchi"]:
        if keyword in text_lower:
            return "yolovchi"
    
    # Umumiy kalit so'zlarni tekshirish
    for keyword in AUTO_REPLY_KEYWORDS["umumiy"]:
        if keyword in text_lower:
            return "umumiy"
    
    return None

async def is_bot_admin(chat_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """
    Botning guruhda admin ekanligini tekshirish
    """
    try:
        bot_member = await context.bot.get_chat_member(chat_id, context.bot.id)
        return bot_member.status in ["administrator", "creator"]
    except Exception as e:
        logger.error(f"Error checking admin status in {chat_id}: {e}")
        return False

async def handle_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Guruh xabarlarini qayta ishlash
    
    1. Guruhni admin chat lar ro'yxatiga qo'shish
    2. Kalit so'z borligini tekshirish
    3. Avtomatik javob berish
    """
    # Faqat guruh va superguruh uchun
    if not update.effective_chat or update.effective_chat.type not in [Chat.GROUP, Chat.SUPERGROUP]:
        return
    
    # Botning o'z xabariga javob bermaslik
    if update.effective_user and update.effective_user.id == context.bot.id:
        return
    
    # Xabar mavjudligini tekshirish
    if not update.message or not update.message.text:
        return
    
    chat_id = update.effective_chat.id
    
    # Bot admin ekanligini tekshirish va ro'yxatga qo'shish
    is_admin = await is_bot_admin(chat_id, context)
    
    if is_admin:
        # Admin chat lar ro'yxatiga qo'shish
        if chat_id not in ADMIN_CHATS:
            ADMIN_CHATS.add(chat_id)
            logger.info(f"Added admin chat: {chat_id} ({update.effective_chat.title})")
        
        # Kalit so'zlarni aniqlash
        keyword_type = detect_keyword_type(update.message.text)
        
        if keyword_type:
            # Javob xabarini olish
            reply_text = AUTO_REPLY_MESSAGES.get(keyword_type)
            
            if reply_text:
                try:
                    # Bot username ni olish
                    bot_info = await context.bot.get_me()
                    bot_username = bot_info.username or "bot"
                    
                    # Javob xabarini formatlash
                    formatted_reply = reply_text.replace("{bot_username}", bot_username)
                    
                    # Javob berish
                    await update.message.reply_text(
                        formatted_reply,
                        disable_web_page_preview=True
                    )
                    logger.info(f"Auto-reply sent in {chat_id} for keyword type: {keyword_type}")
                    
                except Exception as e:
                    logger.error(f"Error sending auto-reply in {chat_id}: {e}")

def get_admin_chats() -> list:
    """
    Admin bo'lgan guruhlar ro'yxatini qaytarish
    """
    return list(ADMIN_CHATS)

def add_admin_chat(chat_id: int, chat_title: str = None) -> None:
    """
    Guruhni admin chat lar ro'yxatiga qo'shish
    """
    ADMIN_CHATS.add(chat_id)
    logger.info(f"Manually added admin chat: {chat_id} ({chat_title})")

async def handle_bot_added_to_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Bot guruhga qo'shilganda yoki admin qilinganda
    """
    if not update.my_chat_member:
        return
    
    chat = update.effective_chat
    new_status = update.my_chat_member.new_chat_member.status
    
    # Agar bot admin yoki a'zo qilingan bo'lsa
    if new_status in ["administrator", "member"]:
        # Admin ekanligini tekshirish
        is_admin = await is_bot_admin(chat.id, context)
        
        if is_admin:
            ADMIN_CHATS.add(chat.id)
            logger.info(f"Bot added as admin to: {chat.id} ({chat.title})")
            
            # Guruhga xabar yuborish
            try:
                bot_info = await context.bot.get_me()
                welcome_msg = f"""👋 Assalomu alaykum!

🤖 Men taksi va yo'lovchi topish botiman.

✅ Avtomatik javob yoqildi
✅ Reklama har 5 minutda yuboriladi

Foydalanish uchun: @{bot_info.username} bo'tdan foydalaning """
                
                await context.bot.send_message(chat.id, welcome_msg)
            except Exception as e:
                logger.error(f"Error sending welcome message: {e}")
    
    # Agar bot guruhdan chiqarilgan bo'lsa
    elif new_status in ["left", "kicked"]:
        if chat.id in ADMIN_CHATS:
            ADMIN_CHATS.discard(chat.id)
            logger.info(f"Bot removed from group: {chat.id}")

