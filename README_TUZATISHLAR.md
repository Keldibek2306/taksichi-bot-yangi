# Bot Tuzatishlari

## O'zgarishlar

### 1. Bot Menyulari Faqat Shaxsiy Chatda Ishlaydi

Quyidagi funksiyalar **faqat shaxsiy chatda** ishlaydi va guruhda ishlamaydi:

- `/start` komandasi
- Barcha callback handlerlar (tugmalar)
- Telefon va komment kiritish
- Buyurtma tasdiqlash

#### O'zgartirilgan fayllar:

**handlers/channel_check.py:**
- `start_command()` - faqat shaxsiy chat
- `check_subscription_callback()` - faqat shaxsiy chat
- `main_menu_callback()` - faqat shaxsiy chat

**handlers/common_handlers.py:**
- `comment_choice_callback()` - faqat shaxsiy chat
- `confirm_callback()` - faqat shaxsiy chat

**main.py:**
- `cancel_callback()` - faqat shaxsiy chat
- `handle_text_message()` - faqat shaxsiy chat
- `handle_contact_message()` - faqat shaxsiy chat
- `universal_direction_callback()` - faqat shaxsiy chat
- `universal_count_callback()` - faqat shaxsiy chat
- `universal_comment_choice_callback_legacy()` - faqat shaxsiy chat
- `universal_confirm_callback_legacy()` - faqat shaxsiy chat

### 2. Guruh/Kanal Funksiyalari

Bot guruhda yoki kanalda **faqat quyidagi funksiyalarni** bajaradi:

#### A) Reklama Yuborish
Bot **admin bo'lgan** barcha guruh va kanallarga avtomatik reklama yuboradi:

- **MAIN_GROUP ga**: Har 30 soniyada (config.py da `MAIN_GROUP_AD_INTERVAL`)
- **Boshqa guruh/kanallarga**: Har 50 soniyada (config.py da `ALL_GROUPS_AD_INTERVAL`)

Reklama xabarlari:
- `AD_MESSAGE` - MAIN_GROUP uchun
- Dinamik xabar bot username bilan - boshqa guruhlar uchun

#### B) Avtomatik Javob
Bot guruhda kalit so'zlarni aniqlaydi va avtomatik javob beradi:

**Kalit so'zlar** (config.py):
```python
AUTO_REPLY_KEYWORDS = {
    "taksi": ["taksi", "taxi", "mashina", "haydovchi", "driver"],
    "yolovchi": ["yo'lovchi", "yolovchi", "passenger", "odam", "joy"],
    "umumiy": ["pochta", "paket", "yuborish", "jo'natish", "xizmat", "service"]
}
```

**Avtomatik javoblar** (config.py):
- `AUTO_REPLY_MESSAGES["taksi"]` - taksi so'zlariga javob
- `AUTO_REPLY_MESSAGES["yolovchi"]` - yo'lovchi so'zlariga javob
- `AUTO_REPLY_MESSAGES["umumiy"]` - pochta so'zlariga javob

#### C) Admin Guruhlarni Kuzatish
Bot quyidagi hollarda guruhni admin ro'yxatiga qo'shadi:

1. Bot guruhga qo'shilganida va admin qilinganda
2. Guruhda xabar yuborilganida (agar bot admin bo'lsa)

**handlers/auto_reply_handler.py:**
- `handle_bot_added_to_group()` - bot qo'shilganda
- `handle_group_message()` - guruh xabarlarini tekshirish
- `get_admin_chats()` - admin guruhlar ro'yxatini qaytarish

### 3. Ishga Tushirish

```bash
# Zarur kutubxonalarni o'rnatish
pip install -r requirements.txt

# .env faylini sozlash
# BOT_TOKEN, CHANNEL_1_ID, CHANNEL_2_ID, CHANNEL_3_ID, MAIN_GROUP_ID

# Botni ishga tushirish
python main.py
```

### 4. Xususiyatlar

✅ Bot menyulari faqat shaxsiy chatda ishlaydi
✅ Guruhda faqat reklama va avtomatik javob ishlaydi
✅ Bot admin bo'lgan barcha guruh/kanallarga reklama yuboriladi
✅ Kalit so'zlar aniqlanganda avtomatik javob beriladi
✅ Xabar filtrlariga ega - guruhda bot menyulari ishlamaydi

### 5. Muhim Eslatmalar

1. **Reklama intervallari** `config.py` dan sozlanadi:
   - `MAIN_GROUP_AD_INTERVAL` - MAIN_GROUP uchun (soniyalarda)
   - `ALL_GROUPS_AD_INTERVAL` - boshqa guruhlar uchun (soniyalarda)

2. **Avtomatik javoblar** `config.py` dan sozlanadi:
   - `AUTO_REPLY_KEYWORDS` - kalit so'zlar
   - `AUTO_REPLY_MESSAGES` - javob xabarlari

3. **Admin guruhlar**:
   - Bot faqat admin bo'lgan guruhlarga reklama va avtomatik javob beradi
   - Guruhdan chiqarilsa, ro'yxatdan olib tashlanadi

## Kod Tuzilmasi

```
fixed_bot/
├── main.py                  # Asosiy fayl - bot ishga tushirish
├── config.py                # Konfiguratsiya
├── requirements.txt         # Kutubxonalar
├── handlers/
│   ├── channel_check.py     # Kanal tekshirish (SHAXSIY CHAT)
│   ├── auto_reply_handler.py # Avtomatik javob (GURUH)
│   ├── common_handlers.py   # Umumiy handlerlar (SHAXSIY CHAT)
│   ├── passenger_handler.py # Yo'lovchi (SHAXSIY CHAT)
│   ├── driver_handler.py    # Taksichi (SHAXSIY CHAT)
│   ├── package_handler.py   # Pochta (SHAXSIY CHAT)
│   ├── admin_handler.py     # Admin bilan bog'lanish (SHAXSIY CHAT)
│   └── booking_handler.py   # Band qilish (SHAXSIY CHAT)
├── keyboards/
│   └── main_keyboards.py    # Tugmalar
└── utils/
    └── order_manager.py     # Buyurtmalarni boshqarish
```

## Ishlash Printsipi

### Shaxsiy Chat:
1. Foydalanuvchi `/start` bosadi
2. Kanal obunasi tekshiriladi
3. Menyu ko'rsatiladi
4. Foydalanuvchi yo'lovchi/taksichi/pochta rejimini tanlaydi
5. Ma'lumotlar kiritiladi
6. Buyurtma guruhga yuboriladi

### Guruh:
1. Bot admin qilinadi
2. Har N soniyada reklama yuboriladi
3. Kalit so'z topilsa avtomatik javob beriladi
4. Buyurtmalar band qilinishi mumkin

## Xatoliklarni Tuzatish

Agar bot ishlamasa:

1. `.env` faylini tekshiring
2. Bot tokenini tekshiring
3. Kanal/guruh ID larini tekshiring
4. Bot kanal/guruhda admin ekanligini tekshiring
5. Python versiyasi 3.8+ ekanligini tekshiring
