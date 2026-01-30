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
        # ✅ DEBUG: state turini chiqarish
        print(f"🔧 OrderManager.set_state: user_id={user_id}, state={state}, type={type(state)}")
        
        # Agar state integer bo'lsa, uni States ga o'tkazish
        if isinstance(state, int):
            try:
                # Integer dan States ga o'tkazish
                state = States(state)
                print(f"🔧 OrderManager.set_state: Converted int to States: {state}")
            except ValueError:
                print(f"⚠️ OrderManager.set_state: Invalid state integer: {state}")
        
        self.user_states[user_id] = state
    
    def get_state(self, user_id: int) -> Union[States, int, None]:
        """Foydalanuvchi holatini olish"""
        state = self.user_states.get(user_id)
        
        # ✅ DEBUG: state turini chiqarish
        print(f"🔧 OrderManager.get_state: user_id={user_id}, state={state}, type={type(state)}")
        
        # Agar state None bo'lsa, START holatini qaytarish
        if state is None:
            return States.START
        
        # Agar state integer bo'lsa, uni States ga o'tkazish
        if isinstance(state, int):
            try:
                state = States(state)
                print(f"🔧 OrderManager.get_state: Converted int to States: {state}")
                return state
            except ValueError:
                print(f"⚠️ OrderManager.get_state: Invalid state integer: {state}")
                return States.START
        
        return state
    
    def clear_state(self, user_id: int) -> None:
        """Foydalanuvchi holatini tozalash"""
        if user_id in self.user_states:
            print(f"🔧 OrderManager.clear_state: user_id={user_id}")
            del self.user_states[user_id]
    
    def set_user_data(self, user_id: int, key: str, value: Any) -> None:
        """Foydalanuvchi ma'lumotlarini saqlash"""
        print(f"🔧 OrderManager.set_user_data: user_id={user_id}, key={key}, value={value}")
        
        if user_id not in self.user_data:
            self.user_data[user_id] = {}
        self.user_data[user_id][key] = value
    
    def get_user_data(self, user_id: int, key: str = None) -> Any:
        """Foydalanuvchi ma'lumotlarini olish"""
        print(f"🔧 OrderManager.get_user_data: user_id={user_id}, key={key}")
        
        if user_id not in self.user_data:
            print(f"🔧 OrderManager.get_user_data: No data for user {user_id}")
            return None
        
        if key:
            value = self.user_data[user_id].get(key)
            print(f"🔧 OrderManager.get_user_data: Found value: {value}")
            return value
        
        print(f"🔧 OrderManager.get_user_data: Returning all data")
        return self.user_data[user_id]
    
    def clear_user_data(self, user_id: int) -> None:
        """Foydalanuvchi ma'lumotlarini tozalash"""
        print(f"🔧 OrderManager.clear_user_data: Clearing data for user {user_id}")
        
        if user_id in self.user_data:
            del self.user_data[user_id]
        self.clear_state(user_id)
        
        # ✅ Foydalanuvchini START holatiga qaytarish
        self.set_state(user_id, States.START)
        print(f"🔧 OrderManager.clear_user_data: User {user_id} reset to START state")
    
    def add_order(self, message_id: int, order_data: Dict[str, Any]) -> None:
        """Yangi buyurtma qo'shish"""
        print(f"🔧 OrderManager.add_order: message_id={message_id}")
        self.orders[message_id] = {
            **order_data,
            "created_at": datetime.now().isoformat()
        }
    
    def get_order(self, message_id: int) -> Optional[Dict[str, Any]]:
        """Buyurtma ma'lumotlarini olish"""
        order = self.orders.get(message_id)
        print(f"🔧 OrderManager.get_order: message_id={message_id}, found={order is not None}")
        return order
    
    def book_order(self, message_id: int, user_id: int) -> bool:
        """
        Buyurtmani band qilish
        Returns: True - muvaffaqiyatli, False - allaqachon band qilingan
        """
        print(f"🔧 OrderManager.book_order: message_id={message_id}, user_id={user_id}")
        
        if message_id in self.booked_orders:
            print(f"🔧 OrderManager.book_order: Already booked by {self.booked_orders[message_id]}")
            return False
        
        self.booked_orders[message_id] = user_id
        print(f"🔧 OrderManager.book_order: Successfully booked")
        return True
    
    def is_order_booked(self, message_id: int) -> bool:
        """Buyurtma band qilinganligini tekshirish"""
        booked = message_id in self.booked_orders
        print(f"🔧 OrderManager.is_order_booked: message_id={message_id}, booked={booked}")
        return booked
    
    def get_booker(self, message_id: int) -> Optional[int]:
        """Buyurtmani band qilgan foydalanuvchini olish"""
        booker = self.booked_orders.get(message_id)
        print(f"🔧 OrderManager.get_booker: message_id={message_id}, booker={booker}")
        return booker
    
    def add_started_user(self, user_id: int) -> None:
        """Foydalanuvchini /start bosganlar ro'yxatiga qo'shish"""
        print(f"🔧 OrderManager.add_started_user: user_id={user_id}")
        self.started_users.add(user_id)
    
    def has_started(self, user_id: int) -> bool:
        """Foydalanuvchi /start bosganligini tekshirish"""
        has_started = user_id in self.started_users
        print(f"🔧 OrderManager.has_started: user_id={user_id}, has_started={has_started}")
        return has_started
    
    def print_user_states(self):
        """Barcha foydalanuvchi holatlarini ko'rsatish (debug uchun)"""
        print("\n" + "="*50)
        print("📊 CURRENT USER STATES:")
        print("="*50)
        
        if not self.user_states:
            print("No users in states")
            return
        
        for user_id, state in self.user_states.items():
            # State nomini aniqlash
            state_name = "UNKNOWN"
            if isinstance(state, States):
                state_name = state.name
            elif isinstance(state, int):
                try:
                    state_name = States(state).name
                except ValueError:
                    state_name = f"Invalid int: {state}"
            
            print(f"User {user_id}: {state_name} ({state})")
        
        print("="*50 + "\n")

# Global order manager instance
order_manager = OrderManager()