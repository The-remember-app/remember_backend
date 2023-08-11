"""add uuid extension

Revision ID: 7931f88b3838
Revises: 
Create Date: 2023-08-11 11:47:16.699810

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7931f88b3838'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # TODO: check it!
    op.execute(  # language=PostgreSql
        """
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    """)



def downgrade():
    # TODO: check it!
    op.execute(
        # language=PostgreSql
        """ 
        DROP EXTENSION  IF EXISTS "uuid-ossp";
    """)
