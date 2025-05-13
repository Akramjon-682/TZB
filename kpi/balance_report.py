import os
import sys
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Root papkani sys.path ga qo‘shamiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schema import Base, User, Card, Transaction

# Bazaga ulanish
engine = create_engine("sqlite:///TZB.db")
Session = sessionmaker(bind=engine)
session = Session()


# 💸 Pul qo‘shish funksiyasi
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


# 💸 Pul yechish funksiyasi
def withdraw_money(card, amount):
    if card.balance >= amount:
        card.balance -= amount
        transaction = Transaction(
            from_card_id=card.id,
            to_card_id=None,
            amount=amount,
            timestamp=datetime.utcnow()
        )
        session.add(transaction)
        session.commit()
        print(f"   ➖ {amount} UZS yechildi ← Karta: {card.card_number}")
    else:
        print(f"   ⚠️ {card.card_number} da yetarli mablag‘ yo‘q (so‘ralgan: {amount}, mavjud: {card.balance})")


# 📜 Tranzaksiya tarixini chiqarish
def show_transaction_history(card):
    print(f"     📜 Tranzaksiya tarixi: {card.card_number}")
    transactions = session.query(Transaction).filter(
        (Transaction.to_card_id == card.id) | (Transaction.from_card_id == card.id)
    ).order_by(Transaction.timestamp.desc()).all()

    if not transactions:
        print("        ⚠️ Tranzaksiya mavjud emas")
        return

    for t in transactions:
        if t.to_card_id == card.id and t.from_card_id:
            direction = f"⬅️ Qabul qilingan {t.amount} UZS"
        elif t.from_card_id == card.id and t.to_card_id:
            direction = f"➡️ Yuborilgan {t.amount} UZS"
        elif t.to_card_id == card.id:
            direction = f"➕ Depozit {t.amount} UZS"
        elif t.from_card_id == card.id:
            direction = f"➖ Pul yechish {t.amount} UZS"
        else:
            direction = f"🔄 Noma’lum yo‘nalish {t.amount} UZS"

        print(f"        📅 {t.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | {direction}")


# 🔍 O‘rtacha balans va eng ko‘p tranzaksiya qilgan foydalanuvchini aniqlash
def analyze_balances_and_transactions():
    print("\n📊 BALANS TAHLILI:")

    users = session.query(User).all()
    user_balances = []
    user_transaction_counts = {}

    for user in users:
        if user.cards:
            total = sum(card.balance for card in user.cards)
            count = len(user.cards)
            avg_balance = total / count
            user_balances.append((user.full_name, avg_balance))
            print(f"   👤 {user.full_name} | 🧮 O‘rtacha balans: {avg_balance:.2f} UZS")

            # Tranzaksiya sonini hisoblash
            transaction_count = 0
            for card in user.cards:
                count1 = session.query(Transaction).filter(Transaction.to_card_id == card.id).count()
                count2 = session.query(Transaction).filter(Transaction.from_card_id == card.id).count()
                transaction_count += (count1 + count2)

            user_transaction_counts[user.full_name] = transaction_count

    # Eng ko‘p tranzaksiya qilgan foydalanuvchi
    if user_transaction_counts:
        most_active_user = max(user_transaction_counts, key=user_transaction_counts.get)
        print(f"\n🏆 Eng ko‘p tranzaksiya qilgan foydalanuvchi: {most_active_user} ({user_transaction_counts[most_active_user]} ta)")
    else:
        print("❌ Tranzaksiyalar topilmadi.")


# === ASOSIY BAJARILADIGAN QISM ===
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

        deposit_money(card, 100)
        withdraw_money(card, 50)
        show_transaction_history(card)

# Statistik tahlilni chaqiramiz
analyze_balances_and_transactions()
