"""
Pochta jo'natish rejimi handler moduli
Pochta jo'natish uchun buyurtma berish jarayoni
"""
import re
from telegram import (
    Update, 
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import ContextTypes
from datetime import datetime

from config import States, DIRECTIONS, PACKAGE_TYPES, MAIN_GROUP_ID
from keyboards.main_keyboards import (
    get_direction_keyboard,
    get_package_type_keyboard,
    get_weight_keyboard,
    get_yes_no_keyboard,
    get_confirm_keyboard,
    get_main_menu_keyboard,
    get_booking_keyboard
)
from utils.order_manager import order_manager

async def package_mode_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Pochta rejimini boshlash
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
    order_manager.set_state(user_id, States.PACKAGE_DIRECTION)
    order_manager.set_user_data(user_id, "mode", "package")
    
    await query.edit_message_text(
        "📦 POCHTA JO'NATISH\n\n"
        "📍 Pochta qaysi manzilga jo'natmoqchisiz?",
        reply_markup=get_direction_keyboard()
    )

async def package_direction_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Yo'nalish tanlagandan keyin
    Pochta turini so'rash
    """
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    direction = query.data.replace("dir_", "")
    
    # Ma'lumotni saqlash
    order_manager.set_user_data(user_id, "direction", direction)
    order_manager.set_state(user_id, States.PACKAGE_TYPE)
    
    await query.edit_message_text(
        f"📍 Yo'nalish: {DIRECTIONS[direction]}\n\n"
        "📋 Pochta turini tanlang:",
        reply_markup=get_package_type_keyboard()
    )

async def package_type_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Pochta turi tanlagandan keyin
    Og'irlikni so'rash
    """
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    pkg_type = query.data.replace("pkg_", "")
    
    # Ma'lumotni saqlash
    order_manager.set_user_data(user_id, "package_type", pkg_type)
    order_manager.set_state(user_id, States.PACKAGE_WEIGHT)
    
    direction = order_manager.get_user_data(user_id, "direction")
    
    await query.edit_message_text(
        f"📍 Yo'nalish: {DIRECTIONS[direction]}\n"
        f"📋 Pochta turi: {PACKAGE_TYPES[pkg_type]}\n\n"
        "⚖️ Og'irligini tanlang:",
        reply_markup=get_weight_keyboard()
    )

async def package_weight_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Og'irlik tanlagandan keyin telefon raqam so'rash
    """
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    weight = int(query.data.replace("weight_", ""))
    
    # Ma'lumotni saqlash
    order_manager.set_user_data(user_id, "weight", weight)
    order_manager.set_state(user_id, States.PACKAGE_PHONE)
    
    direction = order_manager.get_user_data(user_id, "direction")
    pkg_type = order_manager.get_user_data(user_id, "package_type")
    
    # Avval inline xabarni yangilash
    await query.edit_message_text(
        f"📍 Yo'nalish: {DIRECTIONS[direction]}\n"
        f"📋 Pochta turi: {PACKAGE_TYPES[pkg_type]}\n"
        f"⚖️ Og'irligi: {weight} kg\n\n"
        "📞 Telefon raqamingizni quyidagi tugma orqali yuboring..."
    )
    
    # REPLY KEYBOARD bilan YANGI xabar yuborish
    phone_keyboard = ReplyKeyboardMarkup(
        [
            [KeyboardButton("📞 Telefon raqamimni jo'natish", request_contact=True)],
            ["📝 Raqamni yozib yuborish"]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    await context.bot.send_message(
        chat_id=user_id,
        text="📱 Telefon raqamingizni yuboring:\n\n"
             "• 📞 Tugma orqali jo'natish - OSON USUL\n"
             "• 📝 Raqamni yozib yuborish\n\n"
             "📝 Formatlar:\n"
             "✅ +998 90 123 45 67\n"
             "✅ 998901234567\n"
             "✅ 901234567",
        reply_markup=phone_keyboard
    )

async def package_phone_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Telefon raqam yuborilgandan keyin (contact yoki text)
    """
    user_id = update.effective_user.id
    
    print(f"📞 DEBUG: package_phone_handler chaqirildi. User: {user_id}")
    
    # Tekshirish: Faqat PACKAGE_PHONE state dagi foydalanuvchilar uchun
    current_state = order_manager.get_state(user_id)
    print(f"📞 DEBUG: Current state: {current_state}, Expected: {States.PACKAGE_PHONE}")
    
    if current_state != States.PACKAGE_PHONE:
        print(f"📞 DEBUG: Wrong state, ignoring")
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
        print(f"📞 DEBUG: Contact phone received: {phone}")
        
    # 2. Agar text yuborilgan bo'lsa
    elif update.message.text:
        text = update.message.text.strip()
        print(f"📞 DEBUG: Text received: {text}")
        
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
        print(f"📞 DEBUG: Cleaned phone: {cleaned}")
        
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
        print(f"📞 DEBUG: Neither contact nor text")
        return
    
    if phone:
        print(f"📞 DEBUG: Phone to save: {phone}")
        
        # Telefon raqamni saqlash
        order_manager.set_user_data(user_id, "phone", phone)
        order_manager.set_state(user_id, States.PACKAGE_COMMENT_CHOICE)
        
        # Keyboardni olib tashlash
        await update.message.reply_text(
            "✅ Telefon raqamingiz qabul qilindi!",
            reply_markup=ReplyKeyboardRemove()
        )
        
        direction = order_manager.get_user_data(user_id, "direction")
        pkg_type = order_manager.get_user_data(user_id, "package_type")
        weight = order_manager.get_user_data(user_id, "weight")
        
        # Formatalash
        formatted_phone = f"+{phone[:3]} {phone[3:5]} {phone[5:8]} {phone[8:10]} {phone[10:12]}"
        
        # ✅ O'ZGARTIRILDI: get_yes_no_keyboard() ishlatamiz (comment_yes/comment_no)
        await context.bot.send_message(
            chat_id=user_id,
            text=f"📍 Yo'nalish: {DIRECTIONS[direction]}\n"
                 f"📋 Pochta turi: {PACKAGE_TYPES[pkg_type]}\n"
                 f"⚖️ Og'irligi: {weight} kg\n"
                 f"📞 Telefon: {formatted_phone}\n\n"
                 "💬 Qo'shimcha ma'lumot yozasizmi?",
            reply_markup=get_yes_no_keyboard()  # ✅ get_yes_no_keyboard() ishlatildi
        )
        print(f"📞 DEBUG: Sent yes/no question")

async def package_comment_choice_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Qo'shimcha ma'lumot kerakmi degan savolga javob
    """
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    choice = query.data  # "comment_yes" yoki "comment_no"
    
    print(f"📝 DEBUG: Comment choice callback: {choice}")
    
    # ✅ O'ZGARTIRILDI: comment_yes/comment_no tekshiriladi
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
    
    # ✅ O'ZGARTIRILDI: comment_no tekshiriladi
    elif choice == "comment_no":
        # Qo'shimcha ma'lumot yo'q - to'g'ridan-to'g'ri tasdiqlashga
        order_manager.set_user_data(user_id, "comment", "")
        order_manager.set_state(user_id, States.PACKAGE_CONFIRM)
        
        direction = order_manager.get_user_data(user_id, "direction")
        pkg_type = order_manager.get_user_data(user_id, "package_type")
        weight = order_manager.get_user_data(user_id, "weight")
        phone = order_manager.get_user_data(user_id, "phone")
        
        # Formatalash
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

async def package_comment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Qo'shimcha ma'lumot yuborilgandan keyin
    Tasdiqlash ko'rsatish
    """
    user_id = update.effective_user.id
    
    # Tekshirish: Faqat PACKAGE_COMMENT state dagi foydalanuvchilar uchun
    current_state = order_manager.get_state(user_id)
    if current_state != States.PACKAGE_COMMENT:
        print(f"📝 DEBUG: package_comment_handler: Wrong state {current_state}")
        return
    
    comment = update.message.text.strip()
    
    # Kommentni saqlash
    order_manager.set_user_data(user_id, "comment", comment)
    order_manager.set_state(user_id, States.PACKAGE_CONFIRM)
    
    direction = order_manager.get_user_data(user_id, "direction")
    pkg_type = order_manager.get_user_data(user_id, "package_type")
    weight = order_manager.get_user_data(user_id, "weight")
    phone = order_manager.get_user_data(user_id, "phone")
    
    # Formatalash
    formatted_phone = f"+{phone[:3]} {phone[3:5]} {phone[5:8]} {phone[8:10]} {phone[10:12]}"
    
    text = "📋 BUYURTMA TASDIQLANSINMI?\n\n"
    text += f"📍 Yo'nalish: {DIRECTIONS[direction]}\n"
    text += f"📋 Pochta turi: {PACKAGE_TYPES[pkg_type]}\n"
    text += f"⚖️ Og'irligi: {weight} kg\n"
    text += f"📞 Telefon: {formatted_phone}\n"
    if comment:
        text += f"💬 Izoh: {comment}\n"
    
    await context.bot.send_message(
        chat_id=user_id,
        text=text,
        reply_markup=get_confirm_keyboard()
    )

async def package_confirm_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Tasdiqlash yoki bekor qilish
    """
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user = query.from_user
    choice = query.data  # "confirm_yes" yoki "confirm_no"
    
    if choice == "confirm_yes":
        # Buyurtmani qabul qilish
        direction = order_manager.get_user_data(user_id, "direction")
        pkg_type = order_manager.get_user_data(user_id, "package_type")
        weight = order_manager.get_user_data(user_id, "weight")
        phone = order_manager.get_user_data(user_id, "phone")
        comment = order_manager.get_user_data(user_id, "comment") or ""
        
        # Guruhga xabar yuborish
        now = datetime.now()
        time_str = now.strftime("%d.%m.%Y %H:%M")
        
        username = f"@{user.username}" if user.username else f"{user.first_name}"
        
        group_text = "📦 YANGI BUYURTMA - POCHTA\n\n"
        group_text += f"📍 Yo'nalish: {DIRECTIONS[direction]}\n"
        group_text += f"📋 Pochta turi: {PACKAGE_TYPES[pkg_type]}\n"
        group_text += f"⚖️ Og'irligi: {weight} kg\n"
        group_text += f"📞 Telefon: {phone}\n"
        group_text += f"👤 Foydalanuvchi: {username}\n"
        if comment:
            group_text += f"💬 Izoh: {comment}\n"
        group_text += f"⏰ Vaqt: {time_str}"
        
        # Guruhga yuborish
        try:
            group_message = await context.bot.send_message(
                chat_id=MAIN_GROUP_ID,
                text=group_text
            )
            
            # Keyin band qilish tugmasini qo'shamiz
            await context.bot.edit_message_reply_markup(
                chat_id=MAIN_GROUP_ID,
                message_id=group_message.message_id,
                reply_markup=get_booking_keyboard(str(group_message.message_id))
            )
            
            # Buyurtmani saqlash
            order_manager.add_order(group_message.message_id, {
                "type": "package",
                "user_id": user_id,
                "username": username,
                "direction": direction,
                "package_type": pkg_type,
                "weight": weight,
                "phone": phone,
                "comment": comment
            })
            
            # Foydalanuvchiga xabar
            await query.edit_message_text(
                "✅ Buyurtma qabul qilindi!\n\n"
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
            "❌ Buyurtma bekor qilindi.",
            reply_markup=get_main_menu_keyboard()
        )
        order_manager.clear_user_data(user_id)