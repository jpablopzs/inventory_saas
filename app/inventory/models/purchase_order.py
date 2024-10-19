from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, UniqueConstraint, Integer, Numeric
from datetime import datetime
from app.core.database import Base

class Supplier(Base):
    __tablename__ = 'supplier'
    __table_args__ = (
        UniqueConstraint('tax_id','company_id', name='uq_tax_id'),
        UniqueConstraint('email','company_id', name='uq_supplier_email')  
    )
    
    id = Column((Integer), primary_key=True)
    company_id = Column((Integer), ForeignKey("company.id", name='fk_company_id'), nullable=False, index=True)
    name = Column(String(300), nullable=False)
    tax_id = Column(String(20), nullable=False)
    phone = Column(String(30), nullable=False)
    email = Column(String(100), index=True, nullable=False)
    tax_address = Column(String(300), nullable=True)
    create_at = Column(DateTime, nullable=False, default=datetime.now)
    update_at = Column(DateTime, nullable=True, default=datetime.now)
    is_deleted = Column(Boolean, default=False)

class PurchaseOrder(Base):
    __tablename__ = 'purchase_order'
    __table_args__ = (
        UniqueConstraint('order_code','company_id', name='uq_order_code_id'),
    )    
    id = Column((Integer), primary_key=True)
    company_id = Column((Integer), ForeignKey("company.id", name='fk_company_id'), nullable=False, index=True)
    sumpplier_id = Column((Integer), ForeignKey("supplier.id", name='fk_supplier_id'), nullable=False, index=True)
    order_code = Column(String(300), nullable=False)
    order_description = Column(String(300), nullable=True)
    invoice_number = Column(String(50), nullable=True)
    order_date = Column(DateTime, nullable=True)
    delivery_date = Column(DateTime, nullable=True)
    create_at = Column(DateTime, nullable=False, default=datetime.now)
    update_at = Column(DateTime, nullable=True, default=datetime.now)
    is_deleted = Column(Boolean, default=False)

class PurchaseOrderDetail(Base):
    __tablename__ = 'purchase_detail'
  
    id = Column((Integer), primary_key=True)
    company_id = Column((Integer), ForeignKey("company.id", name='fk_company_id'), nullable=False, index=True)
    product_id = Column((Integer), ForeignKey("product.id", name='fk_product_id'), nullable=False, index=True)
    sales_order_id = Column((Integer), ForeignKey("purchase_order.id", name='fk_purchase_order_id'), nullable=False, index=True)
    product_quantity = Column((Integer), nullable=False)
    unit_price = Column(Numeric, nullable=False)
    total_price = Column(Numeric, nullable=False)
    create_at = Column(DateTime, nullable=False, default=datetime.now)
    update_at = Column(DateTime, nullable=True, default=datetime.now)
    is_deleted = Column(Boolean, default=False)
