import os
import sys
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# Root papkani sys.path ga qo‘shamiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schema import Base, Transaction, Card  # schema dan model import qilish

# Bazaga ulanish (SQLite fayl bazasi bilan)
engine = create_engine("sqlite:///TZB.db")
Session = sessionmaker(bind=engine)
session = Session()

# Misol: oxirgi 7 kun ichidagi yirik tranzaksiyalarni (150 mln so‘mdan oshgan) tekshirish
one_week_ago = datetime.utcnow() - timedelta(days=7)

# Yirik tranzaksiyalarni olish
large_transactions = session.query(Transaction).filter(
    Transaction.timestamp >= one_week_ago,
    Transaction.amount > 150_000_000  # 150 million so‘mdan oshgan tranzaksiyalar
).all()

print(f"Oxirgi 7 kun ichidagi yirik tranzaksiyalar (150 million so‘mdan oshgan):")
for transaction in large_transactions:
    print(f"Tranzaksiya ID: {transaction.id}, Miktor: {transaction.amount} UZS, "
          f"Yuboruvchi Karta: {transaction.sender_card_id}, "
          f"Qabul qiluvchi Karta: {transaction.receiver_card_id}, "
          f"Vaqti: {transaction.timestamp}")
