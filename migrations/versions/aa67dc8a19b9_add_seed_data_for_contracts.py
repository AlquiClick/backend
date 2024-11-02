"""Add seed data for Contracts

Revision ID: aa67dc8a19b9
Revises: 8970e1fafdea
Create Date: 2024-11-02 19:50:45.852016

"""
from alembic import op
from datetime import date
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa67dc8a19b9'
down_revision = '8970e1fafdea'
branch_labels = None
depends_on = None


def upgrade():
    op.bulk_insert(
    sa.table('contract',
        sa.Column('property_id', sa.Integer),
        sa.Column('renter_id', sa.Integer),
        sa.Column('owner_id', sa.Integer),
        sa.Column('start_date', sa.Date),
        sa.Column('end_date', sa.Date),
        sa.Column('monthly_rent', sa.Numeric),
        sa.Column('status', sa.Boolean)
    ),
    [
        {'property_id': 1, 'renter_id': 2, 'owner_id': 1, 'start_date': date(2023, 1, 1), 'end_date': date(2024, 1, 1), 'monthly_rent': 1500.00, 'status': True},
        {'property_id': 2, 'renter_id': 3, 'owner_id': 2, 'start_date': date(2023, 2, 1), 'end_date': date(2024, 2, 1), 'monthly_rent': 2000.00, 'status': True},
        {'property_id': 3, 'renter_id': 4, 'owner_id': 3, 'start_date': date(2023, 3, 1), 'end_date': date(2024, 3, 1), 'monthly_rent': 1200.00, 'status': True},
        {'property_id': 4, 'renter_id': 1, 'owner_id': 4, 'start_date': date(2023, 4, 1), 'end_date': date(2024, 4, 1), 'monthly_rent': 2500.00, 'status': True},
    ]
)


def downgrade():
    op.execute("DELETE FROM contract WHERE id BETWEEN 1 AND 4")
