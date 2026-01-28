#!/bin/bash

echo "🚀 Telegram Bot ishga tushirilmoqda..."

# Virtual environment yaratish
if [ ! -d "venv" ]; then
    echo "📦 Virtual environment yaratilmoqda..."
    python3 -m venv venv
fi

# Virtual environment aktivlashtirish
source venv/bin/activate

# Kutubxonalarni o'rnatish
echo "📚 Kutubxonalar o'rnatilmoqda..."
pip install -r requirements.txt

# Botni ishga tushirish
echo "✅ Bot ishga tushdi!"
python main.py
