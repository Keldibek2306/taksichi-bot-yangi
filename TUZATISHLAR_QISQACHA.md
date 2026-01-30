# BOT TO'G'IRLANDI! ✅

## 🎯 Asosiy O'zgarishlar

### 1. BOT MENYULARI FAQAT SHAXSIY CHATDA ISHLAYDI

**❌ GURUHDA ISHLAMAYDI:**
- /start komandasi
- Barcha tugmalar (callback query)
- Yo'lovchi/Taksichi/Pochta buyurtma berish
- Telefon va komment kiritish
- Admin bilan bog'lanish

**✅ FAQAT SHAXSIY CHATDA ISHLAYDI:**
Bot menyularidan foydalanish uchun foydalanuvchi botga **shaxsiy chatda** murojaat qilishi kerak.

---

### 2. GURUH/KANALDA FAQAT BU FUNKSIYALAR ISHLAYDI

#### 📢 A) REKLAMA FUNKSIYASI

Bot **admin bo'lgan** barcha guruh va kanallarga avtomatik reklama yuboradi:

**Reklama intervallari:**
- **MAIN_GROUP** (asosiy guruh): Har **30 soniyada**
- **Boshqa guruh/kanallar**: Har **50 soniyada**

**Sozlash:**
`config.py` faylida:
```python
MAIN_GROUP_AD_INTERVAL = 30   # 30 soniya
ALL_GROUPS_AD_INTERVAL = 50   # 50 soniya
```

**Reklama xabari:**
```
🚖 TAKSI VA YO'LOVCHI TOPISH!

Beshariq ↔️ Toshkent yo'nalishida:
✅ Tez taksi chaqiring
✅ Yo'lovchilarni toping
✅ Pochta jo'nating

🤖 @botusername ga /start bosing!
```

#### 🤖 B) AVTOMATIK JAVOB FUNKSIYASI

Bot guruhda **kalit so'zlarni** aniqlaydi va avtomatik javob beradi.

**Kalit so'zlar:**
1. **Taksi:** taksi, taxi, mashina, haydovchi, driver
2. **Yo'lovchi:** yo'lovchi, yolovchi, passenger, odam, joy  
3. **Pochta:** pochta, paket, yuborish, jo'natish, xizmat, service

Misol:
```
Foydalanuvchi: "taksi kerak"
Bot: 🚖 TEZ VA OSON TAKSI TOPISH UCHUN!
     Bizning bot orqali:
     ✅ Tez taksi chaqiring
     ...
```

#### 📋 C) BUYURTMALARNI BAND QILISH

Guruhda e'lon qilingan buyurtmalarni foydalanuvchilar **BAND QILISH** tugmasini bosib band qilishlari mumkin.

**Shartlar:**
- Foydalanuvchi botga /start bosgan bo'lishi kerak
- O'z buyurtmasini band qila olmaydi
- Allaqachon band qilingan buyurtmani band qila olmaydi

---

## 📁 O'ZGARTIRILGAN FAYLLAR

### Shaxsiy Chat Filtrlari Qo'shilgan:

1. **handlers/channel_check.py**
   - `start_command()` - /start faqat shaxsiy chatda
   - `check_subscription_callback()` - obuna tekshirish faqat shaxsiy chatda
   - `main_menu_callback()` - bosh menyu faqat shaxsiy chatda

2. **handlers/common_handlers.py**
   - `comment_choice_callback()` - komment tanlash faqat shaxsiy chatda
   - `confirm_callback()` - tasdiqlash faqat shaxsiy chatda

3. **handlers/passenger_handler.py**
   - `passenger_mode_start()` - yo'lovchi rejimi faqat shaxsiy chatda

4. **handlers/driver_handler.py**
   - `driver_mode_start()` - taksichi rejimi faqat shaxsiy chatda

5. **handlers/package_handler.py**
   - `package_mode_start()` - pochta rejimi faqat shaxsiy chatda

6. **handlers/admin_handler.py**
   - `contact_admin_callback()` - admin bilan bog'lanish faqat shaxsiy chatda

7. **main.py**
   - `cancel_callback()` - bekor qilish faqat shaxsiy chatda
   - `handle_text_message()` - matn xabarlar faqat shaxsiy chatda
   - `handle_contact_message()` - kontakt xabarlar faqat shaxsiy chatda
   - `universal_direction_callback()` - yo'nalish tanlash faqat shaxsiy chatda
   - `universal_count_callback()` - son tanlash faqat shaxsiy chatda
   - `universal_comment_choice_callback_legacy()` - eski komment tanlash faqat shaxsiy chatda
   - `universal_confirm_callback_legacy()` - eski tasdiqlash faqat shaxsiy chatda

### Guruh Funksiyalari:

8. **handlers/auto_reply_handler.py** (o'zgartirilmagan)
   - Guruhda avtomatik javob berish
   - Admin guruhlarni kuzatish
   - Bot qo'shilganda xabar yuborish

9. **handlers/booking_handler.py** (o'zgartirilmagan)
   - Guruhda buyurtmalarni band qilish
   - Shaxsiy chatda ham ishlaydi

10. **main.py** - Reklama funksiyalari
    - `send_advertisement_to_main_group()` - MAIN_GROUP ga reklama
    - `send_advertisement_to_all_groups()` - barcha admin guruhlarga reklama
    - `setup_advertisement_jobs()` - reklama job larni sozlash

---

## 🚀 ISHGA TUSHIRISH

### 1. Kerakli kutubxonalarni o'rnatish:
```bash
pip install -r requirements.txt
```

### 2. .env faylini sozlash:
```bash
BOT_TOKEN=your_bot_token_here
CHANNEL_1_ID=-1001234567890
CHANNEL_1_LINK=https://t.me/channel1
CHANNEL_2_ID=-1001234567891
CHANNEL_2_LINK=https://t.me/channel2
CHANNEL_3_ID=-1001234567892
CHANNEL_3_LINK=https://t.me/channel3
MAIN_GROUP_ID=-1001234567893
```

### 3. Botni ishga tushirish:
```bash
python main.py
```

---

## ⚙️ SOZLAMALAR

### Reklama Vaqtini O'zgartirish:
`config.py` da:
```python
MAIN_GROUP_AD_INTERVAL = 30   # 30 soniya (istalgan vaqtga o'zgartiring)
ALL_GROUPS_AD_INTERVAL = 50   # 50 soniya (istalgan vaqtga o'zgartiring)
```

### Reklama Xabarini O'zgartirish:
`config.py` da:
```python
AD_MESSAGE = """Sizning reklama xabaringiz"""
```

### Avtomatik Javob Xabarlarini O'zgartirish:
`config.py` da:
```python
AUTO_REPLY_MESSAGES = {
    "taksi": "Sizning taksi javobingiz",
    "yolovchi": "Sizning yo'lovchi javobingiz",
    "umumiy": "Sizning umumiy javobingiz"
}
```

### Kalit So'zlarni O'zgartirish:
`config.py` da:
```python
AUTO_REPLY_KEYWORDS = {
    "taksi": ["taksi", "taxi", "mashina"],
    "yolovchi": ["yo'lovchi", "yolovchi"],
    "umumiy": ["pochta", "paket"]
}
```

---

## ✅ TEST QILISH

### Shaxsiy Chatda:
1. Botga `/start` yuboring
2. Kanallarga obuna bo'ling
3. Yo'lovchi/Taksichi/Pochta rejimlarini sinab ko'ring

### Guruhda:
1. Botni guruhga qo'shing
2. Botni admin qiling
3. "taksi" yoki "yo'lovchi" so'zlarini yozing
4. Bot avtomatik javob berishini kuzating
5. Reklama yuborishini kuting

---

## 📌 MUHIM ESLATMALAR

1. **Bot admin bo'lishi kerak:** Guruhda reklama va avtomatik javob ishlashi uchun bot admin bo'lishi shart.

2. **Reklama intervallari:** Agar guruh ko'p bo'lsa, reklama intervallari ko'proq qiling (spam deb hisoblanmasligi uchun).

3. **Kalit so'zlar:** Avtomatik javob berish uchun kalit so'zlarni to'g'ri sozlang.

4. **Shaxsiy chat:** Barcha buyurtma berish jarayoni faqat shaxsiy chatda amalga oshiriladi.

5. **Guruh filtrlari:** Guruhda faqat reklama, avtomatik javob va band qilish ishlaydi. Boshqa hech narsa ishlamaydi.

---

## 🐛 XATOLIKLARNI TUZATISH

Agar bot ishlamasa:

1. **Bot tokeni to'g'rimi?** `.env` faylini tekshiring
2. **Bot admin qilinganmi?** Guruhda botni admin qiling
3. **Kanal ID lari to'g'rimi?** ID lar `-100` bilan boshlanishi kerak
4. **Python versiyasi?** Python 3.8+ ishlatilishi kerak
5. **Kutubxonalar o'rnatilganmi?** `pip install -r requirements.txt` bajaring

---

## 📞 YORDAM

Agar muammo yuzaga kelsa, quyidagi narsalarni tekshiring:

1. Log fayllarni ko'ring (terminal output)
2. Bot admin huquqlariga ega ekanligini tekshiring
3. Kanal va guruh ID larini to'g'ri kiritganingizni tekshiring
4. Bot tokenini to'g'ri nusxalaganingizni tekshiring

---

**Bot muvaffaqiyatli to'g'irlandi va tayyor!** 🎉
