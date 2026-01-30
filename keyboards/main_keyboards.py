# keyboards/main_keyboards.py
"""
Bot klaviaturalari moduli
Bu yerda barcha InlineKeyboard va ReplyKeyboard lari yaratiladi
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import REQUIRED_CHANNELS, DIRECTIONS, PACKAGE_TYPES

def get_channel_subscription_keyboard() -> InlineKeyboardMarkup:
    """
    Kanal obuna klaviaturasi
    3 ta kanal havolasi + "Obunani tekshirish" tugmasi
    """
    buttons = []
    
    # Har bir kanal uchun tugma
    for i, channel in enumerate(REQUIRED_CHANNELS, 1):
        buttons.append([InlineKeyboardButton(
            text=f"{i}-kanal",
            url=channel["link"]
        )])
    
    # Obunani tekshirish tugmasi
    buttons.append([InlineKeyboardButton(
        text="✔️ Obunani tekshirish",
        callback_data="check_subscription"
    )])
    
    return InlineKeyboardMarkup(buttons)

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Bosh menyu klaviaturasi
    4 ta asosiy funksiya
    """
    keyboard = [
        [InlineKeyboardButton("🚖 Yo'lovchi sifatida", callback_data="mode_passenger")],
        [InlineKeyboardButton("🚕 Taksichi sifatida", callback_data="mode_driver")],
        [InlineKeyboardButton("📦 Pochta jo'natish", callback_data="mode_package")],
        [InlineKeyboardButton("👨‍💼 Admin bilan bog'lanish", callback_data="contact_admin")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_direction_keyboard() -> InlineKeyboardMarkup:
    """
    Yo'nalish tanlash klaviaturasi
    2 ta yo'nalish
    """
    keyboard = [
        [InlineKeyboardButton("Beshariq → Toshkent", callback_data="dir_beshariq_toshkent")],
        [InlineKeyboardButton("Toshkent → Beshariq", callback_data="dir_toshkent_beshariq")],
        [InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_count_keyboard(max_count: int = 4) -> InlineKeyboardMarkup:
    """
    Odam soni yoki joy soni tanlash klaviaturasi
    1 dan max_count gacha tugmalar
    """
    buttons = []
    row = []
    for i in range(1, max_count + 1):
        row.append(InlineKeyboardButton(str(i), callback_data=f"count_{i}"))
        if len(row) == 4:  # Har qatorda 4 ta tugma
            buttons.append(row)
            row = []
    
    if row:  # Qolgan tugmalar
        buttons.append(row)
    
    buttons.append([InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel")])
    return InlineKeyboardMarkup(buttons)

def get_yes_no_keyboard() -> InlineKeyboardMarkup:
    """
    Ha/Yo'q klaviaturasi
    Qo'shimcha ma'lumot uchun
    """
    keyboard = [
        [
            InlineKeyboardButton("✅ Ha", callback_data="comment_yes"),
            InlineKeyboardButton("❌ Yo'q", callback_data="comment_no")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_confirm_keyboard() -> InlineKeyboardMarkup:
    """
    Tasdiqlash klaviaturasi
    Zakaz berish / Bekor qilish
    """
    keyboard = [
        [InlineKeyboardButton("✅ Tasdiqlash", callback_data="confirm_yes")],
        [InlineKeyboardButton("❌ Bekor qilish", callback_data="confirm_no")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_package_type_keyboard() -> InlineKeyboardMarkup:
    """
    Pochta turi tanlash klaviaturasi
    4 ta pochta turi
    """
    keyboard = [
        [InlineKeyboardButton("📄 Hujjat", callback_data="pkg_document")],
        [InlineKeyboardButton("📦 Paket", callback_data="pkg_package")],
        [InlineKeyboardButton("📱 Elektronika", callback_data="pkg_electronics")],
        [InlineKeyboardButton("📋 Boshqa", callback_data="pkg_other")],
        [InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_weight_keyboard() -> InlineKeyboardMarkup:
    """
    Og'irlik tanlash klaviaturasi
    1-30 kg gacha
    """
    buttons = []
    
    # 1-10 kg (bir qatorda 5 ta)
    row = []
    for i in range(1, 11):
        row.append(InlineKeyboardButton(f"{i} kg", callback_data=f"weight_{i}"))
        if len(row) == 5:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    
    # 11-20 kg
    row = []
    for i in range(11, 21):
        row.append(InlineKeyboardButton(f"{i} kg", callback_data=f"weight_{i}"))
        if len(row) == 5:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    
    # 21-30 kg
    row = []
    for i in range(21, 31):
        row.append(InlineKeyboardButton(f"{i} kg", callback_data=f"weight_{i}"))
        if len(row) == 5:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    
    buttons.append([InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel")])
    return InlineKeyboardMarkup(buttons)

def get_booking_keyboard(order_id: str) -> InlineKeyboardMarkup:
    """
    Band qilish tugmasi
    Faqat yo'lovchi va pochta e'lonlari uchun
    """
    keyboard = [
        [InlineKeyboardButton("🔒 Band qilish", callback_data=f"book_{order_id}")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_to_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Bosh menyuga qaytish tugmasi
    """
    keyboard = [
        [InlineKeyboardButton("🏠 Bosh menyu", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)