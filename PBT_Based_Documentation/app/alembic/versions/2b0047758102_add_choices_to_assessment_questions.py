"""add choices to assessment questions

Revision ID: 2b0047758102
Revises: 82a4d2c17b46
Create Date: 2026-06-20 17:07:34.733797

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2b0047758102'
down_revision: Union[str, Sequence[str], None] = '82a4d2c17b46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    inspector = sa.inspect(op.get_bind())
    if not inspector.has_table('assessment_questions'):
        op.create_table('assessment_questions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('documentation_id', sa.Integer(), nullable=False),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('choices', sa.JSON().with_variant(postgresql.JSONB(astext_type=sa.Text()), 'postgresql'), nullable=True),
        sa.Column('correct_response', sa.Text(), nullable=False),
        sa.Column('explanation', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(['documentation_id'], ['documentation.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
        )
    else:
        columns = {column["name"] for column in inspector.get_columns('assessment_questions')}
        if 'choices' not in columns:
            op.add_column(
                'assessment_questions',
                sa.Column('choices', sa.JSON().with_variant(postgresql.JSONB(astext_type=sa.Text()), 'postgresql'), nullable=True),
            )


def downgrade() -> None:
    """Downgrade schema."""
    pass
