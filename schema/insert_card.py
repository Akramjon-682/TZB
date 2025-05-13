import os
import sys
import random
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Loyihaning ildiz papkasini sys.path ga qo‘shamiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schema import Base, Card, User  # schema/__init__.py ichidagi classlar

fake = Faker()

# SQLite bazaga ulanish
engine = create_engine("sqlite:///TZB.db")
Session = sessionmaker(bind=engine)
session = Session()

# Foydalanuvchilarni olish (agar 100 dan kam bo‘lsa, faqat mavjudlarini ishlatadi)
users = session.query(User).limit(100).all()

cards = []
for user in users:
    card_number = fake.unique.credit_card_number()
    balance = round(random.uniform(50.0, 10000.0), 2)
    is_blocked = random.choice([False, False, False, True])  # kamdan-kam bloklanadi

    card = Card(
        user_id=user.id,
        card_number=card_number,
        balance=balance,
        is_blocked=is_blocked
    )
    cards.append(card)

# Malumotlarni saqlash
session.bulk_save_objects(cards)
session.commit()
print(f"✅ {len(cards)} ta karta yozildi.")
