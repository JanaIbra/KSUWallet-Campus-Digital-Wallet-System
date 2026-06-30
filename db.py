from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime
Base = declarative_base()

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True)
    student_id = Column(String(10), unique=True)
    name = Column(String(50))
    password = Column(String(50))
    email = Column(String(100))
    phone = Column(String(15))
    wallet_number = Column(String(10), unique=True)
    wallet_type = Column(String(10))  # student / admin / KSU
    balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.now)

engine = create_engine("sqlite:///ksuwallet.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
admin = session.query(Wallet).filter_by(wallet_type="admin").first()
if not admin:
    new_admin = Wallet(
        student_id="0000000000",
        name="Admin",
        password="admin123",
        email="admin@ksu.edu.sa",
        phone="0500000000",
        wallet_number="9999999999",
        wallet_type="admin",
        balance=0,
        created_at=datetime.datetime.now()
    )
    session.add(new_admin)
    session.commit()