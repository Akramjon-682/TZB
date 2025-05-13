# insert_scheduled_payments.py

import os
import sys
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker

# Loyihaning ildiz papkasini sys.path ga qo‘shamiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schema import Base, ScheduledPayment, User, Card

fake = Faker()

# SQLite bazaga ulanish
engine = create_engine("sqlite:///TZB.db")
Session = sessionmaker(bind=engine)
session = Session()

# Foydalanuvchilar va kartalarni olish
users = session.query(User).all()
cards = session.query(Card).all()

if not users or not cards:
    print("❌ ScheduledPayment yozish uchun foydalanuvchi va karta kerak.")
    exit()

scheduled_payments = []

for _ in range(100):
    user = random.choice(users)
    user_cards = [card for card in cards if card.user_id == user.id]

    if not user_cards:
        continue  # foydalanuvchining kartasi yo‘q bo‘lsa, o‘tkazib yuboramiz

    card = random.choice(user_cards)
    amount = round(random.uniform(20.0, 1000.0), 2)
    schedule_date = datetime.now() + timedelta(days=random.randint(1, 90))

    payment = ScheduledPayment(
        user_id=user.id,
        card_id=card.id,
        amount=amount,
        schedule_date=schedule_date
    )
    scheduled_payments.append(payment)

# Saqlash
session.bulk_save_objects(scheduled_payments)
session.commit()
print(f"✅ {len(scheduled_payments)} ta ScheduledPayment yozuvi yaratildi.")
