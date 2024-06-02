"""Create tables

Revision ID: b6aec9715b77
Revises: 
Create Date: 2023-03-15 09:01:14.786623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6aec9715b77'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create bakeries table
    op.create_table('bakeries',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    # Create baked_goods table
    op.create_table('baked_goods',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False, unique=True),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('bakery_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['bakery_id'], ['bakeries.id'], name='fk_baked_goods_bakery_id_bakeries')
    )

    # Add index on bakery_id column in baked_goods table
    op.create_index('idx_baked_goods_bakery_id', 'baked_goods', ['bakery_id'])


def downgrade():
    # Drop baked_goods table
    op.drop_table('baked_goods')

    # Drop bakeries table
    op.drop_table('bakeries')
