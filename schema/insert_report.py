# insert_reports.py

import os
import sys
import random
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker

# Loyihaning ildiz papkasini sys.path ga qo‘shamiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schema import Base, Report, User  # User kerak bo‘ladi user_id olish uchun

fake = Faker()

# SQLite bazaga ulanish
engine = create_engine("sqlite:///TZB.db")
Session = sessionmaker(bind=engine)
session = Session()

# Mavjud foydalanuvchilarni olish
users = session.query(User).all()
if not users:
    print("❌ Report yaratish uchun kamida 1 ta foydalanuvchi kerak.")
    exit()

reports = []

for _ in range(100):
    user = random.choice(users)
    month = fake.month_name()
    report_text = fake.text(max_nb_chars=250)

    report = Report(
        user_id=user.id,
        month=month,
        report_text=report_text
    )
    reports.append(report)

# Saqlash
session.bulk_save_objects(reports)
session.commit()
print(f"✅ {len(reports)} ta report yozuvi yaratildi.")
