"""baseline schema

Revision ID: 82a4d2c17b46
Revises: 
Create Date: 2026-06-20 17:06:48.826427

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '82a4d2c17b46'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    inspector = sa.inspect(op.get_bind())

    if not inspector.has_table('user'):
        op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.Text(), nullable=False),
        sa.Column('password', sa.Text(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
        )

    if not inspector.has_table('admin_user'):
        op.create_table('admin_user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.Text(), nullable=True),
        sa.Column('password', sa.Text(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
        )

    if not inspector.has_table('documentation'):
        op.create_table('documentation',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('documentation_title', sa.Text(), nullable=False),
        sa.Column('source_code', sa.Text(), nullable=False),
        sa.Column('IBD_generated_md', sa.Text(), nullable=False),
        sa.Column('TD_md', sa.Text(), nullable=False),
        sa.Column('invariants', sa.Text(), nullable=True),
        sa.Column('soundness', sa.Float(), nullable=True),
        sa.Column('validity', sa.Float(), nullable=True),
        sa.Column('mutation_score', sa.Float(), nullable=True),
        sa.Column('mutation_summary', sa.Text(), nullable=True),
        sa.Column('hypothesis_tests', sa.Text(), nullable=True),
        sa.Column('ibd_doc_elo_rating', sa.Integer(), server_default=sa.text('1000'), nullable=False),
        sa.Column('td_doc_elo_rating', sa.Integer(), server_default=sa.text('1000'), nullable=False),
        sa.Column('bt_ibd_rating', sa.Float(), nullable=True),
        sa.Column('bt_td_rating', sa.Float(), nullable=True),
        sa.Column('bt_ibd_win_prob', sa.Float(), nullable=True),
        sa.Column('bt_ibd_win_prob_ci_lower', sa.Float(), nullable=True),
        sa.Column('bt_ibd_win_prob_ci_upper', sa.Float(), nullable=True),
        sa.Column('comparison_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.Column('ibd_wins', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.Column('td_wins', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
        )

    if not inspector.has_table('comparison'):
        op.create_table('comparison',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('documentation_id', sa.Integer(), nullable=False),
        sa.Column('winner', sa.String(), nullable=False),
        sa.Column('comments', sa.Text(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['documentation_id'], ['documentation.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
        )

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

    if not inspector.has_table('assessment_attempts'):
        op.create_table('assessment_attempts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('documentation_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('documentation_type', sa.String(), nullable=False),
        sa.Column('total_questions', sa.Integer(), nullable=False),
        sa.Column('total_correct', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['documentation_id'], ['documentation.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
        )

    if not inspector.has_table('assessment_answers'):
        op.create_table('assessment_answers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('attempt_id', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('user_response', sa.Text(), nullable=False),
        sa.Column('is_correct', sa.Boolean(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['attempt_id'], ['assessment_attempts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['question_id'], ['assessment_questions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
        )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('assessment_answers')
    op.drop_table('assessment_attempts')
    op.drop_table('assessment_questions')
