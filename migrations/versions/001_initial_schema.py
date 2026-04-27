"""initial schema - members and inventory tables

Revision ID: 001
Create Date: 2026-04-27
"""
from alembic import op
import sqlalchemy as sa

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "members",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String(120), unique=True, nullable=False),
        sa.Column("name", sa.String(80), nullable=False),
        sa.Column("tier", sa.String(20), server_default="basic"),
        sa.Column("active", sa.Boolean, server_default=sa.text("1")),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_table(
        "inventory",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("sku", sa.String(50), unique=True, nullable=False),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("quantity", sa.Integer, server_default=sa.text("0")),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("category", sa.String(50)),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )


def downgrade():
    op.drop_table("inventory")
    op.drop_table("members")
