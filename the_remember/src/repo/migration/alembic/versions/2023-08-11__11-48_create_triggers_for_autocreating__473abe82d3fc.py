"""create triggers for autocreating personalize_module and personalize_term

Revision ID: 473abe82d3fc
Revises: d1a4c4c6fdfd
Create Date: 2023-08-11 11:48:45.795707

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '473abe82d3fc'
down_revision = 'd1a4c4c6fdfd'
branch_labels = None
depends_on = None



def upgrade():
    # TODO: check it!

    op.execute(
        # language=PostgreSQL
        """
CREATE OR REPLACE FUNCTION autogenerate_personalize_module()
    RETURNS TRIGGER AS $autogenerate_personalize_module$
BEGIN
    --
    -- Create a row in emp_audit to reflect the operation performed on emp,
    -- make use of the special variable TG_OP to work out the operation.
    --
    INSERT INTO personalize_module(module_id, user_id) values (NEW.id, NEW.author_id);
    -- RETURN  NEW;
     RETURN NULL; 

END;
$autogenerate_personalize_module$ LANGUAGE plpgsql;


        """
    )

    op.execute(
        # language=PostgreSQL
        """
CREATE OR REPLACE FUNCTION autogenerate_personalize_term()
    RETURNS TRIGGER AS $autogenerate_personalize_term$
BEGIN
    --
    -- Create a row in emp_audit to reflect the operation performed on emp,
    -- make use of the special variable TG_OP to work out the operation.
    --

    INSERT INTO personalize_term(module_id, user_id, term_id) values (
        NEW.module_id, 
        (SELECT m.author_id FROM module as m WHERE m.id = NEW.module_id LIMIT 1 ), 
        NEW.id
    );
    RETURN NEW;

END;
$autogenerate_personalize_term$ LANGUAGE plpgsql;


        """
    )

    op.execute(
        # language=PostgreSQL
        """
        -- After триггер на добавление
CREATE   TRIGGER  autogenerate_personalize_module__trigger
AFTER INSERT
ON module
FOR EACH row EXECUTE FUNCTION autogenerate_personalize_module();
        """)
    op.execute(
        # language=PostgreSQL
        """
        -- After триггер на добавление
CREATE   TRIGGER  autogenerate_personalize_term__trigger
AFTER INSERT
ON term
FOR EACH row EXECUTE FUNCTION autogenerate_personalize_term();
        """)


def downgrade():
    # TODO: check it!

    op.execute(  # language=PostgreSQL
        """
        drop trigger autogenerate_personalize_module__trigger on module;
    """)
    op.execute(  # language=PostgreSQL
        """
           drop trigger autogenerate_personalize_term__trigger on term;
            """)
    op.execute(  # language=PostgreSQL
        """
        drop function autogenerate_personalize_module;
         """)
    op.execute(  # language=PostgreSQL
        """
        drop function autogenerate_personalize_term;
    """)

