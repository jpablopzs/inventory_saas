from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, UniqueConstraint, Integer
from datetime import datetime
from app.core.database import Base


class User(Base):
    __tablename__ = 'user'
    __table_args__ = (
        UniqueConstraint('email', name='uq_email'),
        UniqueConstraint('username', name='uq_username'),
        {'schema': 'auth'}
        
    )
    id = Column((Integer), primary_key=True)
    name = Column(String(150), nullable=False)
    username = Column(String(50), nullable=False)
    phone = Column(String(30), nullable=False)
    email = Column(String(100), index=True, nullable=False)
    password = Column(String(300), nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    update_at = Column(DateTime, nullable=False, default=datetime.now)
    create_at = Column(DateTime, nullable=False, default=datetime.now)
