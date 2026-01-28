# Telegram Taksi va Po'chta Bot

Professional Telegram bot yo'lovchilar, haydovchilar va po'chta jo'natish uchun.

## Xususiyatlari

✅ **Yuqori tezlik va samaradorlik**
- Asinxron ishlash (aiogram 3.x)
- RAM-da ma'lumotlar saqlash (tezkor ishlash)
- Optimallashtrilgan kod
- Ko'p foydalanuvchilar uchun moslashgan

✅ **To'liq funksional**
- Yo'lovchi rejimi
- Haydovchi rejimi
- Po'chta jo'natish
- Avtomatik kanal obunasini tekshirish
- Guruhda e'lonlarni band qilish
- Har 15 daqiqada avtomatik reklama

✅ **Xavfsizlik**
- Faqat belgilangan guruhda ishlash
- E'lon yaratuvchi o'z e'lonini band qila olmaydi
- Obuna majburiy tekshiruvi

## O'rnatish

### 1. Talablarni o'rnatish

```bash
pip install -r requirements.txt
```

### 2. Konfiguratsiya

`.env` faylini tahrirlang va o'z ma'lumotlaringizni kiriting:

```env
BOT_TOKEN=your_bot_token_here
CHANNEL_1_ID=-100...
CHANNEL_1_LINK=https://t.me/your_channel
...
MAIN_GROUP_ID=-100...
```

### 3. Botni ishga tushirish

```bash
python main.py
```

## Fayl tuzilishi

```
├── main.py           # Asosiy fayl
├── config.py         # Konfiguratsiya
├── handlers.py       # Barcha handlerlar
├── keyboards.py      # Klaviaturalar
├── utils.py          # Yordamchi funksiyalar
├── scheduler.py      # Avtomatik xabarlar
├── requirements.txt  # Kutubxonalar ro'yxati
└── .env             # Muhit o'zgaruvchilari
```

## Ishlatish

### Foydalanuvchi uchun:

1. `/start` - Botni boshlash
2. Kanallarga obuna bo'lish
3. Kerakli xizmatni tanlash:
   - 🚗 Yo'lovchi sifatida
   - 🚕 Taksichi sifatida
   - 📦 Po'chta jo'natish
4. Ma'lumotlarni to'ldirish
5. E'lonni tasdiqlash

### Guruhda:

- E'lonlar avtomatik guruhga tushadi
- "🔒 Band qilish" tugmasi orqali band qilish mumkin
- Har 15 daqiqada bot reklama xabari yuboradi

## Xususiyatlari

### RAM-da saqlash
Bot barcha ma'lumotlarni RAMda saqlaydi, bu:
- ⚡ Juda tez ishlashni ta'minlaydi
- 🔄 Qayta ishga tushganda tozalanadi
- 💾 Ma'lumotlar bazasi kerak emas

### Asinxron arxitektura
- Ko'p foydalanuvchilar bir vaqtda ishlatishi mumkin
- Blocking operatsiyalar yo'q
- Yuqori unumdorlik

### Modulli tuzilma
- Har bir modul alohida vazifani bajaradi
- Oson kengaytirish va o'zgartirish
- Toza va tushunarli kod

## Texnik talablar

- Python 3.10+
- aiogram 3.4.1
- aiohttp 3.9.1
- python-dotenv 1.0.0

## Xavfsizlik

Bot quyidagilarni ta'minlaydi:
- Faqat ruxsat etilgan guruhda ishlash
- Spam himoyasi
- Foydalanuvchilar ma'lumotlari xavfsizligi

## Qo'llab-quvvatlash

Muammo yoki savol bo'lsa:
- Admin: @u019db
- Dasturchi: @Dasturchi_101

## Litsenziya

Shaxsiy foydalanish uchun.

---

**Ishlab chiqildi professional Python dasturchilar tomonidan** 🚀
