# 🆕 YANGI FUNKSIYALAR

## 🤖 Avtomatik Javob Tizimi

### Qanday Ishlaydi?

Bot admin bo'lgan guruh va kanallarda yozilgan xabarlarga avtomatik javob beradi.

### Sozlash

1. **Botni guruh/kanalga qo'shing**
   - Guruh yoki kanalga botni a'zo qiling
   
2. **Botni admin qiling**
   - Bot admin huquqiga ega bo'lishi kerak
   - Kamida "Xabar yuborish" huquqi kerak
   
3. **Avtomatik ishlaydi!**
   - Bot guruhda xabar yozilganini sezadi
   - Kalit so'zlarni aniqlaydi
   - Avtomatik javob beradi

### Kalit So'zlar va Javoblar

#### 1. TAKSI kalit so'zlari
```
taksi, taxi, mashina, haydovchi, driver
```

**Javob:**
```
🚖 TEZ VA OSON TAKSI TOPISH UCHUN!

Bizning bot orqali:
✅ Tez taksi chaqiring
✅ Yo'lovchilar bilan bog'laning
✅ Ishonchli xizmat

🤖 @bot_username ga /start bosing!
```

#### 2. YO'LOVCHI kalit so'zlari
```
yo'lovchi, yolovchi, passenger, odam, joy
```

**Javob:**
```
👥 TEZ VA OSON YO'LOVCHI TOPISH UCHUN!

Bizning bot orqali:
✅ Yo'lovchilarni toping
✅ Tez buyurtma bering
✅ Qulay narxlar

🤖 @bot_username ga /start bosing!
```

#### 3. UMUMIY kalit so'zlar
```
pochta, paket, yuborish, jo'natish, xizmat, service
```

**Javob:**
```
🚖 TAKSI VA YO'LOVCHI TOPISH UCHUN!

Bizning bot orqali:
✅ Tez taksi chaqiring
✅ Yo'lovchilarni toping
✅ Pochta jo'nating

🤖 @bot_username ga /start bosing!
```

### Misollar

**Misol 1:**
```
Foydalanuvchi: Taksi kerak Toshkentga
Bot: [Avtomatik javob - TAKSI]
```

**Misol 2:**
```
Foydalanuvchi: Yo'lovchi bor emasmikan?
Bot: [Avtomatik javob - YO'LOVCHI]
```

**Misol 3:**
```
Foydalanuvchi: Pochta jo'natmoqchiman
Bot: [Avtomatik javob - UMUMIY]
```

---

## 📣 Avtomatik Reklama Tizimi

### 2 Xil Reklama Rejimi

#### 1. MAIN_GROUP ga reklama
- **Interval:** Har 15 minutda
- **Guruh:** Faqat MAIN_GROUP_ID
- **Xabar:** AD_MESSAGE (config.py da)

#### 2. Barcha admin guruh/kanallarga reklama
- **Interval:** Har 5 minutda
- **Guruhlar:** Bot admin bo'lgan barcha guruh va kanallar
- **Xabar:** Qisqaroq reklama matni
- **Avtomatik:** Yangi guruh/kanal topilsa, avtomatik qo'shiladi

### Vaqt Jadvali

```
00:00 - Bot ishga tushdi
00:00:10 - MAIN_GROUP ga birinchi reklama
00:00:30 - Barcha admin guruh/kanallarga birinchi reklama
00:05:30 - Barcha admin guruh/kanallarga 2-reklama
00:10:30 - Barcha admin guruh/kanallarga 3-reklama
00:15:10 - MAIN_GROUP ga 2-reklama
00:15:30 - Barcha admin guruh/kanallarga 4-reklama
...va hokazo
```

### Admin Guruh/Kanallarni Aniqlash

Bot avtomatik ravishda admin bo'lgan guruh/kanallarni aniqlaydi:

1. **Avtomatik aniqlash:**
   - Guruhda xabar yoziladi
   - Bot admin ekanligini tekshiradi
   - Ro'yxatga qo'shadi

2. **RAM da saqlash:**
   - `context.bot_data["admin_chats"]` da
   - Bot qayta ishga tushsa, ro'yxat yo'qoladi
   - Lekin tez vaqtda qayta to'ldiriladi

3. **Avtomatik tozalash:**
   - Agar bot guruhdan chiqarilsa
   - Yoki blocklanса
   - Avtomatik ro'yxatdan o'chiriladi

---

## 📁 Yangi Fayllar

### handlers/auto_reply_handler.py

```python
# Asosiy funksiyalar:
- handle_group_message()         # Guruh xabarlarini qayta ishlash
- detect_keyword_type()           # Kalit so'zlarni aniqlash
- is_bot_admin()                  # Bot admin ekanligini tekshirish
- check_and_add_admin_chat()      # Admin chat ni ro'yxatga qo'shish
- get_all_admin_chats()           # Barcha admin chat larni olish
```

### config.py - Yangi sozlamalar

```python
# Avtomatik javob xabarlari
AUTO_REPLY_MESSAGES = {
    "taksi": "...",
    "yolovchi": "...",
    "umumiy": "..."
}

# Kalit so'zlar
AUTO_REPLY_KEYWORDS = {
    "taksi": [...],
    "yolovchi": [...],
    "umumiy": [...]
}

# Reklama intervallari
MAIN_GROUP_AD_INTERVAL = 900      # 15 minut
ALL_GROUPS_AD_INTERVAL = 300      # 5 minut
```

---

## 🎯 Foydalanish Bo'yicha Maslahatlar

### 1. Kalit So'zlarni O'zgartirish

`config.py` faylida kalit so'zlarni o'zgartirishingiz mumkin:

```python
AUTO_REPLY_KEYWORDS = {
    "taksi": ["taksi", "taxi", "mashina", "moshina", "avto"],
    ...
}
```

### 2. Javob Xabarlarini O'zgartirish

```python
AUTO_REPLY_MESSAGES = {
    "taksi": """Sizning xabaringiz...""",
    ...
}
```

### 3. Reklama Vaqtini O'zgartirish

```python
MAIN_GROUP_AD_INTERVAL = 1800     # 30 minut
ALL_GROUPS_AD_INTERVAL = 600      # 10 minut
```

---

## ⚠️ Muhim Eslatmalar

1. **Bot admin bo'lishi kerak**
   - Aks holda avtomatik javob ishlamaydi
   - Reklama yuborilmaydi

2. **Xabar yuborish huquqi**
   - Bot guruhda xabar yuborish huquqiga ega bo'lishi kerak

3. **RAM da saqlash**
   - Admin guruhlar ro'yxati RAM da
   - Bot qayta ishga tushsa, ro'yxat yo'qoladi
   - Lekin tez vaqtda qayta to'ldiriladi

4. **Spam oldini olish**
   - Bir xil xabarga bir marta javob beradi
   - Botning o'z xabarlariga javob bermaydi

---

## 🔧 Texnik Tafsilotlar

### Message Handler Priority

```python
# 1. Guruh xabarlari (avtomatik javob)
filters.ChatType.GROUPS & filters.TEXT

# 2. Shaxsiy xabarlar (telefon, komment)
filters.ChatType.PRIVATE & filters.TEXT
```

### Error Handling

- Agar guruhga xabar yuborib bo'lmasa, log ga yoziladi
- Agar bot blocklanган bo'lsa, ro'yxatdan o'chiriladi
- Barcha xatoliklar qayd etiladi

### Performance

- Minimal resurs sarfi
- Tez javob berish
- Async/await ishlatiladi

---

**Savollar yoki muammolar bo'lsa:**
- Dasturchi: @Dasturchi_101
- Telefon: +998 99 565 41 04
