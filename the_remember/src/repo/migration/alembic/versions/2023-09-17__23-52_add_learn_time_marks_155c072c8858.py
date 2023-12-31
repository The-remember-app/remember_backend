"""add learn time marks

Revision ID: 155c072c8858
Revises: c6ace93cf827
Create Date: 2023-09-17 23:52:13.695152

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '155c072c8858'
down_revision = 'c6ace93cf827'
branch_labels = None
depends_on = None




update_columns_map = {
            "learn_term_datetime_mark": "updated_at",
        }


def func_name(field_name: str):
    return f'trigger_set_timestamp_as_{field_name}'


def trigger_name(table_name: str, field_name: str):
    return f'set_timestamp_{field_name}_as_{table_name}'


def upgrade():
    # TODO: check it!
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('learn_term_datetime_mark',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('term_id', sa.UUID(), nullable=False),
    sa.Column('start_watch', sa.DateTime(), nullable=False),
    sa.Column('end_watch', sa.DateTime(), nullable=False),
    sa.Column('is_learnt', sa.Boolean(), nullable=False),
    sa.Column('is_learn_iter_start', sa.Boolean(), nullable=False),
    sa.Column('watch_type', postgresql.ENUM('choice', 'reverse_choice', 'write', 'reverse_write', name='watch_learn_type__enum'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['term_id', 'user_id'], ['personalize_term.term_id', 'personalize_term.user_id'], name='learn_term_datetime_mark__to_personalize_term__fk', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['term_id'], ['term.id'], name='learn_term_datetime_mark__term_id__fk', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='learn_term_datetime_mark__user_id__fk', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    commands = [
        f"""
            CREATE or REPLACE TRIGGER  {trigger_name(k, v)}
    BEFORE UPDATE ON "{k}"
    FOR EACH ROW
    EXECUTE PROCEDURE {func_name(v)}();
            """ for (k, v) in update_columns_map.items()
    ]
    [op.execute(i) for i in commands]
    # ### end Alembic commands ###


def downgrade():
    # TODO: check it!
    # ### commands auto generated by Alembic - please adjust! ###
    commands = [  # language=postgresql
                   f"""
            drop TRIGGER if exists {trigger_name(k, v)}  on "{k}"
            """ for (k, v) in update_columns_map.items()
               ]

    [op.execute(i) for i in commands]
    op.drop_table('learn_term_datetime_mark')
    # ### end Alembic commands ###
