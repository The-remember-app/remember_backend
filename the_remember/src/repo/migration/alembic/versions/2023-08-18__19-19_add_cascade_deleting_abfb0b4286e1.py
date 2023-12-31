"""add cascade deleting

Revision ID: abfb0b4286e1
Revises: 0c181f5c151f
Create Date: 2023-08-18 19:19:47.664002

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abfb0b4286e1'
down_revision = '0c181f5c151f'
branch_labels = None
depends_on = None
maintainer_name = "_Maintainer"


def upgrade():
    # TODO: check it!
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('add_info_of_term_parent_add_info_id_fkey', 'add_info_of_term', type_='foreignkey')
    op.drop_constraint('add_info_of_term_term_id_fkey', 'add_info_of_term', type_='foreignkey')
    op.create_foreign_key('add_info_of_term__parent_add_info_term_id__fk', 'add_info_of_term', 'add_info_of_term', ['parent_add_info_id'], ['id'], ondelete='set null')
    op.create_foreign_key('add_info_of_term__term_id__fk', 'add_info_of_term', 'term', ['term_id'], ['id'], ondelete='CASCADE')
    op.alter_column('folder', 'author_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.drop_constraint('folder_root_folder_id_fkey', 'folder', type_='foreignkey')
    op.drop_constraint('folder__author_id__fkey', 'folder', type_='foreignkey')
    op.create_foreign_key('folder__user_id__fk', 'folder', 'user', ['author_id'], ['id'], ondelete='set null')
    op.create_foreign_key('folder__root_folder_id__fk', 'folder', 'folder', ['root_folder_id'], ['id'], ondelete='CASCADE')
    op.alter_column('module', 'author_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.drop_constraint('module_root_folder_id_fkey', 'module', type_='foreignkey')
    op.drop_constraint('module_author_id_fkey', 'module', type_='foreignkey')
    op.create_foreign_key('module__user_id__fk', 'module', 'user', ['author_id'], ['id'], ondelete='set null')
    op.create_foreign_key('module__root_folder_id__fk', 'module', 'folder', ['root_folder_id'], ['id'], ondelete='set null')
    op.add_column('personalize_folder', sa.Column('root_folder_id', sa.UUID(), nullable=True))
    op.drop_constraint('personalize_folder_user_id_fkey', 'personalize_folder', type_='foreignkey')
    op.drop_constraint('personalize_folder_folder_id_fkey', 'personalize_folder', type_='foreignkey')
    op.create_foreign_key('personalize_folder__user_id__fk', 'personalize_folder', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('personalize_folder__to_root_personalize_folder__fk', 'personalize_folder', 'personalize_folder', ['user_id', 'root_folder_id'], ['user_id', 'folder_id'], ondelete='CASCADE')
    op.create_foreign_key('personalize_folder__folder_id__fk', 'personalize_folder', 'folder', ['folder_id'], ['id'], ondelete='CASCADE')
    op.add_column('personalize_module', sa.Column('root_folder_id', sa.UUID(), nullable=True))
    op.drop_constraint('personalize_module_module_id_fkey', 'personalize_module', type_='foreignkey')
    op.drop_constraint('personalize_module_user_id_fkey', 'personalize_module', type_='foreignkey')
    op.create_foreign_key('personalize_module__to_root_personalize_folder__fk', 'personalize_module', 'personalize_folder', ['user_id', 'root_folder_id'], ['user_id', 'folder_id'], ondelete='CASCADE')
    op.create_foreign_key('personalize_module__user_id__fk', 'personalize_module', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('personalize_module__module_id__fk', 'personalize_module', 'module', ['module_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('personalize_term_module_id_fkey', 'personalize_term', type_='foreignkey')
    op.drop_constraint('personalize_term_term_id_fkey', 'personalize_term', type_='foreignkey')
    op.drop_constraint('personalize_term_module_id_user_id_fkey', 'personalize_term', type_='foreignkey')
    op.drop_constraint('personalize_term_user_id_fkey', 'personalize_term', type_='foreignkey')
    op.create_foreign_key('personalize_term__user_id__fk', 'personalize_term', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('personalize_term__term_id__fk', 'personalize_term', 'term', ['term_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('personalize_term__module_id__fk', 'personalize_term', 'module', ['module_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('personalize_term__to_personalize_module__fk', 'personalize_term', 'personalize_module', ['module_id', 'user_id'], ['module_id', 'user_id'], ondelete='CASCADE')
    op.drop_constraint('sentence_term_id_fkey', 'sentence', type_='foreignkey')
    op.create_foreign_key('sentence__term_id__fk', 'sentence', 'term', ['term_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('term_module_id_fkey', 'term', type_='foreignkey')
    op.create_foreign_key('term__module_id__fk', 'term', 'module', ['module_id'], ['id'], ondelete='CASCADE')
    op.execute(  # language=PostgreSQL
        f"""
        update folder 
        set author_id = null
        from "user" u 
        where u.username = '{maintainer_name}' and folder.author_id = u.id
        returning *
        """
    )
    op.execute(  # language=PostgreSQL
        f"""
        update module 
        set author_id = null
        from "user" u 
        where u.username = '{maintainer_name}' and module.author_id = u.id
        returning *
        """
    )
    op.execute(  # language=PostgreSQL
        """
        update personalize_folder pf
        set root_folder_id = folder.root_folder_id
        from folder 
        where pf.folder_id = folder.id
        """
    )
    op.execute(  # language=PostgreSQL
        """
        update personalize_module 
        set root_folder_id = module.root_folder_id
        from module 
        where module_id = module.id
        """
    )
    # ### end Alembic commands ###


def downgrade():
    # TODO: check it!
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(  # language=PostgreSQL
        f"""
        insert into "user" (username, email, hashed_password, name, surname) values 
        ( '{maintainer_name}',  '{maintainer_name}',  '{maintainer_name}',  '{maintainer_name}',  '{maintainer_name}' )
        ON CONFLICT  DO NOTHING
         RETURNING *
        """
    )
    op.execute(  # language=PostgreSQL
        f"""
        update module 
        set author_id = u.id
        from "user" u
        where u.username = '{maintainer_name}' and module.author_id is null
        returning *
        """
    )
    op.execute(  # language=PostgreSQL
        f"""
        update folder 
        set author_id = u.id
        from "user" u 
        where u.username = '{maintainer_name}' and folder.author_id is null
        returning *
        """
    )
    op.drop_constraint('term__module_id__fk', 'term', type_='foreignkey')
    op.create_foreign_key('term_module_id_fkey', 'term', 'module', ['module_id'], ['id'])
    op.drop_constraint('sentence__term_id__fk', 'sentence', type_='foreignkey')
    op.create_foreign_key('sentence_term_id_fkey', 'sentence', 'term', ['term_id'], ['id'])
    op.drop_constraint('personalize_term__to_personalize_module__fk', 'personalize_term', type_='foreignkey')
    op.drop_constraint('personalize_term__module_id__fk', 'personalize_term', type_='foreignkey')
    op.drop_constraint('personalize_term__term_id__fk', 'personalize_term', type_='foreignkey')
    op.drop_constraint('personalize_term__user_id__fk', 'personalize_term', type_='foreignkey')
    op.create_foreign_key('personalize_term_user_id_fkey', 'personalize_term', 'user', ['user_id'], ['id'])
    op.create_foreign_key('personalize_term_module_id_user_id_fkey', 'personalize_term', 'personalize_module', ['module_id', 'user_id'], ['module_id', 'user_id'])
    op.create_foreign_key('personalize_term_term_id_fkey', 'personalize_term', 'term', ['term_id'], ['id'])
    op.create_foreign_key('personalize_term_module_id_fkey', 'personalize_term', 'module', ['module_id'], ['id'])
    op.drop_constraint('personalize_module__module_id__fk', 'personalize_module', type_='foreignkey')
    op.drop_constraint('personalize_module__user_id__fk', 'personalize_module', type_='foreignkey')
    op.drop_constraint('personalize_module__to_root_personalize_folder__fk', 'personalize_module', type_='foreignkey')
    op.create_foreign_key('personalize_module_user_id_fkey', 'personalize_module', 'user', ['user_id'], ['id'])
    op.create_foreign_key('personalize_module_module_id_fkey', 'personalize_module', 'module', ['module_id'], ['id'])
    op.drop_column('personalize_module', 'root_folder_id')
    op.drop_constraint('personalize_folder__folder_id__fk', 'personalize_folder', type_='foreignkey')
    op.drop_constraint('personalize_folder__to_root_personalize_folder__fk', 'personalize_folder', type_='foreignkey')
    op.drop_constraint('personalize_folder__user_id__fk', 'personalize_folder', type_='foreignkey')
    op.create_foreign_key('personalize_folder_folder_id_fkey', 'personalize_folder', 'folder', ['folder_id'], ['id'])
    op.create_foreign_key('personalize_folder_user_id_fkey', 'personalize_folder', 'user', ['user_id'], ['id'])
    op.drop_column('personalize_folder', 'root_folder_id')
    op.drop_constraint('module__root_folder_id__fk', 'module', type_='foreignkey')
    op.drop_constraint('module__user_id__fk', 'module', type_='foreignkey')
    op.create_foreign_key('module_author_id_fkey', 'module', 'user', ['author_id'], ['id'])
    op.create_foreign_key('module_root_folder_id_fkey', 'module', 'folder', ['root_folder_id'], ['id'])
    op.alter_column('module', 'author_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_constraint('folder__root_folder_id__fk', 'folder', type_='foreignkey')
    op.drop_constraint('folder__user_id__fk', 'folder', type_='foreignkey')
    op.create_foreign_key('folder__author_id__fkey', 'folder', 'user', ['author_id'], ['id'])
    op.create_foreign_key('folder_root_folder_id_fkey', 'folder', 'folder', ['root_folder_id'], ['id'])
    op.alter_column('folder', 'author_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_constraint('add_info_of_term__term_id__fk', 'add_info_of_term', type_='foreignkey')
    op.drop_constraint('add_info_of_term__parent_add_info_term_id__fk', 'add_info_of_term', type_='foreignkey')
    op.create_foreign_key('add_info_of_term_term_id_fkey', 'add_info_of_term', 'term', ['term_id'], ['id'])
    op.create_foreign_key('add_info_of_term_parent_add_info_id_fkey', 'add_info_of_term', 'add_info_of_term', ['parent_add_info_id'], ['id'])

    # ### end Alembic commands ###
