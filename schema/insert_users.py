import os
import sys
import random
from datetime import datetime
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Root papkani sys.path ga qo‘shamiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schema import Base, User  # schema/__init__.py dan import qilinadi

# Faker kutubxonasini chaqiramiz
fake = Faker()

# SQLite bazaga ulanamiz
engine = create_engine("sqlite:///TZB.db")
Session = sessionmaker(bind=engine)
session = Session()

# 100 ta foydalanuvchi generatsiya qilamiz
users = []
for _ in range(100):
    full_name = fake.name()
    email = fake.unique.email()
    phone_number = fake.unique.phone_number()
    user = User(
        full_name=full_name,
        email=email,
        phone_number=phone_number,
        created_at=datetime.utcnow()
    )
    users.append(user)

# Bulk insert
session.bulk_save_objects(users)
session.commit()
print("✅ 100 ta foydalanuvchi muvaffaqiyatli qo‘shildi.")
