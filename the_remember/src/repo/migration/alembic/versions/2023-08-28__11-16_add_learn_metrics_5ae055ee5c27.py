"""add learn metrics

Revision ID: 5ae055ee5c27
Revises: f3aa28930274
Create Date: 2023-08-28 11:16:27.843814

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ae055ee5c27'
down_revision = 'f3aa28930274'
branch_labels = None
depends_on = None


def upgrade():
    # TODO: check it!
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('personalize_module', sa.Column('max_iteration_len', sa.Integer(), server_default=sa.text('10'), nullable=False))
    op.add_column('personalize_module', sa.Column('min_iteration_len', sa.Integer(), server_default=sa.text('4'), nullable=False))
    op.add_column('personalize_module', sa.Column('min_watch_count', sa.Integer(), server_default=sa.text('5'), nullable=False))
    op.add_column('personalize_module', sa.Column('known_term_part', sa.Integer(), server_default=sa.text('30'), nullable=False))
    op.add_column('personalize_module', sa.Column('choices_count', sa.Integer(), server_default=sa.text('4'), nullable=False))
    op.add_column('personalize_term', sa.Column('watch_count', sa.Integer(), server_default=sa.text('0'), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # TODO: check it!
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('personalize_term', 'watch_count')
    op.drop_column('personalize_module', 'choices_count')
    op.drop_column('personalize_module', 'known_term_part')
    op.drop_column('personalize_module', 'min_watch_count')
    op.drop_column('personalize_module', 'min_iteration_len')
    op.drop_column('personalize_module', 'max_iteration_len')
    # ### end Alembic commands ###
