from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, UniqueConstraint, Integer, Numeric
from datetime import datetime
from app.core.database import Base

class Customer(Base):
    __tablename__ = 'customer'
    __table_args__ = (
        UniqueConstraint('dni', 'company_id', name='uq_dni_id'),
    )
    
    id = Column((Integer), primary_key=True)
    company_id = Column((Integer), ForeignKey("company.id", name='fk_company_id'), nullable=False, index=True)
    name = Column(String(300), nullable=False)
    dni = Column(String(20), nullable=False)
    phone = Column(String(30), nullable=False)
    email = Column(String(100), index=True, nullable=False)
    address = Column(String(300), nullable=True)
    create_at = Column(DateTime, nullable=False, default=datetime.now)
    update_at = Column(DateTime, nullable=True, default=datetime.now)
    is_deleted = Column(Boolean, default=False)

class SalesOrder(Base):
    __tablename__ = 'sales_order'
    __table_args__ = (
        UniqueConstraint('order_number','company_id', name='uq_order_number_id'),
    )    
    id = Column((Integer), primary_key=True)
    company_id = Column((Integer), ForeignKey("company.id", name='fk_company_id'), nullable=False, index=True)
    customer_id = Column((Integer), ForeignKey("customer.id", name='fk_customer_id'), nullable=False, index=True)
    order_number = Column(String(300), nullable=False)
    order_description = Column(String(300), nullable=True)
    invoice_number = Column(String(50), nullable=True)
    invoice_date = Column(DateTime, nullable=True)
    delivery_address = Column(String(300), nullable=True)
    delivery_date = Column(DateTime, nullable=True)
    create_at = Column(DateTime, nullable=False, default=datetime.now)
    update_at = Column(DateTime, nullable=True, default=datetime.now)
    is_deleted = Column(Boolean, default=False)

class SalesOrderDetail(Base):
    __tablename__ = 'sales_order_detail'
 
    id = Column((Integer), primary_key=True)
    company_id = Column((Integer), ForeignKey("company.id", name='fk_company_id'), nullable=False, index=True)
    sales_order_id = Column((Integer), ForeignKey("sales_order.id", name='fk_sales_order_id'), nullable=False, index=True)
    product_id = Column((Integer), ForeignKey("product.id", name='fk_product_id'), nullable=False, index=True)
    product_quantity = Column((Integer), nullable=False)
    unit_price = Column(Numeric, nullable=False)
    total_price = Column(Numeric, nullable=False)
    create_at = Column(DateTime, nullable=False, default=datetime.now)
    update_at = Column(DateTime, nullable=True, default=datetime.now)
    is_deleted = Column(Boolean, default=False)
