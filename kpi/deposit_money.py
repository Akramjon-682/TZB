import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Root papkani sys.path ga qo‘shamiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schema import Base, User, Card, Transaction  # kerakli modellar

# Bazaga ulanish (SQLite)
engine = create_engine("sqlite:///TZB.db")
Session = sessionmaker(bind=engine)
session = Session()

# Pul qo‘shish funksiyasi
def deposit_money(card, amount):
    card.balance += amount
    transaction = Transaction(
        from_card_id=None,
        to_card_id=card.id,
        amount=amount,
        timestamp=datetime.utcnow()
    )
    session.add(transaction)
    session.commit()
    print(f"   ➕ {amount} UZS depozit qilindi → Karta: {card.card_number}")




# Pul yechish funksiyasi
def withdraw_money(card, amount):
    if card.balance >= amount:
        card.balance -= amount
        transaction = Transaction(
        from_card_id=None,
        to_card_id=card.id,
        amount=amount,
        timestamp=datetime.utcnow()
    )
        session.add(transaction)
        session.commit()
        print(f"   ➖ {amount} UZS yechildi ← Karta: {card.card_number}")
    else:
        print(f"   ⚠️ {card.card_number} da yetarli mablag‘ yo‘q (so‘ralgan: {amount}, mavjud: {card.balance})")

# Har bir foydalanuvchining kartalari bo‘yicha balansni chiqarish va operatsiya qilish
users = session.query(User).all()

for user in users:
    print(f"\n👤 Foydalanuvchi: {user.full_name}")

    if not user.cards:
        print("   ⚠️ Karta mavjud emas")
        continue

    total_balance = sum(card.balance for card in user.cards)
    print(f"   💰 Umumiy balans: {total_balance} UZS")

    for card in user.cards:
        print(f"     📄 Karta: {card.card_number} | Balans: {card.balance} UZS")

        # Misol tariqasida har bir karta bo‘yicha avtomatik deposit va withdraw qilamiz
        deposit_money(card, 100)     # 100 qo‘shamiz
        withdraw_money(card, 50)     # 50  yechamiz


