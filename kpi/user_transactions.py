import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# sys.path ga root papkani qo‘shish
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schema import Base, Card, Transaction  # kerakli modellarni import qilamiz

# Bazaga ulanish (SQLite)
engine = create_engine("sqlite:///TZB.db")
Session = sessionmaker(bind=engine)  
session = Session()

def transfer_money(from_card_number, to_card_number, amount):
    # Kartalarni bazadan olish
    from_card = session.query(Card).filter_by(card_number=from_card_number).first()
    to_card = session.query(Card).filter_by(card_number=to_card_number).first()

    # Tekshiruvlar
    if not from_card or not to_card:
        print("Karta topilmadi.")
        return

    if from_card.balance < amount:
        print("Yetarli mablag' mavjud emas.")
        return

    # Balanslarni yangilash
    from_card.balance -= amount
    to_card.balance += amount

    # Tranzaksiyani yozish
    transaction = Transaction(
        sender_card_id=from_card.id,
        receiver_card_id=to_card.id,
        amount=amount,
        timestamp=datetime.utcnow()
    )

    session.add(transaction)
    session.commit()
    print(f"{amount} UZS muvaffaqiyatli o‘tkazildi: {from_card_number} → {to_card_number}")

# Foydalanish misoli
transfer_money("########", "########", 500)
