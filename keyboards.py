"""
Bot klaviaturalari
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNELS, DIRECTIONS, POSTAL_DIRECTIONS, POSTAL_TYPES, PASSENGER_COUNTS, WEIGHT_RANGE


def get_subscription_keyboard():
    """Obuna bo'lish klaviaturasi"""
    buttons = []
    
    # Kanallar uchun tugmalar
    for i, channel in enumerate(CHANNELS, 1):
        buttons.append([InlineKeyboardButton(
            text=f"📢 {channel['name']}", 
            url=channel['link']
        )])
    
    # Tekshirish tugmasi
    buttons.append([InlineKeyboardButton(
        text="✅ Obunani tekshirish", 
        callback_data="check_subscription"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_main_menu():
    """Asosiy menyu"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚗 Yo'lovchi sifatida", callback_data="passenger")],
        [InlineKeyboardButton(text="🚕 Taksichi sifatida", callback_data="driver")],
        [InlineKeyboardButton(text="📦 Po'chta jo'natish", callback_data="postal")],
        [InlineKeyboardButton(text="ℹ️ Admin bilan bog'lanish", callback_data="admin_contact")]
    ])


def get_direction_keyboard(mode='taxi'):
    """Yo'nalish tanlash klaviaturasi"""
    if mode == 'postal':
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=POSTAL_DIRECTIONS['beshariq_toshkent'], callback_data="dir_beshariq_toshkent")],
            [InlineKeyboardButton(text=POSTAL_DIRECTIONS['toshkent_beshariq'], callback_data="dir_toshkent_beshariq")],
            [InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_main")]
        ])
    else:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=DIRECTIONS['beshariq_toshkent'], callback_data="dir_beshariq_toshkent")],
            [InlineKeyboardButton(text=DIRECTIONS['toshkent_beshariq'], callback_data="dir_toshkent_beshariq")],
            [InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_main")]
        ])


def get_passenger_count_keyboard():
    """Odamlar soni klaviaturasi"""
    buttons = []
    row = []
    for count in PASSENGER_COUNTS:
        row.append(InlineKeyboardButton(text=f"{count} kishi", callback_data=f"count_{count}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    
    buttons.append([InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_direction")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_postal_type_keyboard():
    """Po'chta turi klaviaturasi"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=POSTAL_TYPES['document'], callback_data="postal_type_document")],
        [InlineKeyboardButton(text=POSTAL_TYPES['package'], callback_data="postal_type_package")],
        [InlineKeyboardButton(text=POSTAL_TYPES['electronics'], callback_data="postal_type_electronics")],
        [InlineKeyboardButton(text=POSTAL_TYPES['other'], callback_data="postal_type_other")],
        [InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_postal_direction")]
    ])


def get_weight_keyboard():
    """Og'irlik tanlash klaviaturasi (1-30 kg)"""
    buttons = []
    row = []
    
    # 1-10 kg
    for weight in range(1, 11):
        row.append(InlineKeyboardButton(text=f"{weight} kg", callback_data=f"weight_{weight}"))
        if len(row) == 5:
            buttons.append(row)
            row = []
    
    # 11-20 kg
    for weight in range(11, 21):
        row.append(InlineKeyboardButton(text=f"{weight} kg", callback_data=f"weight_{weight}"))
        if len(row) == 5:
            buttons.append(row)
            row = []
    
    # 21-30 kg
    for weight in range(21, 31):
        row.append(InlineKeyboardButton(text=f"{weight} kg", callback_data=f"weight_{weight}"))
        if len(row) == 5:
            buttons.append(row)
            row = []
    
    if row:
        buttons.append(row)
    
    buttons.append([InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_postal_type")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_comment_keyboard():
    """Izoh qo'shish klaviaturasi"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Ha", callback_data="comment_yes")],
        [InlineKeyboardButton(text="❌ Yo'q", callback_data="comment_no")]
    ])


def get_confirm_keyboard():
    """Tasdiqlash klaviaturasi"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Zakaz berish", callback_data="confirm_order")],
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_order")]
    ])


def get_admin_contact_keyboard():
    """Admin bilan bog'lanish klaviaturasi"""
    from config import ADMIN_USERNAME, DEVELOPER_USERNAME
    
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"👤 Admin: {ADMIN_USERNAME}", url=f"https://t.me/{ADMIN_USERNAME.replace('@', '')}")],
        [InlineKeyboardButton(text=f"💻 Dasturchi: {DEVELOPER_USERNAME}", url=f"https://t.me/{DEVELOPER_USERNAME.replace('@', '')}")],
        [InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_main")]
    ])


def get_booking_keyboard(message_id, creator_id):
    """Guruhda e'lon uchun band qilish tugmasi"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔒 Band qilish", callback_data=f"book_{message_id}_{creator_id}")]
    ])
