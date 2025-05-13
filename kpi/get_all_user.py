import os
import sys
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# root papkani sys.path ga qo‘shamiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schema import Base, User, Transaction, Card  # model faylingizdan import qiling

# Bazaga ulanish (SQLite fayl bazasi bilan)
engine = create_engine("sqlite:///TZB.db")
Session = sessionmaker(bind=engine)
session = Session()

# 1. Barcha foydalanuvchilarni ko‘rish
def get_all_users(session):
    users = session.query(User).all()
    for user in users:
        print(f"ID: {user.id}, Name: {user.full_name}, Email: {user.email}")


# === Ishga tushirish uchun ===
if __name__ == "__main__":
    print("Barcha foydalanuvchilar:")
    get_all_users(session)


