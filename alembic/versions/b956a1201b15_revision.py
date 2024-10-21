"""revision

Revision ID: b956a1201b15
Revises: 8a94f6dde329
Create Date: 2024-10-19 13:56:18.033855

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b956a1201b15'
down_revision: Union[str, None] = '8a94f6dde329'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('purchase_order_detail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('purchase_order_id', sa.Integer(), nullable=False),
    sa.Column('product_quantity', sa.Integer(), nullable=False),
    sa.Column('unit_price', sa.Numeric(), nullable=False),
    sa.Column('total_price', sa.Numeric(), nullable=False),
    sa.Column('create_at', sa.DateTime(), nullable=False),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], name='fk_company_id'),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], name='fk_product_id'),
    sa.ForeignKeyConstraint(['purchase_order_id'], ['purchase_order.id'], name='fk_purchase_order_id'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_purchase_order_detail_company_id'), 'purchase_order_detail', ['company_id'], unique=False)
    op.create_index(op.f('ix_purchase_order_detail_product_id'), 'purchase_order_detail', ['product_id'], unique=False)
    op.create_index(op.f('ix_purchase_order_detail_purchase_order_id'), 'purchase_order_detail', ['purchase_order_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_purchase_order_detail_purchase_order_id'), table_name='purchase_order_detail')
    op.drop_index(op.f('ix_purchase_order_detail_product_id'), table_name='purchase_order_detail')
    op.drop_index(op.f('ix_purchase_order_detail_company_id'), table_name='purchase_order_detail')
    op.drop_table('purchase_order_detail')
    # ### end Alembic commands ###
