import os
import sys
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# Root papkani sys.path ga qo‘shamiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schema import Base, User, Card  # kerakli modellarni import qilamiz

# Bazaga ulanish (SQLite fayl bazasi bilan)
engine = create_engine("sqlite:///TZB.db")
Session = sessionmaker(bind=engine)
session = Session()

# Har bir foydalanuvchining umumiy balansini chiqaramiz
users = session.query(User).all()

for user in users:
    total_balance = sum(card.balance for card in user.cards)  # user.cards orqali kartalarini olyapmiz
    print(f"Foydalanuvchi: {user.full_name}, Jami balans: {total_balance} UZS")
