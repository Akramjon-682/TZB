import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Root papkani sys.path ga qo‘shamiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schema import Base, User, Card  # kerakli modellarni import qilamiz

# Bazaga ulanish (SQLite fayl bazasi bilan)
engine = create_engine("sqlite:///TZB.db")
Session = sessionmaker(bind=engine)
session = Session()

# Limit qiymati (masalan, 100000 UZS)
limit = 100000

# Barcha foydalanuvchilarni olyapmiz
users = session.query(User).all()

# Har bir foydalanuvchining kartalari limitini tekshiramiz
for user in users:
    for card in user.cards:
        if card.balance < limit:
            print(f"Foydalanuvchi: {user.full_name}, Karta raqami: {card.card_number}, Balans: {card.balance} UZS (limitdan past)")
