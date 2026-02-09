"""Add additional_data column to pending_users table

Revision ID: add_additional_data_to_pending_users
Revises: 
Create Date: 2026-01-05

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_additional_data_to_pending_users'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add additional_data column to pending_users table
    op.add_column('core_mstr_one_qlick_pending_users_tbl', 
                  sa.Column('additional_data', sa.String(), nullable=True))


def downgrade():
    # Remove additional_data column
    op.drop_column('core_mstr_one_qlick_pending_users_tbl', 'additional_data')
