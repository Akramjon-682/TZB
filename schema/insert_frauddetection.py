# insert_fraud_detection.py

import os
import sys
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker

# Loyihaning ildiz papkasini sys.path ga qo‘shamiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schema import Base, Transaction, FraudDetection

fake = Faker()

# Bazaga ulanish
engine = create_engine("sqlite:///TZB.db")
Session = sessionmaker(bind=engine)
session = Session()

# Barcha tranzaksiyalarni olish
transactions = session.query(Transaction).all()
if not transactions:
    print("❌ FraudDetection uchun hech qanday tranzaksiya topilmadi.")
    exit()

fraud_records = []

for _ in range(100):
    transaction = random.choice(transactions)
    reason = random.choice([
        "Shubhali miqdor",
        "IP manzil mos emas",
        "Qayta urinishlar ko‘p",
        "Blacklisted karta",
        "Limitdan oshib ketdi",
        "G‘ayrioddiy vaqt",
        "Tizimda xatolik",
        "Yangi qurilmadan urinish"
    ])
    detected_at = fake.date_time_between(start_date=transaction.timestamp, end_date='now')

    fraud = FraudDetection(
        transaction_id=transaction.id,
        reason=reason,
        detected_at=detected_at
    )
    fraud_records.append(fraud)

# Saqlash
session.bulk_save_objects(fraud_records)
session.commit()
print(f"✅ {len(fraud_records)} ta FraudDetection yozuvi yaratildi.")
