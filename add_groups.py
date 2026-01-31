"""
Test skript - Guruhlarni qo'lda qo'shish
Agar bot qaysidir guruhda admin bo'lsa lekin ro'yxatga tushmagan bo'lsa,
shu skript orqali qo'lda qo'shishingiz mumkin
"""

from handlers.auto_reply_handler import add_admin_chat, get_admin_chats

# QUYIDAGI GURUH ID LARNI O'ZINGIZNIKI BILAN ALMASHTIRING
# Bot admin bo'lgan guruhlar ro'yxati

GURUHLAR = [
    # Misol: (-1001234567890, "Test Guruh"),
    # (-1003194973313, "Bizning Guruh"),
]

def main():
    #print("=" * 50)
    #print("GURUHLARNI RO'YXATGA QO'SHISH")
    #print("=" * 50)
    
    if not GURUHLAR:
        #print("\n⚠️  DIQQAT: GURUHLAR ro'yxati bo'sh!")
        #print("Faylni tahrirlang va guruh ID larini qo'shing")
        #print("\nMisol:")
        #print("GURUHLAR = [")
        #print("    (-1001234567890, 'Mening Guruhim'),")
        #print("    (-1003194973313, 'Boshqa Guruh'),")
        #print("]")
        return
    
    #print(f"\n{len(GURUHLAR)} ta guruh qo'shilmoqda...\n")
    
    for chat_id, chat_title in GURUHLAR:
        add_admin_chat(chat_id, chat_title)
        #print(f"✅ Qo'shildi: {chat_title} ({chat_id})")
    
    #print(f"\n{'='*50}")
    #print(f"Jami admin guruhlar: {len(get_admin_chats())}")
    #print(f"{'='*50}")
    
    #print("\n✅ Tayyor! Bot ishga tushganda bu guruhlarga reklama yuboriladi.")
    #print("💡 Bot ishga tushganda qo'shimcha guruhlar avtomatik qo'shiladi.\n")

if __name__ == "__main__":
    main()
