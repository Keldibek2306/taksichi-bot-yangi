"""
Bot handlerlari
"""
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import (
    get_subscription_keyboard, get_main_menu, get_direction_keyboard,
    get_passenger_count_keyboard, get_comment_keyboard, get_confirm_keyboard,
    get_admin_contact_keyboard, get_postal_type_keyboard, get_weight_keyboard,
    get_booking_keyboard
)
from utils import (
    check_user_subscription, get_not_subscribed_message,
    create_passenger_announcement, create_driver_announcement,
    create_postal_announcement
)
from config import MAIN_GROUP_ID, ADMIN_USERNAME, ADMIN_PHONE, DEVELOPER_USERNAME, DEVELOPER_PHONE

router = Router()


# FSM States
class PassengerState(StatesGroup):
    waiting_for_phone = State()
    waiting_for_comment = State()


class DriverState(StatesGroup):
    waiting_for_phone = State()
    waiting_for_comment = State()


class PostalState(StatesGroup):
    waiting_for_phone = State()
    waiting_for_comment = State()


# Foydalanuvchilar ma'lumotlarini vaqtinchalik saqlash (RAM)
user_data_storage = {}
# E'lon yaratuvchilarini saqlash
announcement_creators = {}


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Start komandasi"""
    await state.clear()
    user_id = message.from_user.id
    
    # Obunani tekshirish
    is_subscribed, not_subscribed = await check_user_subscription(message.bot, user_id)
    
    # Start xabarini o'chirish
    await message.delete()
    
    if not is_subscribed:
        # Obuna bo'lmagan
        msg_text = get_not_subscribed_message(not_subscribed)
        sent_msg = await message.answer(
            msg_text,
            reply_markup=get_subscription_keyboard()
        )
    else:
        # Obuna bo'lgan - asosiy menyu
        sent_msg = await message.answer(
            "🏠 <b>Asosiy menyu</b>\n\nKerakli bo'limni tanlang:",
            reply_markup=get_main_menu()
        )


@router.callback_query(F.data == "check_subscription")
async def check_subscription_callback(callback: CallbackQuery):
    """Obunani tekshirish"""
    user_id = callback.from_user.id
    is_subscribed, not_subscribed = await check_user_subscription(callback.bot, user_id)
    
    if not is_subscribed:
        msg_text = get_not_subscribed_message(not_subscribed)
        await callback.answer("❌ Siz hali barcha kanallarga obuna bo'lmagansiz!", show_alert=True)
        await callback.message.edit_text(
            msg_text,
            reply_markup=get_subscription_keyboard()
        )
    else:
        await callback.answer("✅ Obuna tasdiqlandi!", show_alert=True)
        await callback.message.edit_text(
            "🏠 <b>Asosiy menyu</b>\n\nKerakli bo'limni tanlang:",
            reply_markup=get_main_menu()
        )


@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    """Asosiy menyuga qaytish"""
    await state.clear()
    user_id = callback.from_user.id
    if user_id in user_data_storage:
        del user_data_storage[user_id]
    
    await callback.message.edit_text(
        "🏠 <b>Asosiy menyu</b>\n\nKerakli bo'limni tanlang:",
        reply_markup=get_main_menu()
    )


@router.callback_query(F.data == "passenger")
async def passenger_handler(callback: CallbackQuery, state: FSMContext):
    """Yo'lovchi rejimi"""
    await state.clear()
    user_id = callback.from_user.id
    user_data_storage[user_id] = {'mode': 'passenger'}
    
    await callback.message.edit_text(
        "🚗 <b>Yo'lovchi sifatida</b>\n\nYo'nalishni tanlang:",
        reply_markup=get_direction_keyboard()
    )


@router.callback_query(F.data == "driver")
async def driver_handler(callback: CallbackQuery, state: FSMContext):
    """Haydovchi rejimi"""
    await state.clear()
    user_id = callback.from_user.id
    user_data_storage[user_id] = {'mode': 'driver'}
    
    await callback.message.edit_text(
        "🚕 <b>Taksichi sifatida</b>\n\nYo'nalishni tanlang:",
        reply_markup=get_direction_keyboard()
    )


@router.callback_query(F.data == "postal")
async def postal_handler(callback: CallbackQuery, state: FSMContext):
    """Po'chta rejimi"""
    await state.clear()
    user_id = callback.from_user.id
    user_data_storage[user_id] = {'mode': 'postal'}
    
    await callback.message.edit_text(
        "📦 <b>Po'chta jo'natish</b>\n\nQaysi manzilga jo'natmoqchisiz?",
        reply_markup=get_direction_keyboard(mode='postal')
    )


@router.callback_query(F.data.startswith("dir_"))
async def direction_handler(callback: CallbackQuery):
    """Yo'nalishni tanlash"""
    user_id = callback.from_user.id
    direction = callback.data.replace("dir_", "")
    
    if user_id not in user_data_storage:
        user_data_storage[user_id] = {}
    
    user_data_storage[user_id]['direction'] = direction
    mode = user_data_storage[user_id].get('mode', 'passenger')
    
    if mode == 'postal':
        # Po'chta uchun tur tanlash
        await callback.message.edit_text(
            "📦 <b>Po'chta turini tanlang:</b>",
            reply_markup=get_postal_type_keyboard()
        )
    else:
        # Yo'lovchi yoki haydovchi uchun odamlar soni
        text = "👥 Nechta odam uchun?" if mode == 'passenger' else "💺 Nechta bo'sh joy bor?"
        await callback.message.edit_text(
            text,
            reply_markup=get_passenger_count_keyboard()
        )


@router.callback_query(F.data.startswith("postal_type_"))
async def postal_type_handler(callback: CallbackQuery):
    """Po'chta turini tanlash"""
    user_id = callback.from_user.id
    postal_type = callback.data.replace("postal_type_", "")
    
    if user_id not in user_data_storage:
        await callback.answer("❌ Xatolik yuz berdi. Qaytadan boshlang.", show_alert=True)
        return
    
    user_data_storage[user_id]['postal_type'] = postal_type
    
    await callback.message.edit_text(
        "⚖️ <b>Og'irligini tanlang (kg):</b>",
        reply_markup=get_weight_keyboard()
    )


@router.callback_query(F.data.startswith("weight_"))
async def weight_handler(callback: CallbackQuery, state: FSMContext):
    """Og'irlikni tanlash"""
    user_id = callback.from_user.id
    weight = int(callback.data.replace("weight_", ""))
    
    if user_id not in user_data_storage:
        await callback.answer("❌ Xatolik yuz berdi. Qaytadan boshlang.", show_alert=True)
        return
    
    user_data_storage[user_id]['weight'] = weight
    
    # Telefon raqam so'rash
    await state.set_state(PostalState.waiting_for_phone)
    await callback.message.edit_text(
        "📱 <b>Bog'lanish uchun telefon raqamingizni jo'nating:</b>\n\n"
        "Misol: +998 90 123 45 67"
    )


@router.callback_query(F.data.startswith("count_"))
async def count_handler(callback: CallbackQuery, state: FSMContext):
    """Odamlar sonini tanlash"""
    user_id = callback.from_user.id
    count = int(callback.data.replace("count_", ""))
    
    if user_id not in user_data_storage:
        await callback.answer("❌ Xatolik yuz berdi. Qaytadan boshlang.", show_alert=True)
        return
    
    user_data_storage[user_id]['count'] = count
    mode = user_data_storage[user_id].get('mode', 'passenger')
    
    # Telefon raqam so'rash
    if mode == 'passenger':
        await state.set_state(PassengerState.waiting_for_phone)
    else:
        await state.set_state(DriverState.waiting_for_phone)
    
    await callback.message.edit_text(
        "📱 <b>Bog'lanish uchun telefon raqamingizni jo'nating:</b>\n\n"
        "Misol: +998 90 123 45 67"
    )


@router.message(PassengerState.waiting_for_phone)
@router.message(DriverState.waiting_for_phone)
@router.message(PostalState.waiting_for_phone)
async def phone_handler(message: Message, state: FSMContext):
    """Telefon raqamni qabul qilish"""
    user_id = message.from_user.id
    phone = message.text.strip()
    
    if user_id not in user_data_storage:
        await message.answer("❌ Xatolik yuz berdi. /start dan boshlang.")
        return
    
    user_data_storage[user_id]['phone'] = phone
    mode = user_data_storage[user_id].get('mode', 'passenger')
    
    # Oldingi xabarlarni o'chirish
    await message.delete()
    
    # Izoh so'rash
    if mode == 'postal':
        await state.set_state(PostalState.waiting_for_comment)
    elif mode == 'passenger':
        await state.set_state(PassengerState.waiting_for_comment)
    else:
        await state.set_state(DriverState.waiting_for_comment)
    
    sent_msg = await message.answer(
        "💬 <b>Qo'shimcha ma'lumot yozasizmi?</b>",
        reply_markup=get_comment_keyboard()
    )


@router.callback_query(F.data == "comment_yes")
async def comment_yes_handler(callback: CallbackQuery, state: FSMContext):
    """Izoh yozish - Ha"""
    await callback.message.edit_text(
        "✍️ <b>Qo'shimcha ma'lumotni yozing:</b>"
    )


@router.callback_query(F.data == "comment_no")
async def comment_no_handler(callback: CallbackQuery, state: FSMContext):
    """Izoh yozish - Yo'q"""
    user_id = callback.from_user.id
    
    if user_id in user_data_storage:
        user_data_storage[user_id]['comment'] = ''
    
    await state.clear()
    await callback.message.edit_text(
        "✅ <b>E'loningiz tayyor!</b>\n\n"
        "Tasdiqlaysizmi?",
        reply_markup=get_confirm_keyboard()
    )


@router.message(PassengerState.waiting_for_comment)
@router.message(DriverState.waiting_for_comment)
@router.message(PostalState.waiting_for_comment)
async def comment_handler(message: Message, state: FSMContext):
    """Izohni qabul qilish"""
    user_id = message.from_user.id
    comment = message.text.strip()
    
    if user_id not in user_data_storage:
        await message.answer("❌ Xatolik yuz berdi. /start dan boshlang.")
        return
    
    user_data_storage[user_id]['comment'] = comment
    
    # Oldingi xabarlarni o'chirish
    await message.delete()
    
    await state.clear()
    sent_msg = await message.answer(
        "✅ <b>E'loningiz tayyor!</b>\n\n"
        "Tasdiqlaysizmi?",
        reply_markup=get_confirm_keyboard()
    )


@router.callback_query(F.data == "confirm_order")
async def confirm_order_handler(callback: CallbackQuery):
    """Zakazni tasdiqlash"""
    user_id = callback.from_user.id
    
    if user_id not in user_data_storage:
        await callback.answer("❌ Xatolik yuz berdi.", show_alert=True)
        return
    
    user_data = user_data_storage[user_id]
    mode = user_data.get('mode', 'passenger')
    user_full_name = callback.from_user.full_name
    
    # E'lon matnini yaratish
    if mode == 'passenger':
        announcement = create_passenger_announcement(user_data, user_full_name)
        has_booking = True
    elif mode == 'driver':
        announcement = create_driver_announcement(user_data, user_full_name)
        has_booking = False
    else:  # postal
        announcement = create_postal_announcement(user_data, user_full_name)
        has_booking = True
    
    try:
        # Guruhga jo'natish
        sent_message = await callback.bot.send_message(
            chat_id=MAIN_GROUP_ID,
            text=announcement,
            reply_markup=get_booking_keyboard(0, user_id) if has_booking else None
        )
        
        # E'lon yaratuvchisini saqlash
        if has_booking:
            announcement_creators[sent_message.message_id] = user_id
        
        await callback.answer("✅ E'lon guruhga jo'natildi!", show_alert=True)
        await callback.message.edit_text(
            "✅ <b>Zakaz qabul qilindi!</b>\n\n"
            "E'loningiz guruhga joylashtirildi  @taxi_beshariq.",
            reply_markup=get_main_menu()
        )
    except Exception as e:
        await callback.answer(f"❌ Xatolik: {str(e)}", show_alert=True)
    
    # Ma'lumotlarni tozalash
    if user_id in user_data_storage:
        del user_data_storage[user_id]


@router.callback_query(F.data == "cancel_order")
async def cancel_order_handler(callback: CallbackQuery, state: FSMContext):
    """Zakazni bekor qilish"""
    user_id = callback.from_user.id
    
    await state.clear()
    if user_id in user_data_storage:
        del user_data_storage[user_id]
    
    await callback.answer("❌ Zakaz bekor qilindi", show_alert=True)
    await callback.message.edit_text(
        "🏠 <b>Asosiy menyu</b>\n\nKerakli bo'limni tanlang:",
        reply_markup=get_main_menu()
    )


@router.callback_query(F.data == "admin_contact")
async def admin_contact_handler(callback: CallbackQuery):
    """Admin bilan bog'lanish"""
    text = f"""
ℹ️ <b>Bog'lanish uchun ma'lumotlar:</b>

👤 Admin: {ADMIN_USERNAME}
📱 Telefon: {ADMIN_PHONE}

💻 Dasturchi: {DEVELOPER_USERNAME}
📱 Telefon: {DEVELOPER_PHONE}

📢 Buyurtmalar guruhi: @your_group_link
"""
    
    await callback.message.edit_text(
        text,
        reply_markup=get_admin_contact_keyboard()
    )


@router.callback_query(F.data.startswith("book_"))
async def book_announcement_handler(callback: CallbackQuery):
    """E'lonni band qilish"""
    user_id = callback.from_user.id
    
    # E'lon ma'lumotlarini olish
    parts = callback.data.split("_")
    message_id = int(parts[1])
    creator_id = int(parts[2])
    
    # O'zi yaratgan e'lonni band qila olmasligi
    if user_id == creator_id:
        await callback.answer("❌ Siz o'z e'loningizni band qila olmaysiz!", show_alert=True)
        return
    
    # Botga start bosganligini tekshirish (xotirada bormi)
    # Bu yerda soddalik uchun tekshirmasdan band qilishga ruxsat beramiz
    # Agar kerak bo'lsa, alohida ma'lumotlar bazasida saqlash mumkin
    
    user_name = callback.from_user.full_name
    username = f"@{callback.from_user.username}" if callback.from_user.username else "Foydalanuvchi"
    
    # E'lon matnini yangilash
    original_text = callback.message.text or callback.message.caption or ""
    new_text = f"{original_text}\n\n🔒 <b>Band qildi:</b> {user_name} ({username})"
    
    try:
        await callback.message.edit_text(
            text=new_text,
            reply_markup=None
        )
        await callback.answer("✅ E'lon band qilindi!", show_alert=True)
    except Exception as e:
        await callback.answer("❌ Xatolik yuz berdi!", show_alert=True)
