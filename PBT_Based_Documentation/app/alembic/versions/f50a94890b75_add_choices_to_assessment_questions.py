"""add choices to assessment questions

Revision ID: f50a94890b75
Revises: 2b0047758102
Create Date: 2026-06-21 15:23:32.290531

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f50a94890b75'
down_revision: Union[str, Sequence[str], None] = '2b0047758102'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    inspector = sa.inspect(op.get_bind())
    if not inspector.has_table('assessment_answers'):
        return
    columns = {column["name"] for column in inspector.get_columns('assessment_answers')}
    if 'user_id' not in columns:
        op.add_column('assessment_answers', sa.Column('user_id', sa.Integer(), nullable=True))
        op.create_foreign_key(None, 'assessment_answers', 'user', ['user_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    """Downgrade schema."""
    pass
