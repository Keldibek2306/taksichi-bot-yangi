# Bot Arxitekturasi

```
┌─────────────────────────────────────────────────────────┐
│                     TELEGRAM BOT                         │
│                  (main.py - entry point)                 │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
    ┌────▼────┐           ┌─────▼─────┐
    │ Handlers│           │ Scheduler │
    │ Module  │           │  Module   │
    └────┬────┘           └─────┬─────┘
         │                      │
         │              ┌───────▼────────┐
         │              │ Periodic Msgs  │
         │              │ (Every 15 min) │
         │              └────────────────┘
         │
    ┌────▼──────────────────────────────┐
    │                                   │
┌───▼────┐  ┌─────────┐  ┌──────────┐ │
│KeyBoards│  │ Utils   │  │  Config  │ │
│ Module │  │ Module  │  │  Module  │ │
└────────┘  └─────────┘  └──────────┘ │
                                       │
└───────────────────────────────────────┘
```

## Modullar va ularning vazifalari:

### 1. **main.py** - Asosiy fayl
- Botni ishga tushirish
- Dispatcher sozlash
- Polling boshlash

### 2. **handlers.py** - Handler moduli
- Foydalanuvchi bilan interaksiya
- Buyruqlarni qayta ishlash
- FSM (State) boshqaruv
- Callback querylarni boshqarish

### 3. **keyboards.py** - Klaviaturalar
- Inline klaviaturalar yaratish
- Tugmalar tuzilishi
- Dinamik klaviaturalar

### 4. **utils.py** - Yordamchi funksiyalar
- Obunani tekshirish
- E'lonlar formatlash
- Umumiy funksiyalar

### 5. **config.py** - Konfiguratsiya
- Bot sozlamalari
- Kanal ma'lumotlari
- Konstantalar

### 6. **scheduler.py** - Rejalashtiruvchi
- Har 15 daqiqada xabar
- Avtomatik vazifalar

## Ma'lumotlar oqimi:

```
Foydalanuvchi
     │
     ▼
/start buyrug'i
     │
     ▼
Obunani tekshirish
     │
     ├─► Obuna bo'lmagan ──► Obuna klaviaturasi
     │
     └─► Obuna bo'lgan ──► Asosiy menyu
              │
              ├─► Yo'lovchi ──► Yo'nalish ──► Odamlar ──► Telefon ──► E'lon
              │
              ├─► Haydovchi ──► Yo'nalish ──► Joylar ──► Telefon ──► E'lon
              │
              └─► Po'chta ──► Yo'nalish ──► Turi ──► Og'irligi ──► Telefon ──► E'lon
```

## Texnik xususiyatlar:

### ⚡ Tezlik va optimallashtirish:
- **Asinxron ishlash**: aiogram 3.x (async/await)
- **RAM saqlash**: Ma'lumotlar dictionary'larda
- **Zero blocking**: Hech qanday blocking operatsiyalar yo'q
- **Parallel processing**: Ko'p foydalanuvchi bir vaqtda

### 🔒 Xavfsizlik:
- Environment variables (.env)
- Faqat ruxsat etilgan guruhda ishlash
- E'lon yaratuvchini tekshirish
- Spam himoyasi

### 📊 Masshtablanish:
- Modulli arxitektura
- Mustaqil komponentlar
- Oson kengaytirish
- Toza kod (Clean Code)

### 💾 Ma'lumotlar boshqaruvi:
```python
# RAM-da saqlash (tez)
user_data_storage = {}
announcement_creators = {}

# Qayta ishga tushganda tozalanadi
# Ma'lumotlar bazasi kerak emas
```

## Ishlash printsipi:

1. **Bot ishga tushadi** → Polling boshlanadi
2. **Foydalanuvchi /start** → Obuna tekshiriladi
3. **Menyu tanlash** → State o'rnatiladi
4. **Ma'lumot to'plash** → RAM-da saqlanadi
5. **Tasdiqlash** → Guruhga jo'natiladi
6. **RAM tozalanadi** → Keyingi buyurtma uchun tayyor

## Afzalliklari:

✅ Juda tez (RAM)
✅ Ko'p foydalanuvchi
✅ Xavfsiz
✅ Oson boshqarish
✅ Professional kod
✅ Kengaytiriladigan
✅ Ma'lumotlar bazasi kerak emas
