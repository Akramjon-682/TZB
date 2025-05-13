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

# Misol: oxirgi 30 kun ichidagi transactionlar soni
one_month_ago = datetime.utcnow() - timedelta(days=30)

count = session.query(func.count(Transaction.id)).filter(Transaction.timestamp >= one_month_ago).scalar()
print(f"Oxirgi 1 oy ichidagi transactionlar soni: {count}")
