"""Add pricing configuration table

Revision ID: 002_add_pricing_config
Revises: 001_add_additional_data_to_pending_users
Create Date: 2026-02-06 17:50:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid
from datetime import datetime, timezone

# revision identifiers, used by Alembic.
revision = '002_add_pricing_config'
down_revision = '001_add_additional_data_to_pending_users'
branch_labels = None
depends_on = None


def upgrade():
    # Create pricing_config table
    op.create_table(
        'core_mstr_one_qlick_pricing_config_tbl',
        sa.Column('config_id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('config_key', sa.String(100), unique=True, nullable=False),
        sa.Column('config_value', sa.Numeric(10, 2), nullable=False),
        sa.Column('config_type', sa.String(50), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('is_active', sa.Boolean, default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    
    # Create index on config_key
    op.create_index('idx_pricing_config_key', 'core_mstr_one_qlick_pricing_config_tbl', ['config_key'])
    
    # Insert default pricing configuration
    # Note: Using raw SQL for UUID generation compatibility
    op.execute("""
        INSERT INTO core_mstr_one_qlick_pricing_config_tbl 
        (config_id, config_key, config_value, config_type, description, is_active, created_at, updated_at) 
        VALUES
        (gen_random_uuid(), 'platform_fee_type', 1, 'fixed', 'Platform fee type: 0=percentage, 1=fixed', true, now(), now()),
        (gen_random_uuid(), 'platform_fee_value', 5.00, 'fixed', 'Platform fee value (₹5 fixed or percentage)', true, now(), now()),
        (gen_random_uuid(), 'tax_rate', 5.00, 'percentage', 'GST/Tax rate in percentage', true, now(), now()),
        (gen_random_uuid(), 'free_delivery_threshold', 199.00, 'threshold', 'Minimum order amount for free delivery', true, now(), now()),
        (gen_random_uuid(), 'delivery_base_fee', 20.00, 'fixed', 'Base delivery fee (0-2 km)', true, now(), now()),
        (gen_random_uuid(), 'delivery_fee_2_5km', 5.00, 'fixed', 'Additional fee per km for 2-5 km range', true, now(), now()),
        (gen_random_uuid(), 'delivery_fee_5_10km', 8.00, 'fixed', 'Additional fee per km for 5-10 km range', true, now(), now()),
        (gen_random_uuid(), 'delivery_fee_10plus_km', 10.00, 'fixed', 'Additional fee per km for 10+ km range', true, now(), now())
    """)


def downgrade():
    op.drop_index('idx_pricing_config_key', table_name='core_mstr_one_qlick_pricing_config_tbl')
    op.drop_table('core_mstr_one_qlick_pricing_config_tbl')
