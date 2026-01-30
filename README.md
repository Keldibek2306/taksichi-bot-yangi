# Telegram Bot - Taksi va Pochta Xizmati

Beshariq-Toshkent yo'nalishida taksi va pochta xizmatini taqdim etuvchi professional Telegram bot.

## 📋 Xususiyatlar

### ✅ Asosiy Funksiyalar
- 🔐 Kanal obunasini tekshirish (3 ta majburiy kanal)
- 🚖 Yo'lovchi sifatida taksi chaqirish
- 🚕 Taksichi sifatida e'lon berish
- 📦 Pochta jo'natish xizmati
- 🔒 Buyurtmalarni band qilish tizimi
- 📢 Avtomatik reklama (MAIN_GROUP ga har 15 minutda)
- 🤖 **YANGI: Bot admin bo'lgan barcha guruh/kanallarga avtomatik javob**
- 📣 **YANGI: Barcha admin guruh/kanallarga har 5 minutda reklama**
- 👨‍💼 Admin bilan bog'lanish

### 🤖 Avtomatik Javob Tizimi
Bot admin bo'lgan guruh va kanallarda quyidagi kalit so'zlar yozilsa avtomatik javob beradi:

**Taksi kalit so'zlari:**
- taksi, taxi, mashina, haydovchi, driver

**Yo'lovchi kalit so'zlari:**
- yo'lovchi, yolovchi, passenger, odam, joy

**Umumiy kalit so'zlar:**
- pochta, paket, yuborish, jo'natish, xizmat, service

### 📣 Avtomatik Reklama
1. **MAIN_GROUP:** Har 15 minutda
2. **Barcha admin guruh/kanallar:** Har 5 minutda

### 🏗️ Texnik Xususiyatlar
- Python 3.10+
- python-telegram-bot kutubxonasi
- In-memory ma'lumotlar saqlash (RAM)
- Modul tuzilmali arxitektura
- Professional kod sifati

## 📁 Loyiha Tuzilmasi

```
telegram_bot/
├── main.py                      # Asosiy bot fayl
├── config.py                    # Sozlamalar va konstantalar
├── .env                         # Token va ID lar
├── requirements.txt             # Kerakli kutubxonalar
├── README.md                    # Dokumentatsiya
├── handlers/                    # Handler modullari
│   ├── __init__.py
│   ├── channel_check.py        # Kanal obunasi
│   ├── passenger_handler.py    # Yo'lovchi rejimi
│   ├── driver_handler.py       # Taksichi rejimi
│   ├── package_handler.py      # Pochta rejimi
│   ├── admin_handler.py        # Admin bilan bog'lanish
│   └── booking_handler.py      # Band qilish funksiyasi
├── keyboards/                   # Klaviatura modullari
│   ├── __init__.py
│   └── main_keyboards.py       # Barcha klaviaturalar
└── utils/                       # Yordamchi modullar
    ├── __init__.py
    └── order_manager.py         # In-memory ma'lumotlar boshqaruvi
```

## 🚀 O'rnatish

### 1. Talablar
- Python 3.10 yoki yuqori versiya
- pip package manager

### 2. Kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

### 3. Sozlamalar

`.env` faylida quyidagi sozlamalar mavjud:

```env
BOT_TOKEN=7492023343:AAH-pGS6QVlor3k5NqLFPGeyxBEmHyf7Nbw

CHANNEL_1_ID=-1002156254251
CHANNEL_1_LINK=https://t.me/uz_dasturlash_asosi

CHANNEL_2_ID=-1002156254251
CHANNEL_2_LINK=https://t.me/uz_dasturlash_asosi

CHANNEL_3_ID=-1003194973313
CHANNEL_3_LINK=https://t.me/b_111111111111111111

MAIN_GROUP_ID=-1003194973313
```

**Eslatma:** Agar sizning kanallaringiz boshqa bo'lsa, `.env` faylini tahrirlang.

### 4. Botni ishga tushirish

```bash
python main.py
```

## 📱 Foydalanish

### Foydalanuvchi uchun

1. Botga `/start` buyrug'ini yuboring
2. Majburiy kanallarga obuna bo'ling
3. "Obunani tekshirish" tugmasini bosing
4. Bosh menyudan kerakli xizmatni tanlang:
   - 🚖 Yo'lovchi sifatida
   - 🚕 Taksichi sifatida
   - 📦 Pochta jo'natish
   - 👨‍💼 Admin bilan bog'lanish

### Yo'lovchi rejimi

1. Yo'nalishni tanlang (Beshariq ↔️ Toshkent)
2. Yo'lovchilar sonini kiriting (1-4)
3. Telefon raqamingizni yuboring
4. Qo'shimcha ma'lumot kiriting (ixtiyoriy)
5. Buyurtmani tasdiqlang

### Taksichi rejimi

1. Yo'nalishni tanlang
2. Bo'sh joylar sonini kiriting (1-4)
3. Telefon raqamingizni yuboring
4. Qo'shimcha ma'lumot kiriting (ixtiyoriy)
5. E'lonni tasdiqlang

### Pochta rejimi

1. Yo'nalishni tanlang
2. Pochta turini tanlang (Hujjat, Paket, Elektronika, Boshqa)
3. Og'irligini tanlang (1-30 kg)
4. Telefon raqamingizni yuboring
5. Qo'shimcha ma'lumot kiriting (ixtiyoriy)
6. Buyurtmani tasdiqlang

### Band qilish

- Faqat yo'lovchi va pochta e'lonlarida "🔒 Band qilish" tugmasi mavjud
- Taksichi e'lonlarida band qilish yo'q
- O'z buyurtmangizni band qila olmaysiz
- Botga /start bosgan foydalanuvchilar band qilishi mumkin

### 🤖 Avtomatik Javob va Reklama

**Botni guruh/kanalga admin qilish:**
1. Botni guruh yoki kanalga qo'shing
2. Botni admin qilib tayinlang
3. Bot avtomatik ravishda kalit so'zlarni aniqlaydi
4. Guruhda "taksi", "yo'lovchi" kabi so'zlar yozilsa avtomatik javob beradi
5. Har 5 minutda avtomatik reklama yuboriladi

**Misol:**
```
Foydalanuvchi: Taksi kerak Toshkentga
Bot: 🚖 TEZ VA OSON TAKSI TOPISH UCHUN!
     Bizning bot orqali tez taksi chaqiring...
```

## 🔧 Texnik Ma'lumotlar

### In-Memory Storage

Bot barcha ma'lumotlarni RAM da saqlaydi:
- Foydalanuvchi holatlari (user states)
- Vaqtinchalik ma'lumotlar (user data)
- Buyurtmalar (orders)
- Band qilingan buyurtmalar (booked orders)
- /start bosgan foydalanuvchilar
- **YANGI:** Admin bo'lgan guruh/kanallar ro'yxati

### Avtomatik Javob Tizimi

Bot guruh xabarlarini tekshiradi:
1. Botning admin ekanligini aniqlaydi
2. Guruhni admin chat lar ro'yxatiga qo'shadi
3. Kalit so'zlarni aniqlaydi
4. Mos javob xabarini yuboradi (reply sifatida)

### Conversation States

Bot quyidagi holatlarni boshqaradi:
- Yo'lovchi holatlari (direction, count, phone, comment, confirm)
- Taksichi holatlari (direction, seats, phone, comment, confirm)
- Pochta holatlari (direction, type, weight, phone, comment, confirm)

### Error Handling

- Barcha xatoliklar log ga yoziladi
- Foydalanuvchiga tushunarli xabar ko'rsatiladi
- Bot ishlashda davom etadi

## 👨‍💻 Dasturchi

- **Telegram:** @Dasturchi_101
- **Telefon:** +998 99 565 41 04

## 📞 Admin

- **Telegram:** @u019db
- **Telefon:** +998 93 603 88 15

## 📝 Litsenziya

Bu bot Beshariq-Toshkent taksi va pochta xizmati uchun yaratilgan.

---

**Eslatma:** Bot to'liq ishga tushishi uchun barcha kanal va guruh ID lari to'g'ri bo'lishi kerak.
