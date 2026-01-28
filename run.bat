@echo off
echo 🚀 Telegram Bot ishga tushirilmoqda...

REM Virtual environment yaratish
if not exist "venv" (
    echo 📦 Virtual environment yaratilmoqda...
    python -m venv venv
)

REM Virtual environment aktivlashtirish
call venv\Scripts\activate.bat

REM Kutubxonalarni o'rnatish
echo 📚 Kutubxonalar o'rnatilmoqda...
pip install -r requirements.txt

REM Botni ishga tushirish
echo ✅ Bot ishga tushdi!
python main.py

pause
