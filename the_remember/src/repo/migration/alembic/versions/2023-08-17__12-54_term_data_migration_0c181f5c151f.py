"""term data migration

Revision ID: 0c181f5c151f
Revises: 8ac6e6da0be3
Create Date: 2023-08-17 12:54:06.715253

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c181f5c151f'
down_revision = '8ac6e6da0be3'
branch_labels = None
depends_on = None



def upgrade():
    # TODO: check it!
#     op.execute(  # language=PostgreSQL
#         """
#         insert into add_info_of_term
#     (text_data, adding_text_data, add_info_type, term_id)
#
# select t.term, null, 'usual_term'::add_info_type__enum, t.id
# from term as t
# where not(t.term LIKE '% %');
#         """
#     )

    op.execute("""
        with recursive replacing_text as (select replace(
                                                 term.term,
                                                 substr('ÁáÉéÍíÓóÚúÝýÀàÈèÌìÒòÙù', 1, 1),
                                                 substr('AaEeIiOoUuYyAaEeIiOoUu', 1, 1)
                                             ) as res_,
                                         2     as str_index,
                                         term,
                                         id,
                                         substr('AaEeIiOoUuYyAaEeIiOoUu', 1, 1)

                                  from term
                                  where term.term SIMILAR TO '%[ÁáÉéÍíÓóÚúÝýÀàÈèÌìÒòÙù]%'
                                  union all
                                  select replace(
                                                 res_,
                                                 substr('ÁáÉéÍíÓóÚúÝýÀàÈèÌìÒòÙù', str_index, 1),
                                                 substr('AaEeIiOoUuYyAaEeIiOoUu', str_index, 1)
                                             ) as res_,
                                      str_index + 1     as str_index,
                                                                               term,
                                         id,
                                         substr('ÁáÉéÍíÓóÚúÝýÀàÈèÌìÒòÙù', str_index, 1)
                                  from replacing_text
                                  where str_index <= length('AaEeIiOoUuYyAaEeIiOoUu')
                                  ),
    inserting as (

        insert
            into add_info_of_term (text_data,
                                   adding_text_data,
                                   add_info_type,
                                   term_id)
                select res_, term, 'transcription'::add_info_type__enum, id
                from replacing_text
                where str_index > length('AaEeIiOoUuYyAaEeIiOoUu')
                returning *)
update term
set
    term = text_data
from inserting
where inserting.term_id = term.id
returning *;
    """)

    op.execute("""
        INSERT INTO personalize_folder (folder_id, user_id)
        select folder.id, folder.author_id
        from folder
        returning *
    """)
    op.execute(  # language=PostgreSQL
        """
update term
set term = replace(term, '&#8217;', '`')
where term like '%&#8217;%'
returning *
;
    """)
    op.execute(  # language=PostgreSQL
        """
update term
set term = replace(term, '’', '`')
where term like '%’%'
returning *
;
    """)
    op.execute(  # language=PostgreSQL
        """
update term
set term = 'colour (br.), color (am.)'
where term like 'color (colour)'
returning *
;
    """)
    op.execute(  # language=PostgreSQL
        """
update term
set term = 'can (could, could)'
where term like 'can (could)'
returning *
;
    """)
    op.execute(  # language=PostgreSQL
        """
update term
set term = 'grey  (br.), gray (am.)'
where term like 'grey (gray)'
returning *
;
    """)
    op.execute(  # language=PostgreSQL
        """
update term
set term = 'favour  (br.), favor (am.)'
where term like 'favor (favour)'
returning *
;
    """)
    op.execute(  # language=PostgreSQL
        """
update term
set term = 'personal computer (сокр. ps)'
where term like 'pc (personal computer)'
returning *
;
    """)
    op.execute(  # language=PostgreSQL
        """
update term
set term = 'ahead (go ahead)'
where term like '%ahead (go ahed)%'
returning *
;
    """)
    op.execute(  # language=PostgreSQL
        """
update term
set term = 'tablet computer (сокр. tablet)'
where term like 'tablet (tablet computer)'
returning *
;
    """)
    op.execute(  # language=PostgreSQL
        """
        with base_select as (select t.term as base_text_data,
                            null as adding_text_data,
                            null as dialect_or_area,
                            'usual_term'::add_info_type__enum as add_info_type,
                            t.id as term_id,
                            lower(trim(substring(t.term similar '%#"[A-Za-z \s\S`]*#"[(]%' escape '#')))   as orig_term,
                            lower(trim(substring(t.term similar '%[(]#"[A-Za-z \s\S`]*#"[,]%' escape '#')))         as v2_form,
                            lower(trim(substring(t.term similar '%[,][ \s\S]*?#"[A-Za-z \s\S`]*#"[)]' escape '#'))) as v3_form
                     from term as t
                              join module m on t.module_id = m.id
                              join folder f on f.id = m.root_folder_id
                     where (t.term LIKE '% %')
                       and (t.term LIKE '%(%,%)%')
                       and not ((t.term LIKE '%\\%'))
                       and (lower(f.name) like '%глаголы%')),
    orig_term as (
        select orig_term as text_data,
               'infinitive' as adding_text_data,
               dialect_or_area as dialect_or_area,
               add_info_type as add_info_type,
               term_id as term_id
        from base_select
    ),
    v2_term as (
        select v2_form as text_data,
               'v2' as adding_text_data,
               dialect_or_area as dialect_or_area,
               'other_form'::add_info_type__enum as add_info_type,
               term_id as term_id
        from base_select
    ),
    v3_term as (
        select v3_form  as text_data,
               'v3' as adding_text_data,
               dialect_or_area as dialect_or_area,
               'other_form'::add_info_type__enum as add_info_type,
               term_id as term_id
        from base_select
    ),
    union_selects as (
        select *
         from orig_term
         union
         select *
         from v2_term
         union select *
         from v3_term
    )
insert into add_info_of_term
    (text_data, adding_text_data, dialect_or_area, add_info_type, term_id)
select text_data, adding_text_data, dialect_or_area, add_info_type, term_id
from union_selects
join term t on t.id = union_selects.term_id
        """
    )

    op.execute(  # language=PostgreSQL
        """
with base_select as (select t.term as base_text_data,
                            null as adding_text_data,
                            null as dialect_or_area,
                            'usual_term'::add_info_type__enum as add_info_type,
                            t.id as term_id,
                            lower(trim(substring(t.term similar '%#"[A-Za-z \s\S`]*#"[(]%' escape '#')))   as orig_term,
                            lower(trim(substring(t.term similar '%[(]#"[A-Za-z \s\S`]*#"[,]%' escape '#')))         as v2_form,
                            lower(trim(substring(t.term similar '%[,][ \s\S]*?#"[A-Za-z \s\S`]*#"[)]' escape '#'))) as v3_form
                     from term as t
                              join module m on t.module_id = m.id
                              join folder f on f.id = m.root_folder_id
                     where (t.term LIKE '% %')
                       and (t.term LIKE '%(%,%)%')
                       and ((t.term LIKE '%\\%'))
                       and (lower(f.name) like '%глаголы%')),
    orig_term as (
        select orig_term as text_data,
               'infinitive' as adding_text_data,
               dialect_or_area as dialect_or_area,
               add_info_type as add_info_type,
               term_id as term_id
        from base_select
    union

        select v2_form as text_data,
               'v2' as adding_text_data,
               dialect_or_area as dialect_or_area,
               'other_form'::add_info_type__enum as add_info_type,
               term_id as term_id
        from base_select
    union
        select v3_form  as text_data,
               'v3' as adding_text_data,
               dialect_or_area as dialect_or_area,
               'other_form'::add_info_type__enum as add_info_type,
               term_id as term_id
        from base_select
    ),
    with_geo_style as (
        select *
        from orig_term
        where text_data not like '%\\%'
        union
        select
            trim(substring(text_data similar '%#"[A-Za-z \s\S`]*#"[\\]%' escape '#'))  as text_data,
            adding_text_data,
            'British',
            add_info_type,
            term_id

        from orig_term
        where text_data like '%\\%'
        union
        select
            trim(substring(text_data similar '%[\\]#"[A-Za-z \s\S`]*#"%' escape '#'))  as text_data,
            adding_text_data,
            'American',
            add_info_type,
            term_id

        from orig_term
        where text_data like '%\\%'
    )
insert into add_info_of_term
    (text_data, adding_text_data, dialect_or_area, add_info_type, term_id)
select *
from with_geo_style
    """)


    op.execute(  # language=PostgreSQL
        """
with RECURSIVE
    formatting_data as (select trim((string_to_array(base_text_data, ')'))[1]) as base_text_data,
                               adding_text_data,
                               dialect_or_area,
                               add_info_type,
                               term_id,
                               2                                               as arr_index,
                               string_to_array(base_text_data, ')')::text[]    as text_as_arr
                        from raw_data
                        union all
                        select trim(text_as_arr[arr_index]) as base_text_data,
                               adding_text_data,
                               dialect_or_area,
                               add_info_type,
                               term_id,
                               arr_index + 1                as arr_index,
                               text_as_arr
                        from formatting_data
                        where arr_index = 1
                           or (text_as_arr[arr_index ] IS NOT NULL
                            and not(text_as_arr[arr_index ] = '' and text_as_arr[arr_index + 1] IS  NULL))
                        ),
    raw_data as (select replace(t.term, ',', ' ')         as base_text_data,
                        null                              as adding_text_data,
                        null                              as dialect_or_area,
                        'usual_term'::add_info_type__enum as add_info_type,
                        t.id                              as term_id
                 from term as t
                          join module m on t.module_id = m.id
                          join folder f on f.id = m.root_folder_id
                 where (t.term LIKE '% %')
                   and ((t.term LIKE '%(%.)%')
                     or (t.term LIKE '%(geography)%')
                     or (t.term LIKE '%(am)%')
                     or (t.term LIKE '%(br)%')
                     or (t.term LIKE '%(us)%')
                     or (t.term LIKE '%(uk)%'))
--                        and (t.term LIKE '%(%,%)%')
--                        and ((t.term LIKE '%\\%'))
                    and  (
                         lower(f.name) not like '%глаголы%' or
                         (lower(f.name) like '%глаголы%' and (t.term not LIKE '%(%,%)%'))
                         )),
    add_dialect_or_area as (select trim((string_to_array(base_text_data, '('))[1])                   as base_text_data,
                                   adding_text_data,
                                   trim(replace((string_to_array(base_text_data, '('))[2], '.', '')) as dialect_or_area,
                                   add_info_type,
                                   term_id
                            from formatting_data),
    formatting_dialect_or_area as (select base_text_data,
                                          adding_text_data,
                                          (case
                                               when dialect_or_area = 'am' then 'American'
                                               when dialect_or_area = 'br' then 'British'
                                               when dialect_or_area = 'us' then 'American'
                                               when dialect_or_area = 'uk' then 'British'
                                               else dialect_or_area end) as dialect_or_area,
                                          add_info_type,
                                          term_id
                                   from add_dialect_or_area)

insert
into add_info_of_term
    (text_data, adding_text_data, dialect_or_area, add_info_type, term_id)
select *
from formatting_dialect_or_area;
    """)
    op.execute(  # language=PostgreSQL
        """
with raw_data
         as (select lower(trim(substring(lower(t.term) similar '%#"[A-Za-z \s\S`]*#"[(]%' escape '#')))           as base_text_data,
                    null                                                                                         as adding_text_data,
                    null                                                                                         as dialect_or_area,
                    'usual_term'::add_info_type__enum                                                            as add_info_type,
                    t.id                                                                                         as term_id,
                    lower(trim(substring(lower(t.term) similar '%[(]сокр[.]#"[A-Za-z \s\S`]*#"[)]%'
                                         escape '#')))                                                           as abbreviation

             from term as t
                      join module m on t.module_id = m.id
                      join folder f on f.id = m.root_folder_id
             where (t.term LIKE '% %')
               and (t.term LIKE '%(сокр.%)%')
--                        and (t.term LIKE '%(%,%)%')
--                        and ((t.term LIKE '%\\%'))
                and  (
                         lower(f.name) not like '%глаголы%' or
                         (lower(f.name) like '%глаголы%' and (t.term not LIKE '%(%,%)%'))
                         )),
     formatting_data as (select base_text_data,
                                adding_text_data,
                                dialect_or_area,
                                add_info_type,
                                term_id
                         from raw_data
                         union
                         select abbreviation,
                                adding_text_data,
                                dialect_or_area,
                                'abbreviation'::add_info_type__enum as add_info_type,
                                term_id
                         from raw_data)
insert
into add_info_of_term
    (text_data, adding_text_data, dialect_or_area, add_info_type, term_id)
select *
from formatting_data;
    """)

     # language=PostgreSQL
    query_ = """
with recursive
    raw_data_2 as (select trim((string_to_array(base_text_data, ','))[1]) as base_text_data,
                          adding_text_data,
                          dialect_or_area,
                          add_info_type,
                          term_id,
                          2                                               as _arr_index,
                          string_to_array(base_text_data, ',')::text[]    as _text_as_arr
                   from raw_data_1
                   where base_text_data like '%,%(%)%'

                   union all
                   select trim(_text_as_arr[_arr_index]) as base_text_data,
                          adding_text_data,
                          dialect_or_area,
                          add_info_type,
                          term_id,
                          _arr_index + 1                 as _arr_index,
                          _text_as_arr
                   from raw_data_2
                   where _arr_index = 1
                      or _text_as_arr[_arr_index] IS NOT NULL),
    raw_data_3 as (select base_text_data,
                          adding_text_data,
                          dialect_or_area,
                          add_info_type,
                          term_id
                   from raw_data_1
                   where not (base_text_data like '%,%(%)%')),
    raw_data as (select base_text_data,
                        adding_text_data,
                        dialect_or_area,
                        add_info_type,
                        term_id
                 from raw_data_2
                 union
                 select *
                 from raw_data_3),


    raw_data_1 as (select t.term                            as base_text_data,
                          t.definition,
                          null                              as adding_text_data,
                          null                              as dialect_or_area,
                          'usual_term'::add_info_type__enum as add_info_type,
                          t.id                              as term_id
                   from term as t
                            join module m on t.module_id = m.id
                            join folder f on f.id = m.root_folder_id
                   where (t.term LIKE '% %')
                     and not (t.term LIKE '%(сокр.%)%')
                     and not ((t.term LIKE '%(%.)%')
                       or (t.term LIKE '%(geography)%')
                       or (t.term LIKE '%(am)%')
                       or (t.term LIKE '%(br)%')
                       or (t.term LIKE '%(us)%')
                       or (t.term LIKE '%(uk)%'))
                     and (t.term LIKE '%(%)%')
--                      and (t.term like '%…%')
--                      and (t.term like '%,%(%)%')
--                        and (t.term LIKE '%(%,%)%')
--                        and ((t.term LIKE '%\\%'))
                      and  (
                         lower(f.name) not like '%глаголы%' or
                         (lower(f.name) like '%глаголы%' and (t.term not LIKE '%(%,%)%'))
                         )),
    raw_data_4 as (select uuid_generate_v4()::uuid              as id,
                          t.term                                as base_text_data,
                          null                                  as adding_text_data,
                          null                                  as dialect_or_area,
                          'composite_word'::add_info_type__enum as add_info_type,
                          t.id                                  as term_id
                   from term as t
                   where not (t.term LIKE '%(%)%')
                     and (t.term like '%…%')),

    formatted_data as (select uuid_generate_v4()::uuid           as id,
                              lower(trim(substring(lower(base_text_data) similar '%#"[…A-Za-z \s\S`]*#"[(]%'
                                                   escape '#'))) as base_text_data,
                              adding_text_data,
                              dialect_or_area,
                              add_info_type,
                              term_id
                       from raw_data
                       where base_text_data like '%(%)'
                       union
                       select uuid_generate_v4()::uuid as id,
                              base_text_data,
                              adding_text_data,
                              dialect_or_area,
                              add_info_type,
                              term_id
                       from raw_data
                       where not (base_text_data like '%(%)%')
                       union
                       select *
                       from raw_data_4
                       union
                       select uuid_generate_v4()::uuid as id,
                              base_text_data,
                              adding_text_data,
                              dialect_or_area,
                              add_info_type,
                              term_id
                       from raw_data
                       where not (base_text_data like '%(%)%')
                       union
                       select uuid_generate_v4()::uuid           as id,
                              lower(trim(substring(lower(base_text_data) similar '%[)]#"[…A-Za-z \s\S`]*#"%'
                                                   escape '#'))) as base_text_data,
                              adding_text_data,
                              dialect_or_area,
                              add_info_type,
                              term_id
                       from raw_data
                       where base_text_data like '(%)%'),
    comlexed_term as (select uuid_generate_v4()::uuid                        as id,
                             trim((string_to_array(base_text_data, '…'))[1]) as base_text_data,
                             cast(1 as varchar)                              as adding_text_data,
                             dialect_or_area,
                             'composite_word'::add_info_type__enum           as add_info_type,
                             term_id,
                             2                                               as _arr_index,
                             string_to_array(base_text_data, '…')::text[]    as _text_as_arr

                      from formatted_data
                      where base_text_data like '%…%'
                      union all
                      select uuid_generate_v4()::uuid       as id,
                             trim(_text_as_arr[_arr_index]) as base_text_data,
                             cast(_arr_index as varchar)    as adding_text_data,
                             dialect_or_area,
                             add_info_type,
                             term_id,
                             _arr_index + 1                 as _arr_index,
                             _text_as_arr
                      from comlexed_term
                      where _arr_index = 1
                         or (_text_as_arr[_arr_index] IS NOT NULL
                          and not (_text_as_arr[_arr_index] = '' and _text_as_arr[_arr_index + 1] IS NULL))),

    q1_ as (select lower(trim(substring(lower(base_text_data) similar
                                        '%[(]#"[…A-Za-z \s\S,`0-9?!.]*#"[)]%'
                                        escape '#'))) as base_text_data,
                   'any'                              as adding_text_data,
                   dialect_or_area,
                   add_info_type,
                   term_id,
                   lower(trim(substring(lower(base_text_data) similar '%#"[…A-Za-z \s\S`]*#"[(]%'
                                        escape '#'))) as main_term
            from raw_data
            where base_text_data like '%(%)'),
    q2_ as (select ' ' || base_text_data || ' ' as base_text_data,
                   adding_text_data,
                   dialect_or_area,
                   (case
                        when base_text_data like '%' || main_term || '%'
                            then 'help_phrase_with_word'::add_info_type__enum
                        else 'help_phrase_without_word'::add_info_type__enum
                       end)                     as add_info_type,
                   term_id,
                   main_term
            from q1_),

    q3_ as (select trim(q2_.base_text_data)                                                       as base_text_data,
                   trim(q2_.base_text_data)                                                       as adding_text_data,
                   q2_.dialect_or_area,
                   1                                                                              as add_info_type,
                   q2_.term_id,
                   (case
                        when q2_.main_term like '%…%' then null
                        else
                            (case when target_table.id is NULL then fd.id else target_table.id end)
                       end)                                                                       as parent_add_info_id,
                   q2_.adding_text_data                                                           as _normal_adding_text_data,
                   1                                                                              as _arr_index,
                   string_to_array(trim(q2_.main_term), ' ')::text[]                              as _adding_text_data_as_arr,
                   trim(replace((string_to_array(trim(q2_.main_term), ' ')::text[])[1], '…', '')) as next_word,
                   q2_.base_text_data                                                             as _old_base_text_data,
                   main_term                                                                      as main_term


            from q2_
                     join formatted_data fd on
                fd.term_id = q2_.term_id and fd.base_text_data = main_term
                     left join add_info_of_term target_table
                               on target_table.term_id = q2_.term_id and target_table.text_data = main_term
            union all
            select base_text_data,
                   trim(replace((
                                    case
                                        when add_info_type = _arr_index and
                                             replace(adding_text_data, ' ' || next_word || ' ', ' ... ') !=
                                             adding_text_data
                                            then replace(adding_text_data, ' ' || next_word || ' ', ' ... ')
                                        when add_info_type = _arr_index and
                                             replace(adding_text_data, ' ' || next_word, ' ...') !=
                                             adding_text_data
                                            then replace(adding_text_data, ' ' || next_word, ' ...')
                                        when add_info_type = _arr_index and
                                             replace(adding_text_data, next_word || ' ', '... ') !=
                                             adding_text_data
                                            then replace(adding_text_data, next_word || ' ', '... ')
                                        when add_info_type = _arr_index and
                                             replace(adding_text_data, next_word, '...') !=
                                             adding_text_data
                                            then replace(adding_text_data, next_word, '...')
                                        else _old_base_text_data end
                                    ), '... ...', '...'))                           as adding_text_data,
                   dialect_or_area,
                   (case
                        when base_text_data like '%' || next_word || '%' then 1
                        else 0 end) + add_info_type                                 as add_info_type,
                   term_id,
                   parent_add_info_id,
                   _normal_adding_text_data,
                   _arr_index + 1                                                   as _arr_index,
                   _adding_text_data_as_arr,
                   trim(replace(_adding_text_data_as_arr[_arr_index + 1], '…', '')) as next_word,
                   q3_.base_text_data                                               as _old_base_text_data,
                   main_term
            from q3_
            where (_arr_index = 1)
               or (_adding_text_data_as_arr[_arr_index] IS NOT NULL
                and not (_adding_text_data_as_arr[_arr_index] = '' and
                         _adding_text_data_as_arr[_arr_index + 1] IS NULL))),
    q4_ as (select base_text_data,
                   (case
                        when add_info_type = _arr_index then adding_text_data
                        else 'any' end)                                           as adding_text_data,
                   dialect_or_area,
                   (case
                        when add_info_type = _arr_index then 'help_phrase_with_word'::add_info_type__enum
                        else 'help_phrase_without_word'::add_info_type__enum end) as add_info_type,
                   term_id,
                   parent_add_info_id,
                   _arr_index,
                   add_info_type                                                  as count_
            from q3_
            where next_word is null),

    update_err_terms as (
        update term
            set term = replace(replace(term, ')', ''), '(', ' , ')
            from q4_
            where (_arr_index != count_ and count_ > 1) and q4_.term_id = term.id
            returning _arr_index, count_),

    formatting_data as (select uuid_generate_v4()::uuid as id,
                               base_text_data,
                               adding_text_data,
                               dialect_or_area,
                               add_info_type,
                               term_id,
                               parent_add_info_id
                        from q4_
                        where not (_arr_index != count_ and count_ > 1)
                        union
                        select null, null, null, null, null, null, null
                        from update_err_terms
                        where not (_arr_index != count_ and count_ > 1)
                        union
                        select uuid_generate_v4()::uuid                        as id,
                               lower(trim(substring(lower(rd.base_text_data) similar
                                                    '%[(]#"[…A-Za-z \s\S,`0-9?!.]*#"[)]%'
                                                    escape '#')))              as base_text_data,
                               'at_first'                                      as adding_text_data,
                               rd.dialect_or_area,
                               'help_phrase_without_word'::add_info_type__enum as add_info_type,
                               rd.term_id,
                               (case
                                    when rd.base_text_data like '%…%' then null
                                    else
                                        (case when target_table.id is NULL then fd.id else target_table.id end)
                                   end)                                        as parent_add_info_id

                        from raw_data as rd
                                 join formatted_data fd on
                                    fd.term_id = rd.term_id and fd.base_text_data =
                                                                 lower(trim(substring(lower(rd.base_text_data) similar
                                                                                      '%[)]#"[…A-Za-z \s\S`]*#"%'
                                                                                      escape '#')))
                                 left join add_info_of_term target_table
                                           on target_table.term_id = rd.term_id and target_table.text_data =
                                                                                     lower(trim(substring(
                                                                                             lower(rd.base_text_data)
                                                                                             similar
                                                                                             '%[)]#"[…A-Za-z \s\S`]*#"%'
                                                                                             escape '#')))


                        where rd.base_text_data like '(%)%'),
    all_formatted_data as (select *
                           from formatting_data
                           union
                           select *,
                                  null as parent_add_info_id
                           from formatted_data
                           where base_text_data not like '%…%'
                           union
                           select id,
                                  base_text_data,
                                  adding_text_data,
                                  dialect_or_area,
                                  add_info_type,
                                  term_id,
                                  null as parent_add_info_id
                           from comlexed_term
                           order by parent_add_info_id NULLS FIRST),
    first_op as (select *
                 from all_formatted_data
                 where parent_add_info_id is null),
    second_op as (select *
                  from all_formatted_data
                  where parent_add_info_id is not null)

    """


    op.execute(  # language=PostgreSQL
        query_ + """
insert
into add_info_of_term
    (id, text_data, adding_text_data, dialect_or_area, add_info_type, term_id, parent_add_info_id)
select *
from first_op
    """)
    op.execute(  # language=PostgreSQL
        query_ + """
    insert
    into add_info_of_term
        (id, text_data, adding_text_data, dialect_or_area, add_info_type, term_id, parent_add_info_id)
    select *
    from second_op
        """)

    op.execute(  # language=PostgreSQL
        """
with recursive raw_data as (select trim((string_to_array(t.term, ','))[1]) as base_text_data,
                         null                                    as adding_text_data,
                         null                                    as dialect_or_area,
                         'usual_term'::add_info_type__enum       as add_info_type,
                         t.id                                    as term_id,
                         2                                       as _arr_index,
                         string_to_array(t.term, ',')::text[]    as _text_as_arr
                  from term as t
                           join module m on t.module_id = m.id
                           join folder f on f.id = m.root_folder_id
                  where (t.term LIKE '% %')
                    and not (t.term LIKE '%(сокр.%)%')
                    and not ((t.term LIKE '%(%.)%')
                      or (t.term LIKE '%(geography)%')
                      or (t.term LIKE '%(am)%')
                      or (t.term LIKE '%(br)%')
                      or (t.term LIKE '%(us)%')
                      or (t.term LIKE '%(uk)%'))
                    and not (t.term LIKE '%(%)%')
                    and not (t.term like '%…%')
                    and (t.term like '%,%')
                   and  (
                         lower(f.name) not like '%глаголы%' or
                         (lower(f.name) like '%глаголы%' and (t.term not LIKE '%(%,%)%'))
                         )
                  union all
                  select  trim(_text_as_arr[_arr_index]) as base_text_data,
                              adding_text_data,
                              dialect_or_area,
                              add_info_type,
                              term_id,
                              _arr_index  + 1 as _arr_index,
                              _text_as_arr
                  from raw_data
                  where _arr_index = 1
                         or (_text_as_arr[_arr_index] IS NOT NULL
                          and not (_text_as_arr[_arr_index] = '' and _text_as_arr[_arr_index + 1] IS NULL))

                  )
insert
into add_info_of_term
( text_data, adding_text_data, dialect_or_area, add_info_type, term_id)
select base_text_data,
                              adding_text_data,
                              dialect_or_area,
                              add_info_type,
                              term_id
from raw_data
returning *
;
    """)
    # op.execute(  # language=PostgreSQL
    #     """
    #
    # """)


def downgrade():
    # TODO: check it!
    pass

