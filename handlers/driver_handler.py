"""
Taksichi rejimi handler moduli
Taksichlar uchun e'lon berish jarayoni
"""

import re
from datetime import datetime
from telegram import (
    Update, 
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    ReplyKeyboardRemove
)
from telegram.ext import ContextTypes

from config import States, DIRECTIONS, MAIN_GROUP_ID
from keyboards.main_keyboards import (
    get_direction_keyboard,
    get_count_keyboard,
    get_yes_no_keyboard,
    get_confirm_keyboard,
    get_main_menu_keyboard
)
from utils.order_manager import order_manager

async def driver_mode_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Taksichi rejimini boshlash
    Yo'nalish tanlashni so'rash
    Faqat shaxsiy chatda ishlaydi
    """
    query = update.callback_query
    await query.answer()
    
    # Faqat shaxsiy chatda ishlash
    if update.effective_chat.type != "private":
        return
    
    user_id = query.from_user.id
    
    # Holatni o'rnatish
    order_manager.set_state(user_id, States.DRIVER_DIRECTION)
    order_manager.set_user_data(user_id, "mode", "driver")
    
    await query.edit_message_text(
        "🚕 TAKSICHI REJIMI\n\n"
        "📍 Yo'nalishni tanlang:",
        reply_markup=get_direction_keyboard()
    )

async def driver_direction_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Yo'nalish tanlagandan keyin
    Bo'sh joylar sonini so'rash
    """
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    direction = query.data.replace("dir_", "")
    
    # Ma'lumotni saqlash
    order_manager.set_user_data(user_id, "direction", direction)
    order_manager.set_state(user_id, States.DRIVER_SEATS)
    
    await query.edit_message_text(
        f"📍 Yo'nalish: {DIRECTIONS[direction]}\n\n"
        "💺 Nechta odam uchun joy bor?",
        reply_markup=get_count_keyboard(4)
    )

async def driver_seats_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Bo'sh joylar soni tanlagandan keyin
    Telefon raqamni so'rash
    """
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    seats = int(query.data.replace("count_", ""))
    
    # Ma'lumotni saqlash
    order_manager.set_user_data(user_id, "seats", seats)
    order_manager.set_state(user_id, States.DRIVER_PHONE)
    
    direction = order_manager.get_user_data(user_id, "direction")
    
    # Telefon raqam jo'natish tugmasi bilan
    phone_keyboard = ReplyKeyboardMarkup(
        [
            [KeyboardButton("📞 Telefon raqamimni jo'natish", request_contact=True)],
            ["📝 Raqamni yozib yuborish"]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    await query.edit_message_text(
        f"📍 Yo'nalish: {DIRECTIONS[direction]}\n"
        f"💺 Bo'sh joylar: {seats} kishi\n\n"
        "📞 Telefon raqamingizni yuboring:"
    )
    
    await context.bot.send_message(
        chat_id=user_id,
        text="Telefon raqamingizni quyidagi formatlarda kiriting:\n"
             "• +998901234567\n"
             "• 998901234567\n"
             "• 901234567\n\n"
             "Yoki tugma orqali jo'nating:",
        reply_markup=phone_keyboard
    )

async def driver_phone_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Telefon raqam yuborilgandan keyin (contact yoki text)
    Qo'shimcha ma'lumot kerakligini so'rash
    """
    user_id = update.effective_user.id
    
    print(f"🚕 DEBUG: driver_phone_handler chaqirildi. User: {user_id}")
    
    # Tekshirish: Faqat DRIVER_PHONE state dagi foydalanuvchilar uchun
    current_state = order_manager.get_state(user_id)
    print(f"🚕 DEBUG: Current state: {current_state}, Expected: {States.DRIVER_PHONE}")
    
    if current_state != States.DRIVER_PHONE:
        print(f"🚕 DEBUG: Wrong state, ignoring")
        return
    
    phone = None
    
    # 1. Agar contact jo'natilgan bo'lsa
    if update.message.contact:
        contact = update.message.contact
        
        # Faqat o'zining raqamini jo'natishini tekshirish
        if contact.user_id != user_id:
            await update.message.reply_text(
                "❌ Iltimos, faqat o'zingizning telefon raqamingizni jo'nating!",
                reply_markup=ReplyKeyboardRemove()
            )
            return
        
        phone = contact.phone_number
        print(f"🚕 DEBUG: Contact phone received: {phone}")
        
    # 2. Agar text yuborilgan bo'lsa
    elif update.message.text:
        text = update.message.text.strip()
        print(f"🚕 DEBUG: Text received: {text}")
        
        # Agar "Raqamni yozib yuborish" tanlangan bo'lsa
        if text == "📝 Raqamni yozib yuborish":
            await update.message.reply_text(
                "📱 Telefon raqamingizni quyidagi formatlarda kiriting:\n\n"
                "• +998901234567\n"
                "• 998901234567\n"
                "• 901234567\n\n"
                "Yoki qaytadan tugmani bosing:",
                reply_markup=ReplyKeyboardMarkup(
                    [[KeyboardButton("📞 Telefon raqamimni jo'natish", request_contact=True)]],
                    resize_keyboard=True,
                    one_time_keyboard=True
                )
            )
            return
        
        # Telefon raqamni tozalash
        cleaned = re.sub(r'\D', '', text)
        print(f"🚕 DEBUG: Cleaned phone: {cleaned}")
        
        # Validatsiya
        if len(cleaned) == 9 and cleaned.startswith(('90', '91', '93', '94', '95', '97', '98', '99')):
            phone = '998' + cleaned
        elif len(cleaned) == 12 and cleaned.startswith('998'):
            phone = cleaned
        elif len(cleaned) == 13 and cleaned.startswith('998'):
            phone = cleaned[1:]
        else:
            await update.message.reply_text(
                f"❌ Noto'g'ri telefon raqami: {text}\n\n"
                "Iltimos, quyidagi formatlarda kiriting:\n"
                "• +998901234567\n"
                "• 998901234567\n"
                "• 901234567",
                reply_markup=ReplyKeyboardMarkup(
                    [
                        [KeyboardButton("📞 Telefon raqamimni jo'natish", request_contact=True)],
                        ["📝 Raqamni yozib yuborish"]
                    ],
                    resize_keyboard=True
                )
            )
            return
    else:
        print(f"🚕 DEBUG: Neither contact nor text")
        return
    
    if phone:
        print(f"🚕 DEBUG: Phone to save: {phone}")
        
        # Telefon raqamni saqlash
        order_manager.set_user_data(user_id, "phone", phone)
        order_manager.set_state(user_id, States.DRIVER_COMMENT_CHOICE)
        
        # Keyboardni olib tashlash
        await update.message.reply_text(
            "✅ Telefon raqamingiz qabul qilindi!",
            reply_markup=ReplyKeyboardRemove()
        )
        
        direction = order_manager.get_user_data(user_id, "direction")
        seats = order_manager.get_user_data(user_id, "seats")
        
        # Formatalash
        formatted_phone = f"+{phone[:3]} {phone[3:5]} {phone[5:8]} {phone[8:10]} {phone[10:12]}"
        
        # ✅ get_yes_no_keyboard() ishlatamiz
        await context.bot.send_message(
            chat_id=user_id,
            text=f"📍 Yo'nalish: {DIRECTIONS[direction]}\n"
                 f"💺 Bo'sh joylar: {seats} kishi\n"
                 f"📞 Telefon: {formatted_phone}\n\n"
                 "💬 Qo'shimcha ma'lumot yozasizmi?",
            reply_markup=get_yes_no_keyboard()  # ✅ comment_yes/comment_no qaytaradi
        )

# ✅ ESKI VERSIYA (legacy) - comment_choice_callback ga o'tkazadi
async def driver_comment_choice_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Qo'shimcha ma'lumot kerakmi degan savolga javob
    """
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    choice = query.data  # "comment_yes" yoki "comment_no"
    
    print(f"🚕 DEBUG: driver_comment_choice_callback: choice={choice}")
    
    # ✅ O'ZGARTIRILDI: comment_yes/comment_no tekshiriladi
    if choice == "comment_yes":
        print(f"🚕 DEBUG: comment_yes selected")
        # Qo'shimcha ma'lumot yozishni so'rash
        order_manager.set_state(user_id, States.DRIVER_COMMENT)
        
        direction = order_manager.get_user_data(user_id, "direction")
        seats = order_manager.get_user_data(user_id, "seats")
        phone = order_manager.get_user_data(user_id, "phone")
        
        # Formatalash
        formatted_phone = f"+{phone[:3]} {phone[3:5]} {phone[5:8]} {phone[8:10]} {phone[10:12]}"
        
        await query.edit_message_text(
            f"📍 Yo'nalish: {DIRECTIONS[direction]}\n"
            f"💺 Bo'sh joylar: {seats} kishi\n"
            f"📞 Telefon: {formatted_phone}\n\n"
            "✍️ Qo'shimcha ma'lumotni yozing:\n"
            "(Masalan: avtomobil modeli, qo'shimcha xizmatlar)"
        )
    
    # ✅ O'ZGARTIRILDI: comment_no tekshiriladi
    elif choice == "comment_no":
        print(f"🚕 DEBUG: comment_no selected")
        # Qo'shimcha ma'lumot yo'q - to'g'ridan-to'g'ri tasdiqlashga
        order_manager.set_user_data(user_id, "comment", "")
        order_manager.set_state(user_id, States.DRIVER_CONFIRM)
        
        direction = order_manager.get_user_data(user_id, "direction")
        seats = order_manager.get_user_data(user_id, "seats")
        phone = order_manager.get_user_data(user_id, "phone")
        
        # Formatalash
        formatted_phone = f"+{phone[:3]} {phone[3:5]} {phone[5:8]} {phone[8:10]} {phone[10:12]}"
        
        text = "📋 E'LON TASDIQLANSINMI?\n\n"
        text += f"📍 Yo'nalish: {DIRECTIONS[direction]}\n"
        text += f"💺 Bo'sh joylar: {seats} kishi\n"
        text += f"📞 Telefon: {formatted_phone}\n"
        
        await query.edit_message_text(
            text,
            reply_markup=get_confirm_keyboard()
        )

async def driver_comment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Qo'shimcha ma'lumot yuborilgandan keyin
    Tasdiqlash ko'rsatish
    """
    user_id = update.effective_user.id
    
    # Tekshirish: Faqat DRIVER_COMMENT state dagi foydalanuvchilar uchun
    current_state = order_manager.get_state(user_id)
    if current_state != States.DRIVER_COMMENT:
        print(f"🚕 DEBUG: driver_comment_handler: Wrong state {current_state}")
        return
    
    comment = update.message.text.strip()
    
    # Kommentni saqlash
    order_manager.set_user_data(user_id, "comment", comment)
    order_manager.set_state(user_id, States.DRIVER_CONFIRM)
    
    direction = order_manager.get_user_data(user_id, "direction")
    seats = order_manager.get_user_data(user_id, "seats")
    phone = order_manager.get_user_data(user_id, "phone")
    
    # Formatalash
    formatted_phone = f"+{phone[:3]} {phone[3:5]} {phone[5:8]} {phone[8:10]} {phone[10:12]}"
    
    text = "📋 E'LON TASDIQLANSINMI?\n\n"
    text += f"📍 Yo'nalish: {DIRECTIONS[direction]}\n"
    text += f"💺 Bo'sh joylar: {seats} kishi\n"
    text += f"📞 Telefon: {formatted_phone}\n"
    if comment:
        text += f"💬 Izoh: {comment}\n"
    
    await context.bot.send_message(
        chat_id=user_id,
        text=text,
        reply_markup=get_confirm_keyboard()
    )

async def driver_confirm_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Tasdiqlash yoki bekor qilish
    """
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user = query.from_user
    choice = query.data  # "confirm_yes" yoki "confirm_no"
    
    if choice == "confirm_yes":
        # E'lonni qabul qilish
        direction = order_manager.get_user_data(user_id, "direction")
        seats = order_manager.get_user_data(user_id, "seats")
        phone = order_manager.get_user_data(user_id, "phone")
        comment = order_manager.get_user_data(user_id, "comment") or ""
        
        # Guruhga xabar yuborish
        now = datetime.now()
        time_str = now.strftime("%d.%m.%Y %H:%M")
        
        username = f"@{user.username}" if user.username else f"{user.first_name}"
        
        group_text = "🚕 YANGI E'LON - TAKSICHI\n\n"
        group_text += f"📍 Yo'nalish: {DIRECTIONS[direction]}\n"
        group_text += f"💺 Bo'sh joylar: {seats} kishi\n"
        group_text += f"📞 Telefon: {phone}\n"
        group_text += f"👤 Haydovchi: {username}\n"
        if comment:
            group_text += f"💬 Izoh: {comment}\n"
        group_text += f"⏰ Vaqt: {time_str}"
        
        # Guruhga yuborish (band qilish tugmasi YO'Q!)
        try:
            await context.bot.send_message(
                chat_id=MAIN_GROUP_ID,
                text=group_text
            )
            
            # Foydalanuvchiga xabar
            await query.edit_message_text(
                "✅ E'lon qabul qilindi!\n\n"
                "Guruhga yuborildi. Tez orada siz bilan bog'lanishadi.",
                reply_markup=get_main_menu_keyboard()
            )
            
        except Exception as e:
            print(f"❌ Error sending to group: {e}")
            await query.edit_message_text(
                "❌ Guruhga yuborishda xatolik. Iltimos, qayta urinib ko'ring.",
                reply_markup=get_main_menu_keyboard()
            )
        
        # Ma'lumotlarni tozalash
        order_manager.clear_user_data(user_id)
    else:
        # Bekor qilish
        await query.edit_message_text(
            "❌ E'lon bekor qilindi.",
            reply_markup=get_main_menu_keyboard()
        )
        order_manager.clear_user_data(user_id)