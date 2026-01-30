"""
Band qilish handler moduli
Yo'lovchi va pochta buyurtmalarini band qilish funksiyasi
"""

from telegram import Update
from telegram.ext import ContextTypes

from utils.order_manager import order_manager

async def book_order_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Band qilish tugmasi bosilganda
    
    Tekshiruvlar:
    1. Foydalanuvchi /start bosgan bo'lishi kerak
    2. O'z buyurtmasini band qila olmaydi
    3. Allaqachon band qilingan buyurtmani band qila olmaydi
    """
    query = update.callback_query
    user = query.from_user
    
    # Buyurtma ID sini olish
    order_id_str = query.data.replace("book_", "")
    
    try:
        order_id = int(order_id_str)
    except ValueError:
        await query.answer("❌ Xatolik yuz berdi!", show_alert=True)
        return
    
    # 1. Tekshiruv: Foydalanuvchi /start bosganmi?
    if not order_manager.has_started(user.id):
        await query.answer(
            "❌ Botga /start buyrug'ini bering!",
            show_alert=True
        )
        return
    
    # Buyurtma ma'lumotlarini olish
    order = order_manager.get_order(order_id)
    
    if not order:
        await query.answer("❌ Buyurtma topilmadi!", show_alert=True)
        return
    
    # 2. Tekshiruv: O'z buyurtmasini band qila olmasligi
    if order["user_id"] == user.id:
        await query.answer(
            "❌ O'z buyurtmangizni band qila olmaysiz!",
            show_alert=True
        )
        return
    
    # 3. Tekshiruv: Allaqachon band qilinganmi?
    if order_manager.is_order_booked(order_id):
        await query.answer(
            "❌ Bu buyurtma allaqachon band qilingan!",
            show_alert=True
        )
        return
    
    # Band qilish
    success = order_manager.book_order(order_id, user.id)
    
    if not success:
        await query.answer(
            "❌ Bu buyurtma allaqachon band qilingan!",
            show_alert=True
        )
        return
    
    # E'lon matnini yangilash
    username = f"@{user.username}" if user.username else f"{user.first_name}"
    
    original_text = query.message.text
    updated_text = f"{original_text}\n\n🔒 BAND QILINDI\n👤 {username} tomonidan"
    
    try:
        # Xabarni yangilash (tugmasiz)
        await query.edit_message_text(updated_text)
    except Exception as e:
        print(f"Error updating message: {e}")
    
    # Band qilganga xabar
    await query.answer("✅ Buyurtma muvaffaqiyatli band qilindi!", show_alert=True)
    
    # E'lon egasiga xabar
    try:
        await context.bot.send_message(
            chat_id=order["user_id"],
            text=f"🔔 Sizning buyurtmangiz band qilindi!\n\n"
                 f"👤 Band qildi: {username}"
        )
    except Exception as e:
        print(f"Error sending notification to order owner: {e}")
