"""add contract

Revision ID: 8970e1fafdea
Revises: 6e6b90368936
Create Date: 2024-11-02 19:46:11.209113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8970e1fafdea'
down_revision = '6e6b90368936'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contract',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('property_id', sa.Integer(), nullable=False),
    sa.Column('renter_id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('monthly_rent', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['property_id'], ['property.id'], ),
    sa.ForeignKeyConstraint(['renter_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contract')
    # ### end Alembic commands ###
