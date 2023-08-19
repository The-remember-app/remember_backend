"""create personalize folder trigger

Revision ID: 25c31049cfb4
Revises: abfb0b4286e1
Create Date: 2023-08-18 23:59:25.674749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25c31049cfb4'
down_revision = 'abfb0b4286e1'
branch_labels = None
depends_on = None


def upgrade():
    # TODO: check it!
    op.execute(
        # language=PostgreSQL
        """
CREATE OR REPLACE FUNCTION autogenerate_personalize_folder()
    RETURNS TRIGGER AS $autogenerate_personalize_folder$
BEGIN
    --
    -- Create a row in emp_audit to reflect the operation performed on emp,
    -- make use of the special variable TG_OP to work out the operation.
    --
    INSERT INTO personalize_folder(folder_id, user_id, root_folder_id) values (NEW.id, NEW.author_id, NEW.root_folder_id);
    -- RETURN  NEW;
     RETURN NULL; 

END;
$autogenerate_personalize_folder$ LANGUAGE plpgsql;


        """
    )
    op.execute(
        # language=PostgreSQL
        """
        -- After триггер на добавление
CREATE   TRIGGER  autogenerate_personalize_folder__trigger
AFTER INSERT
ON folder
FOR EACH row EXECUTE FUNCTION autogenerate_personalize_folder();
        """)


def downgrade():
    # TODO: check it!
    op.execute(  # language=PostgreSQL
        """
           drop trigger autogenerate_personalize_folder__trigger on folder;
            """)
    op.execute(  # language=PostgreSQL
        """
        drop function autogenerate_personalize_folder;
         """)
