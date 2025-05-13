import os
import sys
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# root papkani sys.path ga qo‘shamiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schema import Base, Transaction, Card  # schema dan model import qilish

# Bazaga ulanish (SQLite fayl bazasi bilan)
engine = create_engine("sqlite:///TZB.db")
Session = sessionmaker(bind=engine)
session = Session()

# Misol: oxirgi 7 kun ichidagi transactionlar soni
one_week_ago = datetime.utcnow() - timedelta(days=7)

count = session.query(func.count(Transaction.id)).filter(Transaction.timestamp >= one_week_ago).scalar()
print(f"Oxirgi 7 kun ichidagi transactionlar soni: {count}")
