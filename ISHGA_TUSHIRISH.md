# 🚀 AVTOMATIK JAVOB VA REKLAMA - ISHGA TUSHIRISH

## ✅ BO'TNING YANGI IMKONIYATLARI

### 1. 🤖 Avtomatik Javob
- Guruhda "taksi", "yo'lovchi", "pochta" kabi so'zlar yozilsa avtomatik javob beradi
- Faqat bot **admin** bo'lgan guruhlarda ishlaydi

### 2. 📣 Avtomatik Reklama
- **MAIN_GROUP**: har 15 minutda
- **Barcha admin guruhlar**: har 5 minutda

---

## 📋 ISHGA TUSHIRISH QO'LLANMASI

### Qadam 1: Botni O'rnatish

```bash
cd telegram_bot
pip install -r requirements.txt
```

### Qadam 2: Botni Guruhga Qo'shish

1. Telegram da botingizni toping
2. Guruhga qo'shing
3. **MUHIM:** Botni **ADMIN** qilib tayinlang!
4. Admin huquqlari:
   - ✅ Xabar yuborish
   - ✅ Xabarlarni o'chirish (ixtiyoriy)

### Qadam 3: Botni Ishga Tushirish

```bash
python main.py
```

Bot ishga tushganda:
```
INFO - Bot is starting...
INFO - Auto-reply enabled for admin groups/channels
INFO - Advertisement jobs scheduled
INFO - Bot added as admin to: -1001234567890 (Test Guruh)
```

### Qadam 4: Test Qilish

1. **Avtomatik javobni test qilish:**
   - Guruhga "taksi kerak" yozing
   - Bot avtomatik javob berishi kerak

2. **Reklamani test qilish:**
   - 5 minut kuting
   - Guruhda reklama paydo bo'ladi

---

## 🔧 SOZLAMALAR

### Kalit So'zlarni O'zgartirish

`config.py` faylini oching:

```python
AUTO_REPLY_KEYWORDS = {
    "taksi": ["taksi", "taxi", "mashina", "haydovchi"],
    "yolovchi": ["yo'lovchi", "yolovchi", "passenger", "odam"],
    "umumiy": ["pochta", "paket", "yuborish"]
}
```

### Reklama Vaqtini O'zgartirish

```python
MAIN_GROUP_AD_INTERVAL = 900      # 15 minut (sekundlarda)
ALL_GROUPS_AD_INTERVAL = 300      # 5 minut (sekundlarda)
```

### Javob Xabarlarini O'zgartirish

```python
AUTO_REPLY_MESSAGES = {
    "taksi": """🚖 TEZ VA OSON TAKSI TOPISH UCHUN!
    
Bizning bot orqali:
✅ Tez taksi chaqiring
...
🤖 @{bot_username} ga /start bosing!""",
    ...
}
```

---

## ❓ TEZKOR MUAMMOLARNI HAL QILISH

### ❌ Avtomatik javob ishlamayapti?

**Tekshirish ro'yxati:**
1. ✅ Bot guruhda **admin**mi?
2. ✅ Bot **xabar yuborish** huquqiga egami?
3. ✅ To'g'ri kalit so'z yozildimi? ("taksi", "yo'lovchi" va h.k.)

**Loglarni tekshirish:**
```
# Bot ishlaganida quyidagilar ko'rinishi kerak:
INFO - Added admin chat: -1001234567890 (Test Guruh)
INFO - Auto-reply sent in -1001234567890 for keyword type: taksi
```

### ❌ Reklama yuborilmayapti?

**Tekshirish:**
1. ✅ Bot admin bo'lganidan keyin 5 minut kutilganmi?
2. ✅ Logda "Advertisement sent to X groups" yozuvimi?

**Logni ko'rish:**
```
INFO - Advertisement sent to 3 admin groups/channels at 2026-01-29 12:05:30
```

### ❌ Guruh ro'yxatga tushmayapti?

**Yechim 1:** Guruhda xabar yozing
- Bot avtomatik aniqlaydi va ro'yxatga qo'shadi

**Yechim 2:** Botni qayta qo'shing
- Guruhdan botni chiqaring
- Qaytadan admin qilib qo'shing

---

## 📊 MONITORING VA LOGLAR

### Foydali Loglar

Bot ishlayotganida quyidagi loglar chiqadi:

```
# Bot guruhga qo'shilganda:
INFO - Bot added as admin to: -1001234567890 (Test Guruh)

# Xabarga javob berganda:
INFO - Auto-reply sent in -1001234567890 for keyword type: taksi

# Reklama yuborilganda:
INFO - Advertisement sent to MAIN_GROUP at 2026-01-29 12:00:10
INFO - Advertisement sent to 5 admin groups/channels at 2026-01-29 12:05:30
```

### Admin Guruhlar Ro'yxatini Ko'rish

Python shell da:

```python
from handlers.auto_reply_handler import get_admin_chats

print(get_admin_chats())
# Output: [-1001234567890, -1003194973313, ...]
```

---

## 💡 MASLAHATLAR

### 1. Ko'p Guruhlar Uchun

Agar ko'p guruhlarda botingiz bo'lsa:
- Barcha guruhlarda admin qiling
- Bot avtomatik aniqlaydi
- 5 minutda barchaga reklama yuboriladi

### 2. Test Rejimi

Test qilish uchun vaqtni qisqartiring:

```python
# config.py
ALL_GROUPS_AD_INTERVAL = 60  # 1 minut (test uchun)
```

Keyin qayta oddiy qilib qo'ying:
```python
ALL_GROUPS_AD_INTERVAL = 300  # 5 minut
```

### 3. Kanal uchun

Kanal uchun ham ishlaydi:
1. Botni kanalga qo'shing
2. Admin qiling
3. Har 5 minutda reklama yuboriladi

---

## 🎯 QISQACHA

### ✅ NIMA QILISH KERAK:
1. Botni guruhga qo'shing
2. **ADMIN** qiling
3. `python main.py` ishga tushiring
4. Tayyor!

### ✅ BOT AVTOMATIK QILADI:
1. Guruhni ro'yxatga oladi
2. Kalit so'zlarga javob beradi
3. Har 5 minutda reklama yuboradi

### ❌ NIMA QILMASLIK KERAK:
1. Botni admin qilmasdan qoldirmaslik
2. Bot ishlamay turganida kutmaslik
3. Kalit so'zlarni to'g'ri yozmaslik

---

**Yordam kerakmi?**
- 👨‍💻 Dasturchi: @Dasturchi_101
- 📞 Telefon: +998 99 565 41 04
