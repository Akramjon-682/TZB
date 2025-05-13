import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Loyihaning ildiz papkasini sys.path ga qo‘shamiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schema import User, Card

# SQLite bazaga ulanish
engine = create_engine("sqlite:///TZB.db")
Session = sessionmaker(bind=engine)
session = Session()

# Barcha foydalanuvchilarni olish
users = session.query(User).all()


# Har bir foydalanuvchining kartalarini ko‘rsatish
for user in users:
    print(f"\n👤 Foydalanuvchi: {user.full_name} (ID: {user.id})")
    if not user.cards:
        print("   ❌ Karta topilmadi.")
        continue
