import os
import sys
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker

# Loyihaning ildiz papkasini sys.path ga qo‘shamiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schema import Base, Card, Transaction

fake = Faker()

# SQLite bazaga ulanish
engine = create_engine("sqlite:///TZB.db")
Session = sessionmaker(bind=engine)
session = Session()

# Barcha kartalarni olish
cards = session.query(Card).all()
if len(cards) < 2:
    print("❌ Tranzaksiya yaratish uchun kamida 2 ta karta kerak.")
    exit()

transactions = []

for _ in range(100):
    from_card, to_card = random.sample(cards, 2)  # Ikkita turli karta tanlaymiz
    amount = round(random.uniform(10.0, 500.0), 2)
    timestamp = fake.date_time_between(start_date='-1y', end_date='now')
    status = random.choice(['completed'] * 8 + ['pending', 'failed'])  # Ko‘pchiligi completed

    transaction = Transaction(
        from_card_id=from_card.id,
        to_card_id=to_card.id,
        amount=amount,
        timestamp=timestamp,
        status=status
    )
    transactions.append(transaction)

# Saqlash
session.bulk_save_objects(transactions)
session.commit()
print(f"✅ {len(transactions)} ta tranzaksiya yozildi.")
