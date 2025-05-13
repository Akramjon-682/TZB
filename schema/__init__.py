from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, create_engine, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

# ------------------------- User Table -------------------------
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone_number = Column(String(20), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    cards = relationship("Card", back_populates="user")
    reports = relationship("Report", back_populates="user")
    scheduled_payments = relationship("ScheduledPayment", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, name={self.full_name})>"

# ------------------------- Card Table -------------------------
class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    card_number = Column(String(20), unique=True, nullable=False)
    balance = Column(Float, default=0.0)
    is_blocked = Column(Boolean, default=False)

    user = relationship("User", back_populates="cards")
    transactions_sent = relationship("Transaction", back_populates="from_card", foreign_keys='Transaction.from_card_id')
    transactions_received = relationship("Transaction", back_populates="to_card", foreign_keys='Transaction.to_card_id')

    def __repr__(self):
        return f"<Card(id={self.id}, number={self.card_number})>"

# ------------------------- Transaction Table -------------------------
class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    from_card_id = Column(Integer, ForeignKey('cards.id'))
    to_card_id = Column(Integer, ForeignKey('cards.id'))
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default='completed')  # completed, failed, pending

    from_card = relationship("Card", foreign_keys=[from_card_id], back_populates="transactions_sent")
    to_card = relationship("Card", foreign_keys=[to_card_id], back_populates="transactions_received")

    def __repr__(self):
        return f"<Transaction(id={self.id}, amount={self.amount})>"

# ------------------------- Report Table -------------------------
class Report(Base):
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    month = Column(String(20))
    report_text = Column(Text)

    user = relationship("User", back_populates="reports")

    def __repr__(self):
        return f"<Report(id={self.id}, month={self.month})>"

# ------------------------- Scheduled Payment Table -------------------------
class ScheduledPayment(Base):
    __tablename__ = 'scheduled_payments'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    card_id = Column(Integer, ForeignKey('cards.id'))
    amount = Column(Float, nullable=False)
    schedule_date = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="scheduled_payments")
    card = relationship("Card")

    def __repr__(self):
        return f"<ScheduledPayment(id={self.id}, amount={self.amount})>"

# ------------------------- Fraud Detection Table -------------------------
class FraudDetection(Base):
    __tablename__ = 'fraud_detection'

    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'))
    reason = Column(String(200))
    detected_at = Column(DateTime, default=datetime.utcnow)

    transaction = relationship("Transaction")

    def __repr__(self):
        return f"<FraudDetection(id={self.id}, reason={self.reason})>"

# ------------------------- VIP User Table -------------------------
class VipUser(Base):
    __tablename__ = 'vip_users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    assigned_by = Column(String(100))
    assigned_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")

    def __repr__(self):
        return f"<VipUser(user_id={self.user_id})>"

# ------------------------- Blocked User Table -------------------------
class BlockedUser(Base):
    __tablename__ = 'blocked_users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    reason = Column(String(200))
    blocked_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")

    def __repr__(self):
        return f"<BlockedUser(user_id={self.user_id})>"

# ------------------------- Log Table -------------------------
class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    action = Column(String(100))
    performed_by = Column(String(100))
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(Text)

    def __repr__(self):
        return f"<Log(action={self.action})>"

# ------------------------- DB Create Function -------------------------
def create_tables(engine):
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    engine = create_engine("sqlite:///TZB.db")
    create_tables(engine)