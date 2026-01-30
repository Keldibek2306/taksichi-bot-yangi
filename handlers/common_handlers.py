# handlers/common_handlers.py
"""
Umumiy handlerlar - comment va confirm uchun
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes

from config import States
from utils.order_manager import order_manager
from keyboards.main_keyboards import get_confirm_keyboard

logger = logging.getLogger(__name__)

async def comment_choice_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Umumiy comment choice handler
    Pochta va yo'lovchi uchun ishlaydi
    Faqat shaxsiy chatda ishlaydi
    """
    query = update.callback_query
    await query.answer()
    
    # Faqat shaxsiy chatda ishlash
    if update.effective_chat.type != "private":
        return
    
    user_id = query.from_user.id
    choice = query.data  # "comment_yes" yoki "comment_no"
    
    logger.info(f"💬 comment_choice_callback: user_id={user_id}, choice={choice}")
    
    # Foydalanuvchi mode'ni aniqlash
    mode = order_manager.get_user_data(user_id, "mode")
    
    if mode == "package":
        await handle_package_comment_choice(update, context, choice)
    elif mode == "passenger":
        await handle_passenger_comment_choice(update, context, choice)
    elif mode == "driver":
        await handle_driver_comment_choice(update, context, choice)
    else:
        logger.error(f"Unknown mode: {mode}")
        await query.edit_message_text(
            "❌ Xatolik yuz berdi. Iltimos, /start ni bosing."
        )

async def handle_package_comment_choice(update, context, choice):
    """Pochta uchun comment choice"""
    from config import DIRECTIONS, PACKAGE_TYPES
    
    query = update.callback_query
    user_id = query.from_user.id
    
    if choice == "comment_yes":
        # Qo'shimcha ma'lumot yozishni so'rash
        order_manager.set_state(user_id, States.PACKAGE_COMMENT)
        
        direction = order_manager.get_user_data(user_id, "direction")
        pkg_type = order_manager.get_user_data(user_id, "package_type")
        weight = order_manager.get_user_data(user_id, "weight")
        phone = order_manager.get_user_data(user_id, "phone")
        
        # Formatalash
        formatted_phone = f"+{phone[:3]} {phone[3:5]} {phone[5:8]} {phone[8:10]} {phone[10:12]}"
        
        await query.edit_message_text(
            f"📍 Yo'nalish: {DIRECTIONS[direction]}\n"
            f"📋 Pochta turi: {PACKAGE_TYPES[pkg_type]}\n"
            f"⚖️ Og'irligi: {weight} kg\n"
            f"📞 Telefon: {formatted_phone}\n\n"
            "✍️ Qo'shimcha ma'lumotni yozing:\n"
            "(Masalan: ichida nima bor, qanday qadoqlangan)"
        )
    
    elif choice == "comment_no":
        # Qo'shimcha ma'lumot yo'q
        order_manager.set_user_data(user_id, "comment", "")
        order_manager.set_state(user_id, States.PACKAGE_CONFIRM)
        
        direction = order_manager.get_user_data(user_id, "direction")
        pkg_type = order_manager.get_user_data(user_id, "package_type")
        weight = order_manager.get_user_data(user_id, "weight")
        phone = order_manager.get_user_data(user_id, "phone")
        
        formatted_phone = f"+{phone[:3]} {phone[3:5]} {phone[5:8]} {phone[8:10]} {phone[10:12]}"
        
        text = "📋 BUYURTMA TASDIQLANSINMI?\n\n"
        text += f"📍 Yo'nalish: {DIRECTIONS[direction]}\n"
        text += f"📋 Pochta turi: {PACKAGE_TYPES[pkg_type]}\n"
        text += f"⚖️ Og'irligi: {weight} kg\n"
        text += f"📞 Telefon: {formatted_phone}\n"
        
        await query.edit_message_text(
            text,
            reply_markup=get_confirm_keyboard()
        )

async def handle_passenger_comment_choice(update, context, choice):
    """Yo'lovchi uchun comment choice"""
    from config import DIRECTIONS
    
    query = update.callback_query
    user_id = query.from_user.id
    
    if choice == "comment_yes":
        order_manager.set_state(user_id, States.PASSENGER_COMMENT)
        
        direction = order_manager.get_user_data(user_id, "direction")
        count = order_manager.get_user_data(user_id, "count")
        phone = order_manager.get_user_data(user_id, "phone")
        
        formatted_phone = f"+{phone[:3]} {phone[3:5]} {phone[5:8]} {phone[8:10]} {phone[10:12]}"
        
        await query.edit_message_text(
            f"📍 Yo'nalish: {DIRECTIONS[direction]}\n"
            f"👥 Yo'lovchilar: {count} kishi\n"
            f"📞 Telefon: {formatted_phone}\n\n"
            "✍️ Qo'shimcha ma'lumotni yozing:"
        )
    
    elif choice == "comment_no":
        order_manager.set_user_data(user_id, "comment", "")
        order_manager.set_state(user_id, States.PASSENGER_CONFIRM)
        
        direction = order_manager.get_user_data(user_id, "direction")
        count = order_manager.get_user_data(user_id, "count")
        phone = order_manager.get_user_data(user_id, "phone")
        
        formatted_phone = f"+{phone[:3]} {phone[3:5]} {phone[5:8]} {phone[8:10]} {phone[10:12]}"
        
        text = "📋 BUYURTMA TASDIQLANSINMI?\n\n"
        text += f"📍 Yo'nalish: {DIRECTIONS[direction]}\n"
        text += f"👥 Yo'lovchilar: {count} kishi\n"
        text += f"📞 Telefon: {formatted_phone}\n"
        
        await query.edit_message_text(
            text,
            reply_markup=get_confirm_keyboard()
        )

async def handle_driver_comment_choice(update, context, choice):
    """Haydovchi uchun comment choice"""
    from config import DIRECTIONS
    
    query = update.callback_query
    user_id = query.from_user.id
    
    if choice == "comment_yes":
        order_manager.set_state(user_id, States.DRIVER_COMMENT)
        
        direction = order_manager.get_user_data(user_id, "direction")
        seats = order_manager.get_user_data(user_id, "seats")
        phone = order_manager.get_user_data(user_id, "phone")
        
        formatted_phone = f"+{phone[:3]} {phone[3:5]} {phone[5:8]} {phone[8:10]} {phone[10:12]}"
        
        await query.edit_message_text(
            f"📍 Yo'nalish: {DIRECTIONS[direction]}\n"
            f"🚕 Bo'sh joylar: {seats} ta\n"
            f"📞 Telefon: {formatted_phone}\n\n"
            "✍️ Qo'shimcha ma'lumotni yozing:"
        )
    
    elif choice == "comment_no":
        order_manager.set_user_data(user_id, "comment", "")
        order_manager.set_state(user_id, States.DRIVER_CONFIRM)
        
        direction = order_manager.get_user_data(user_id, "direction")
        seats = order_manager.get_user_data(user_id, "seats")
        phone = order_manager.get_user_data(user_id, "phone")
        
        formatted_phone = f"+{phone[:3]} {phone[3:5]} {phone[5:8]} {phone[8:10]} {phone[10:12]}"
        
        text = "📋 BUYURTMA TASDIQLANSINMI?\n\n"
        text += f"📍 Yo'nalish: {DIRECTIONS[direction]}\n"
        text += f"🚕 Bo'sh joylar: {seats} ta\n"
        text += f"📞 Telefon: {formatted_phone}\n"
        
        await query.edit_message_text(
            text,
            reply_markup=get_confirm_keyboard()
        )

async def confirm_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Umumiy confirm handler
    Faqat shaxsiy chatda ishlaydi
    """
    query = update.callback_query
    await query.answer()
    
    # Faqat shaxsiy chatda ishlash
    if update.effective_chat.type != "private":
        return
    
    user_id = query.from_user.id
    choice = query.data  # "confirm_yes" yoki "confirm_no"
    
    logger.info(f"✅ confirm_callback: user_id={user_id}, choice={choice}")
    
    mode = order_manager.get_user_data(user_id, "mode")
    
    if mode == "package":
        from handlers.package_handler import package_confirm_callback
        await package_confirm_callback(update, context)
    elif mode == "passenger":
        from handlers.passenger_handler import passenger_confirm_callback
        await passenger_confirm_callback(update, context)
    elif mode == "driver":
        from handlers.driver_handler import driver_confirm_callback
        await driver_confirm_callback(update, context)
