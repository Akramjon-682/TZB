# insert_vip_users.py

import os
import sys
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker

# Loyihaning ildiz papkasini sys.path ga qo‘shamiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schema import Base, User, VipUser

fake = Faker()

# SQLite bazaga ulanish
engine = create_engine("sqlite:///TZB.db")
Session = sessionmaker(bind=engine)
session = Session()

# Barcha foydalanuvchilarni olish
users = session.query(User).all()
if len(users) < 100:
    print("❌ Kamida 100 ta user kerak.")
    exit()

# Unikal user_id larni tanlaymiz (VIP bo‘lishi uchun user_id unique bo‘lishi kerak)
selected_users = random.sample(users, 100)

vip_users = []

for user in selected_users:
    vip = VipUser(
        user_id=user.id,
        assigned_by=fake.name(),
        assigned_at=fake.date_time_between(start_date='-1y', end_date='now')
    )
    vip_users.append(vip)

# Saqlash
session.bulk_save_objects(vip_users)
session.commit()
print(f"✅ {len(vip_users)} ta VipUser yozuvi yaratildi.")
