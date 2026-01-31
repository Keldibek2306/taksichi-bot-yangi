"""
In-memory ma'lumotlar boshqaruvchi moduli
Bu yerda barcha buyurtmalar va foydalanuvchi holatlari RAM da saqlanadi
"""

from datetime import datetime
from typing import Dict, Optional, Any, Union
from enum import IntEnum

from config import States

class OrderManager:
    """
    Buyurtmalar va foydalanuvchilar holatini boshqaruvchi klass
    Barcha ma'lumotlar RAM da saqlanadi (in-memory storage)
    """
    
    def __init__(self):
        # Foydalanuvchilar holati (user_id: state)
        # ✅ O'ZGARTIRILDI: State IntEnum yoki integer
        self.user_states: Dict[int, Union[States, int]] = {}
        
        # Foydalanuvchilar vaqtinchalik ma'lumotlari (user_id: data_dict)
        self.user_data: Dict[int, Dict[str, Any]] = {}
        
        # E'lonlar (message_id: order_info)
        self.orders: Dict[int, Dict[str, Any]] = {}
        
        # Band qilingan e'lonlar (message_id: booker_user_id)
        self.booked_orders: Dict[int, int] = {}
        
        # Botga /start bosgan foydalanuvchilar
        self.started_users: set = set()
    
    def set_state(self, user_id: int, state: Union[States, int]) -> None:
        """Foydalanuvchi holatini o'rnatish"""
        # Agar state integer bo'lsa, uni States ga o'tkazish
        if isinstance(state, int):
            try:
                # Integer dan States ga o'tkazish
                state = States(state)
            except ValueError:
                pass
        
        self.user_states[user_id] = state
    
    def get_state(self, user_id: int) -> Union[States, int, None]:
        """Foydalanuvchi holatini olish"""
        state = self.user_states.get(user_id)
        
        # Agar state None bo'lsa, START holatini qaytarish
        if state is None:
            return States.START
        
        # Agar state integer bo'lsa, uni States ga o'tkazish
        if isinstance(state, int):
            try:
                state = States(state)
                return state
            except ValueError:
                return States.START
        
        return state
    
    def clear_state(self, user_id: int) -> None:
        """Foydalanuvchi holatini tozalash"""
        if user_id in self.user_states:
            del self.user_states[user_id]
    
    def set_user_data(self, user_id: int, key: str, value: Any) -> None:
        """Foydalanuvchi ma'lumotlarini saqlash"""
        if user_id not in self.user_data:
            self.user_data[user_id] = {}
        self.user_data[user_id][key] = value
    
    def get_user_data(self, user_id: int, key: str = None) -> Any:
        """Foydalanuvchi ma'lumotlarini olish"""
        if user_id not in self.user_data:
            return None
        
        if key:
            return self.user_data[user_id].get(key)
        
        return self.user_data[user_id]
    
    def clear_user_data(self, user_id: int) -> None:
        """Foydalanuvchi ma'lumotlarini tozalash"""
        if user_id in self.user_data:
            del self.user_data[user_id]
        self.clear_state(user_id)
        
        # ✅ Foydalanuvchini START holatiga qaytarish
        self.set_state(user_id, States.START)
    
    def add_order(self, message_id: int, order_data: Dict[str, Any]) -> None:
        """Yangi buyurtma qo'shish"""
        self.orders[message_id] = {
            **order_data,
            "created_at": datetime.now().isoformat()
        }
    
    def get_order(self, message_id: int) -> Optional[Dict[str, Any]]:
        """Buyurtma ma'lumotlarini olish"""
        return self.orders.get(message_id)
    
    def book_order(self, message_id: int, user_id: int) -> bool:
        """
        Buyurtmani band qilish
        Returns: True - muvaffaqiyatli, False - allaqachon band qilingan
        """
        if message_id in self.booked_orders:
            return False
        
        self.booked_orders[message_id] = user_id
        return True
    
    def is_order_booked(self, message_id: int) -> bool:
        """Buyurtma band qilinganligini tekshirish"""
        return message_id in self.booked_orders
    
    def get_booker(self, message_id: int) -> Optional[int]:
        """Buyurtmani band qilgan foydalanuvchini olish"""
        return self.booked_orders.get(message_id)
    
    def add_started_user(self, user_id: int) -> None:
        """Foydalanuvchini /start bosganlar ro'yxatiga qo'shish"""
        self.started_users.add(user_id)
    
    def has_started(self, user_id: int) -> bool:
        """Foydalanuvchi /start bosganligini tekshirish"""
        return user_id in self.started_users

# Global order manager instance
order_manager = OrderManager()