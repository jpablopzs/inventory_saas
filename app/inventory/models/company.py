from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, UniqueConstraint, Integer
from datetime import datetime
from app.core.database import Base


class Company(Base):
    __tablename__ = 'company'
    __table_args__ = (
        UniqueConstraint('tax_id', name='uq_txt_id'),
        UniqueConstraint('email', name='uq_company_email')  
    )

    id = Column((Integer), primary_key=True)
    name = Column(String(300), nullable=False)
    tax_id = Column(String(20), nullable=False)
    phone = Column(String(30), nullable=False)
    email = Column(String(100), index=True, nullable=False)
    txt_address = Column(String(300), nullable=False)
    create_at = Column(DateTime, nullable=False, default=datetime.now)
    update_at = Column(DateTime, nullable=True, default=datetime.now)
    is_deleted = Column(Boolean, default=False)

class CompanyUser(Base):
    __tablename__ = 'company_user'
    __table_args__ = (
        UniqueConstraint('company_id', 'user_id', name='uq_company_user'),
    )
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("company.id", name='fk_company_id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("auth.user.id", name='fk_user_id'), nullable=False, index=True)
    create_at = Column(DateTime, nullable=False, default=datetime.now)
    update_at = Column(DateTime, nullable=True, default=datetime.now)
    is_deleted = Column(Boolean, default=False)