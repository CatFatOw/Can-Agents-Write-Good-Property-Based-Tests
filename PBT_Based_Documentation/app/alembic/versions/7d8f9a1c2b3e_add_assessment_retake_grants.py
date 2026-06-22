"""add assessment retake grants

Revision ID: 7d8f9a1c2b3e
Revises: f50a94890b75
Create Date: 2026-06-21 23:50:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7d8f9a1c2b3e"
down_revision: Union[str, Sequence[str], None] = "f50a94890b75"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "assessment_retake_grants",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("documentation_id", sa.Integer(), nullable=False),
        sa.Column("allow_all_users", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("user_email", sa.Text(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["created_by"], ["user.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["documentation_id"], ["documentation.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("assessment_retake_grants")
