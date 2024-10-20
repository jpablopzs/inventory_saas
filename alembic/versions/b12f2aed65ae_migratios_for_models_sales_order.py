"""migratios for models sales order

Revision ID: b12f2aed65ae
Revises: 18c0dbcaa7b9
Create Date: 2024-10-18 04:00:13.651464

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b12f2aed65ae'
down_revision: Union[str, None] = '18c0dbcaa7b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=300), nullable=False),
    sa.Column('dni', sa.String(length=20), nullable=False),
    sa.Column('phone', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('address', sa.String(length=300), nullable=True),
    sa.Column('create_at', sa.DateTime(), nullable=False),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], name='fk_company_id'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('dni', 'company_id', name='uq_dni_id')
    )
    op.create_index(op.f('ix_customer_company_id'), 'customer', ['company_id'], unique=False)
    op.create_index(op.f('ix_customer_email'), 'customer', ['email'], unique=False)
    op.create_table('sales_order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('order_number', sa.String(length=300), nullable=False),
    sa.Column('order_description', sa.String(length=300), nullable=True),
    sa.Column('invoice_number', sa.String(length=50), nullable=True),
    sa.Column('invoice_date', sa.DateTime(), nullable=True),
    sa.Column('delivery_address', sa.String(length=300), nullable=True),
    sa.Column('delivery_date', sa.DateTime(), nullable=True),
    sa.Column('create_at', sa.DateTime(), nullable=False),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], name='fk_company_id'),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], name='fk_customer_id'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('order_number', 'company_id', name='uq_order_number_id')
    )
    op.create_index(op.f('ix_sales_order_company_id'), 'sales_order', ['company_id'], unique=False)
    op.create_index(op.f('ix_sales_order_customer_id'), 'sales_order', ['customer_id'], unique=False)
    op.create_table('sales_order_detail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('sales_order_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('product_quantity', sa.Integer(), nullable=False),
    sa.Column('unit_price', sa.Numeric(), nullable=False),
    sa.Column('total_price', sa.Numeric(), nullable=False),
    sa.Column('create_at', sa.DateTime(), nullable=False),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], name='fk_company_id'),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], name='fk_product_id'),
    sa.ForeignKeyConstraint(['sales_order_id'], ['sales_order.id'], name='fk_sales_order_id'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sales_order_detail_company_id'), 'sales_order_detail', ['company_id'], unique=False)
    op.create_index(op.f('ix_sales_order_detail_product_id'), 'sales_order_detail', ['product_id'], unique=False)
    op.create_index(op.f('ix_sales_order_detail_purchase_order_id'), 'sales_order_detail', ['sales_order_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_sales_order_detail_purchase_order_id'), table_name='sales_order_detail')
    op.drop_index(op.f('ix_sales_order_detail_product_id'), table_name='sales_order_detail')
    op.drop_index(op.f('ix_sales_order_detail_company_id'), table_name='sales_order_detail')
    op.drop_table('sales_order_detail')
    op.drop_index(op.f('ix_sales_order_customer_id'), table_name='sales_order')
    op.drop_index(op.f('ix_sales_order_company_id'), table_name='sales_order')
    op.drop_table('sales_order')
    op.drop_index(op.f('ix_customer_email'), table_name='customer')
    op.drop_index(op.f('ix_customer_company_id'), table_name='customer')
    op.drop_table('customer')
    # ### end Alembic commands ###
