from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, UniqueConstraint, Integer, Numeric
from datetime import datetime
from app.core.database import Base

from datetime import datetime

class Category(Base):
    __tablename__ = 'category'
    __table_args__ = (
        UniqueConstraint('name', 'company_id', name='uq_category_name'),
    )
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("company.id", name='fk_company_id'), nullable=False, index=True)
    name = Column(String(300), nullable=False)
    description = Column(String(300), nullable=True)
    create_at = Column(DateTime, nullable=False, default=datetime.now)
    update_at = Column(DateTime, nullable=True, default=datetime.now)
    is_deleted = Column(Boolean, default=False)

class Product(Base):
    __tablename__ = 'product'
    __table_args__ = (
        UniqueConstraint('product_code', 'company_id', name='uq_product_code'),
    )
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("company.id", name='fk_company_id'), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("category.id", name='fk_category_id'), nullable=False, index=True)
    product_code = Column(String(40), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    description = Column(String(300), nullable=True)
    current_price = Column(Numeric, nullable=True)
    stock_quantity = Column(Integer, nullable=True)
    create_at = Column(DateTime, nullable=False, default=datetime.now)
    update_at = Column(DateTime, nullable=True, default=datetime.now)
    is_deleted = Column(Boolean, default=False)
