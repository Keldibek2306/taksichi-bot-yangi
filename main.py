"""
Telegram Bot - Taksi va Pochta Xizmati
Beshariq-Toshkent yo'nalishida taksi va pochta xizmatini taqdim etuvchi bot

Asosiy funksiyalar:
- Kanal obunasini tekshirish
- Yo'lovchi sifatida taksi chaqirish
- Taksichi sifatida e'lon berish
- Pochta jo'natish
- Buyurtmalarni band qilish
- Avtomatik reklama
"""

import asyncio
import logging
from datetime import datetime

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ChatMemberHandler
)

from config import (
    BOT_TOKEN,
    MAIN_GROUP_ID,
    AD_MESSAGE,
    MAIN_GROUP_AD_INTERVAL,
    ALL_GROUPS_AD_INTERVAL,
    States
)

# Handler modullarini import qilish
from handlers.channel_check import (
    start_command,
    check_subscription_callback,
    main_menu_callback
)
from handlers.auto_reply_handler import (
    handle_group_message,
    get_admin_chats,
    handle_bot_added_to_group
)
from handlers.passenger_handler import (
    passenger_mode_start,
    passenger_direction_callback,
    passenger_count_callback,
    passenger_phone_handler,
    passenger_comment_choice_callback,
    passenger_comment_handler,
    passenger_confirm_callback
)
from handlers.driver_handler import (
    driver_mode_start,
    driver_direction_callback,
    driver_seats_callback,
    driver_phone_handler,
    driver_comment_choice_callback,
    driver_comment_handler,
    driver_confirm_callback
)
from handlers.package_handler import (
    package_mode_start,
    package_direction_callback,
    package_type_callback,
    package_weight_callback,
    package_phone_handler,
    package_comment_choice_callback,
    package_comment_handler,
    package_confirm_callback
)
from handlers.admin_handler import contact_admin_callback
from handlers.booking_handler import book_order_callback

from utils.order_manager import order_manager

# Common handlers import
from handlers.common_handlers import (
    comment_choice_callback,
    confirm_callback
)

# Logging sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def cancel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Bekor qilish tugmasi bosilganda
    Foydalanuvchi ma'lumotlarini tozalash va bosh menyuga qaytarish
    Faqat shaxsiy chatda ishlaydi
    """
    query = update.callback_query
    await query.answer()
    
    # Faqat shaxsiy chatda ishlash
    if update.effective_chat.type != "private":
        return
    
    user_id = query.from_user.id
    
    # Foydalanuvchi ma'lumotlarini tozalash
    order_manager.clear_user_data(user_id)
    
    await query.edit_message_text(
        "❌ Jarayon bekor qilindi.\n\n"
        "🏠 Bosh menyu:",
        reply_markup=None
    )
    
    # Bosh menyuni ko'rsatish
    await main_menu_callback(update, context)

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Oddiy matn xabarlarini qayta ishlash
    Foydalanuvchi holatiga qarab telefon raqam yoki komment qabul qilish
    Faqat shaxsiy chatda ishlaydi (guruhda ishlamas)
    """
    # Faqat shaxsiy chatda ishlash
    if update.effective_chat.type != "private":
        return
    
    user_id = update.effective_user.id
    state = order_manager.get_state(user_id)
    
    logger.info(f"📝 handle_text_message: user_id={user_id}, state={state}")
    
    if state == States.PASSENGER_PHONE:
        # Yo'lovchi telefon raqamini kiritmoqda
        await passenger_phone_handler(update, context)
    
    elif state == States.PASSENGER_COMMENT:
        # Yo'lovchi komment yozmoqda
        await passenger_comment_handler(update, context)
    
    elif state == States.DRIVER_PHONE:
        # Taksichi telefon raqamini kiritmoqda
        await driver_phone_handler(update, context)
    
    elif state == States.DRIVER_COMMENT:
        # Taksichi komment yozmoqda
        await driver_comment_handler(update, context)
    
    elif state == States.PACKAGE_PHONE:
        # Pochta jo'natuvchi telefon raqamini kiritmoqda
        await package_phone_handler(update, context)
    
    elif state == States.PACKAGE_COMMENT:
        # Pochta jo'natuvchi komment yozmoqda
        await package_comment_handler(update, context)
    
    else:
        # Noma'lum holat - xabarni o'chirish
        try:
            await update.message.delete()
        except:
            pass
        logger.warning(f"⚠️ handle_text_message: Unknown state {state}")

async def handle_contact_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Contact xabarlarini qayta ishlash
    Foydalanuvchi holatiga qarab telefon raqam qabul qilish
    Faqat shaxsiy chatda ishlaydi
    """
    # Faqat shaxsiy chatda ishlash
    if update.effective_chat.type != "private":
        return
    
    user_id = update.effective_user.id
    state = order_manager.get_state(user_id)
    
    logger.info(f"📱 handle_contact_message: user_id={user_id}, state={state}")
    
    if state == States.PASSENGER_PHONE:
        # Yo'lovchi telefon raqamini jo'natmoqda
        await passenger_phone_handler(update, context)
    
    elif state == States.DRIVER_PHONE:
        # Taksichi telefon raqamini jo'natmoqda
        await driver_phone_handler(update, context)
    
    elif state == States.PACKAGE_PHONE:
        # Pochta jo'natuvchi telefon raqamini jo'natmoqda
        await package_phone_handler(update, context)
    
    else:
        # Noma'lum holat
        logger.warning(f"⚠️ handle_contact_message: Unknown state {state}")

async def universal_direction_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Yo'nalish callback - barcha rejimlar uchun universal
    Foydalanuvchi holatiga qarab to'g'ri handler ga yo'naltiradi
    Faqat shaxsiy chatda ishlaydi
    """
    query = update.callback_query
    await query.answer()
    
    # Faqat shaxsiy chatda ishlash
    if update.effective_chat.type != "private":
        return
    
    user_id = query.from_user.id
    state = order_manager.get_state(user_id)
    
    logger.info(f"📍 universal_direction_callback: user_id={user_id}, state={state}")
    
    if state == States.PASSENGER_DIRECTION:
        await passenger_direction_callback(update, context)
    elif state == States.DRIVER_DIRECTION:
        await driver_direction_callback(update, context)
    elif state == States.PACKAGE_DIRECTION:
        await package_direction_callback(update, context)
    else:
        logger.error(f"❌ universal_direction_callback: Wrong state {state}")

async def universal_count_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Son callback - yo'lovchi va taksichi uchun universal
    Faqat shaxsiy chatda ishlaydi
    """
    query = update.callback_query
    await query.answer()
    
    # Faqat shaxsiy chatda ishlash
    if update.effective_chat.type != "private":
        return
    
    user_id = query.from_user.id
    state = order_manager.get_state(user_id)
    
    logger.info(f"👥 universal_count_callback: user_id={user_id}, state={state}")
    
    if state == States.PASSENGER_COUNT:
        await passenger_count_callback(update, context)
    elif state == States.DRIVER_SEATS:
        await driver_seats_callback(update, context)
    else:
        logger.error(f"❌ universal_count_callback: Wrong state {state}")

async def universal_comment_choice_callback_legacy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    ESKI VERSIYA: Qo'shimcha ma'lumot kerakmi callback (yes/no uchun)
    Faqat eski kodlar bilan mosligi uchun
    Faqat shaxsiy chatda ishlaydi
    """
    query = update.callback_query
    await query.answer()
    
    # Faqat shaxsiy chatda ishlash
    if update.effective_chat.type != "private":
        return
    
    user_id = query.from_user.id
    state = order_manager.get_state(user_id)
    choice = query.data  # "yes" yoki "no"
    
    logger.info(f"💬 universal_comment_choice_callback_legacy: user_id={user_id}, state={state}, choice={choice}")
    
    # Legacy code - faqat yes/no kelganda ishlaydi
    if state == States.PASSENGER_COMMENT_CHOICE:
        await passenger_comment_choice_callback(update, context)
    elif state == States.DRIVER_COMMENT_CHOICE:
        await driver_comment_choice_callback(update, context)
    elif state == States.PACKAGE_COMMENT_CHOICE:
        await package_comment_choice_callback(update, context)
    else:
        logger.error(f"❌ universal_comment_choice_callback_legacy: Wrong state {state}")

async def universal_confirm_callback_legacy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    ESKI VERSIYA: Tasdiqlash callback (confirm_yes/confirm_no uchun)
    Faqat shaxsiy chatda ishlaydi
    """
    query = update.callback_query
    await query.answer()
    
    # Faqat shaxsiy chatda ishlash
    if update.effective_chat.type != "private":
        return
    
    user_id = query.from_user.id
    state = order_manager.get_state(user_id)
    choice = query.data  # "confirm_yes" yoki "confirm_no"
    
    logger.info(f"✅ universal_confirm_callback_legacy: user_id={user_id}, state={state}, choice={choice}")
    
    if state == States.PASSENGER_CONFIRM:
        await passenger_confirm_callback(update, context)
    elif state == States.DRIVER_CONFIRM:
        await driver_confirm_callback(update, context)
    elif state == States.PACKAGE_CONFIRM:
        await package_confirm_callback(update, context)
    else:
        logger.error(f"❌ universal_confirm_callback_legacy: Wrong state {state}")

async def send_advertisement_to_main_group(context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    MAIN_GROUP ga reklama yuborish (har 15 minutda)
    """
    try:
        await context.bot.send_message(
            chat_id=MAIN_GROUP_ID,
            text=AD_MESSAGE
        )
        logger.info(f"Advertisement sent to MAIN_GROUP at {datetime.now()}")
    except Exception as e:
        logger.error(f"Error sending advertisement to MAIN_GROUP: {e}")

async def send_advertisement_to_all_groups(context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Bot admin bo'lgan barcha guruh va kanallarga reklama yuborish (har 5 minutda)
    """
    try:
        # Bot ma'lumotini olish
        bot_info = await context.bot.get_me()
        bot_username = bot_info.username or "bot"
        
        # Barcha admin chat larni olish
        admin_chats = get_admin_chats()
        
        if not admin_chats:
            logger.info("No admin chats found for advertisements")
            return
        
        # Reklama xabari
        ad_text = f"""🚖 TAKSI VA YO'LOVCHI TOPISH!

Beshariq ↔️ Toshkent yo'nalishida:
✅ Tez taksi chaqiring
✅ Yo'lovchilarni toping
✅ Pochta jo'nating

🤖 @{bot_username} shu bo'ttan foydalaning """
        
        # Har bir guruhga yuborish
        sent_count = 0
        for chat_id in admin_chats:
            # MAIN_GROUP ga alohida yuboriladi, uni skip qilamiz
            if chat_id == MAIN_GROUP_ID:
                continue
                
            try:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=ad_text,
                    disable_web_page_preview=True
                )
                sent_count += 1
            except Exception as e:
                logger.error(f"Error sending ad to chat {chat_id}: {e}")
        
        if sent_count > 0:
            logger.info(f"Advertisement sent to {sent_count} admin groups/channels at {datetime.now()}")
    
    except Exception as e:
        logger.error(f"Error in send_advertisement_to_all_groups: {e}")

async def setup_advertisement_jobs(application: Application) -> None:
    """
    Reklama job larni sozlash
    
    1. MAIN_GROUP ga har 15 minutda
    2. Barcha admin guruh/kanallarga har 5 minutda
    """
    job_queue = application.job_queue
    
    # 1. MAIN_GROUP ga har 15 minutda reklama
    job_queue.run_repeating(
        send_advertisement_to_main_group,
        interval=MAIN_GROUP_AD_INTERVAL,
        first=1  # Birinchi marta 10 soniyadan keyin
    )
    
    # 2. Barcha admin guruh/kanallarga har 5 minutda reklama
    job_queue.run_repeating(
        send_advertisement_to_all_groups,
        interval=ALL_GROUPS_AD_INTERVAL,
        first=2  # Birinchi marta 30 soniyadan keyin
    )
    
    logger.info("Advertisement jobs set up successfully")
    logger.info(f"- MAIN_GROUP: every {MAIN_GROUP_AD_INTERVAL} seconds")
    logger.info(f"- All admin groups: every {ALL_GROUPS_AD_INTERVAL} seconds")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Xatoliklarni qayta ishlash
    """
    logger.error(f"Exception while handling an update: {context.error}")
    
    # Agar update mavjud bo'lsa va foydalanuvchiga xabar yuborish mumkin bo'lsa
    if isinstance(update, Update) and update.effective_user:
        try:
            await context.bot.send_message(
                chat_id=update.effective_user.id,
                text="❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring yoki /start bosing."
            )
        except Exception as e:
            logger.error(f"Could not send error message to user: {e}")

def main() -> None:
    """
    Botni ishga tushirish funksiyasi
    Barcha handler larni ro'yxatdan o'tkazish va botni boshlash
    """
    # Application yaratish
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Command handler
    application.add_handler(CommandHandler("start", start_command))
    
    # Callback query handler lar
    # Kanal obunasi
    application.add_handler(CallbackQueryHandler(check_subscription_callback, pattern="^check_subscription$"))
    application.add_handler(CallbackQueryHandler(main_menu_callback, pattern="^main_menu$"))
    
    # Asosiy menyu
    application.add_handler(CallbackQueryHandler(passenger_mode_start, pattern="^mode_passenger$"))
    application.add_handler(CallbackQueryHandler(driver_mode_start, pattern="^mode_driver$"))
    application.add_handler(CallbackQueryHandler(package_mode_start, pattern="^mode_package$"))
    application.add_handler(CallbackQueryHandler(contact_admin_callback, pattern="^contact_admin$"))
    
    # ✅ YANGI: Comment va Confirm uchun umumiy handlerlar
    application.add_handler(CallbackQueryHandler(comment_choice_callback, pattern="^comment_"))
    application.add_handler(CallbackQueryHandler(confirm_callback, pattern="^confirm_"))
    
    # Universal callback handler lar (barcha rejimlar uchun)
    application.add_handler(CallbackQueryHandler(universal_direction_callback, pattern="^dir_"))
    application.add_handler(CallbackQueryHandler(universal_count_callback, pattern="^count_"))
    
    # ✅ ESKI: Legacy handlerlar (yes/no va confirm_yes/confirm_no)
    # Faqat eski keyboard'lar bilan mosligi uchun
    application.add_handler(CallbackQueryHandler(universal_comment_choice_callback_legacy, pattern="^(yes|no)$"))
    application.add_handler(CallbackQueryHandler(universal_confirm_callback_legacy, pattern="^confirm_(yes|no)$"))
    
    # Pochta uchun maxsus callback lar
    application.add_handler(CallbackQueryHandler(package_type_callback, pattern="^pkg_"))
    application.add_handler(CallbackQueryHandler(package_weight_callback, pattern="^weight_"))
    
    # Band qilish
    application.add_handler(CallbackQueryHandler(book_order_callback, pattern="^book_"))
    
    # Bekor qilish
    application.add_handler(CallbackQueryHandler(cancel_callback, pattern="^cancel$"))
    
    # Bot guruhga qo'shilganda yoki admin qilinganda
    application.add_handler(ChatMemberHandler(handle_bot_added_to_group, ChatMemberHandler.MY_CHAT_MEMBER))
    
    # Guruh xabarlarini qayta ishlash (avtomatik javob)
    application.add_handler(MessageHandler(
        filters.ChatType.GROUPS & filters.TEXT & ~filters.COMMAND,
        handle_group_message
    ))
    
    # ✅ YANGI: Contact xabarlarini qayta ishlash
    application.add_handler(MessageHandler(
        filters.CONTACT,
        handle_contact_message
    ))
    
    # Shaxsiy matn xabarlarini qayta ishlash (telefon, komment)
    application.add_handler(MessageHandler(
        filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND,
        handle_text_message
    ))
    
    # Xatolik handler
    application.add_error_handler(error_handler)
    
    # Reklama job larni sozlash
    application.job_queue.run_once(
        lambda context: asyncio.create_task(setup_advertisement_jobs(application)),
        when=1
    )
    
    # Botni ishga tushirish
    logger.info("Bot is starting...")
    logger.info("Auto-reply enabled for admin groups/channels")
    logger.info("Advertisement jobs scheduled")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()