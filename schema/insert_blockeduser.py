# insert_blocked_users.py

import os
import sys
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker

# Loyihaning ildiz papkasini sys.path ga qo‘shamiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schema import Base, User, BlockedUser

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

# Unikal user_id larni tanlaymiz (BlockedUser bo‘lishi uchun user_id kerak)
selected_users = random.sample(users, 100)

blocked_users = []

for user in selected_users:
    blocked_user = BlockedUser(
        user_id=user.id,
        reason=fake.sentence(nb_words=6),
        blocked_at=fake.date_time_between(start_date='-1y', end_date='now')
    )
    blocked_users.append(blocked_user)

# Saqlash
session.bulk_save_objects(blocked_users)
session.commit()
print(f"✅ {len(blocked_users)} ta BlockedUser yozuvi yaratildi.")
