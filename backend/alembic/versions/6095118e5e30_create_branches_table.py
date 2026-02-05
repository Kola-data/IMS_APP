"""create branches table safely

Revision ID: 6095118e5e30
Revises: 7f9e5fe3ce69
Create Date: 2026-02-02 13:01:37.013894
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6095118e5e30'
down_revision: Union[str, Sequence[str], None] = '7f9e5fe3ce69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # ===========================
    # 1️⃣ Create branches table
    # ===========================
    op.create_table(
        'branches',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('location', sa.String(length=500), nullable=False),
        sa.Column('branch_manager', sa.String(length=255), nullable=False),
        sa.Column('branch_contacts', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('company_id', sa.UUID(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # =========================================
    # 2️⃣ Add is_active & is_deleted to companies
    # =========================================

    # Step 1: Add columns as nullable
    op.add_column('companies', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.add_column('companies', sa.Column('is_deleted', sa.Boolean(), nullable=True))

    # Step 2: Fill existing rows
    op.execute("UPDATE companies SET is_active = TRUE")
    op.execute("UPDATE companies SET is_deleted = FALSE")

    # Step 3: Alter columns to NOT NULL
    op.alter_column('companies', 'is_active', nullable=False)
    op.alter_column('companies', 'is_deleted', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop the columns in reverse order
    op.drop_column('companies', 'is_deleted')
    op.drop_column('companies', 'is_active')
    op.drop_table('branches')
