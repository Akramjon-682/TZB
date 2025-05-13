# insert_logs.py

import os
import sys
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker

# Loyihaning ildiz papkasini sys.path ga qo‘shamiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schema import Base, Log, User

fake = Faker()

# SQLite bazaga ulanish
engine = create_engine("sqlite:///TZB.db")
Session = sessionmaker(bind=engine)
session = Session()

# Barcha foydalanuvchilarni olish
users = session.query(User).all()
if len(users) < 1:
    print("❌ Foydalanuvchi ma'lumotlari mavjud emas.")
    exit()

# Har xil log action'lari
actions = [
    'User login', 'User logout', 'Transaction completed', 'Transaction failed', 
    'Card blocked', 'Scheduled payment added', 'Report generated', 'Fraud detected', 
    'User created', 'Card added', 'Card updated', 'Balance checked'
]

logs = []

for _ in range(100):
    user = random.choice(users)
    action = random.choice(actions)
    performed_by = user.full_name
    timestamp = fake.date_time_between(start_date='-1y', end_date='now')
    details = fake.text(max_nb_chars=200)

    log = Log(
        action=action,
        performed_by=performed_by,
        timestamp=timestamp,
        details=details
    )
    logs.append(log)

# Saqlash
session.bulk_save_objects(logs)
session.commit()
print(f"✅ {len(logs)} ta Log yozuvi yaratildi.")
