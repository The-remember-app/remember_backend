import re
import urllib.request
from datetime import datetime
from time import sleep
from urllib.error import URLError
from uuid import UUID

from sqlalchemy.ext.asyncio import async_sessionmaker

from the_remember.src.api.folders.dto import CreateFolderAsTreeDTO
from the_remember.src.api.folders.view import create_folder_as_tree
from the_remember.src.api.modules.dto import CreateModuleAsTreeDTO
from the_remember.src.api.sentences.dto import CreateSentenceAsTreeDTO
from the_remember.src.api.terms.dtos.dto import CreateTermAsTreeDTO
from the_remember.src.api.users.dto import UserDTO
from the_remember.src.config.config import CONFIG
from the_remember.src.utils._help_file import r_d, bad_terms, add_words


async def get_3000_words():
    r_ = r"<ol[^<]*(?:<li>[^<]*(?:<a(?:(?<=<a)([^>]*)>[^<]*(?=<\/a>))<\/a>[^@]*?)[^<]*<\/li>[^<]*)*?(?=<\/ol>)<\/ol>"
    main_folder = CreateFolderAsTreeDTO(
        name='3000_words',
        sub_folders=[],
    )

    fp = urllib.request.urlopen("https://langformula.ru/voc3000/")
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    # print(mystr)
    for i in re.findall(
            r"(?:<\/span>[^<]*<\/div>[^#]*?(?=<ol>))<ol>[^#]*?(?=<\/ol>)<\/ol>",
            mystr
    ):

        folder_title = re.search(r'<\/span>([^<]*)<\/div>', i).groups()[0]
        cur_folder = CreateFolderAsTreeDTO(
            name=' '.join(folder_title.split()),
            sub_folders=[],
            sub_modules=[]
        )
        main_folder.sub_folders += [cur_folder]
        print(folder_title)
        for html_link_tag in re.findall(
                r"<li>[^<]*(?:<a(?:(?<=<a)([^>]*)>([^<]*)(?=<\/a>))<\/a>[^@]*?)[^<]*<\/li>[^<]*", i):
            link = re.search(r'''href=(?:"|'|`)([^"'`]*)(?:"|'|`)''', html_link_tag[0]).groups()[0]
            print(link, html_link_tag[1])
            module_name = html_link_tag[1]
            curr_module = CreateModuleAsTreeDTO(
                name=' '.join(module_name.split()),
                description=f'autogenerated from {link}',
                sub_terms=get_words_from_words_page(link)
            )
            cur_folder.sub_modules += [curr_module]
    print(main_folder.model_dump_json())
    return main_folder


def get_words_from_words_page(url: str):
    _r = r'(?:<\/i>[^<]*?<strong[^>]*>(?:(?:<a[^>]*>([^<]*)<\/a>([^<]*)(?=</strong>)</strong>([^—<&#8212–-]*)(?:—|&#8212;|&#8212|–|-))|(?:([^<]*)</strong>([^—<&#8212–-]*)(?:—|&#8212;|&#8212|–|-)))([^<]*)<\/li>)'
    fp = None
    while fp is None:
        try:
            fp = urllib.request.urlopen(url)
        except URLError as e:
            print(e)
            sleep(1)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    table_datas = re.findall(r'<table([^@]*?)<\/table>', mystr)
    print(table_datas)
    terms_entities: dict[str, CreateTermAsTreeDTO] = dict()
    for table_data in table_datas:
        for word in re.finditer(
                r'<tr[^@]*?(?:<td[^>]*>([^<]*)<\/td>[^<]*)(?:<td[^>]*>([^<]*)<\/td>[^<]*)(?:<td[^>]*>([^<]*)<\/td>[^<]*)<\/tr>',
                table_data):
            term, transcribe, definition = (word.groups())
            terms_entities[' '.join(term.strip().split()).lower()] = CreateTermAsTreeDTO(
                term=' '.join(term.strip().split()).lower(),
                definition=' '.join(definition.strip().split()).lower(),
                transcription=transcribe,
            )
            print(term, transcribe, definition)
    try:
        for sentences_html_piece in  re.findall(
            r'((?:(?:<div[^>]*?class=\"su-list\"[^>]*[^<]*)(?:\s*<div>\s*)?(?:<ul[^@]*?(?=<\/ul>)<\/ul>))[^<]*<blockquote[^@]*?(?=<\/blockquote>)<\/blockquote>[^@]*?</div>)',
            mystr
        ):
            print("sentences_html_piece", sentences_html_piece)

            print(sentences_html_piece)
            for sent_html in re.findall(
                    r'(?:<ul[^@]*?(?=<\/ul>)<\/ul>)[^<]*<blockquote[^@]*?<\/blockquote>', sentences_html_piece):
                print('-----')
                print(sent_html)
                try:
                    gr = re.search(
                        r"(?:<\/i>[^<]*?(?:<a[^>]*>[^<]*)?<strong[^>]*>(?:(?:<a[^>]*>([^<]*)<\/a>([^<]*)(?=</strong>)</strong>(?:[^<]*</a>)?([^—<&#8212–-]*)(?:—|&#8212;|&#8212|–|-))|(?:([^<]*)</strong>(?:[^<]*</a>)?(?:[^<]*<strong>)?([^—<&#8212–-]*)(?:(?:</strong>\s*)?(?:—|&#8212;|&#8212|–|-))))([^<]*)<\/li>)[^@]*?(?=<p)(<p[^<]*<\/p>[^@]*?)(?=<\/blockquote>)",
                        sent_html
                    ).groups()
                    main_term2, sub_terms2, _, main_term1, sub_terms1, definition, sentences_in_term = gr
                    main_term = main_term1 or main_term2
                    sub_terms = sub_terms1 or sub_terms2

                except AttributeError as e:
                    print(e)
                    is_ok = False
                    is_continue = False

                    while is_ok is False:
                        if sent_html in r_d:
                            main_term, sub_terms, definition, sentences_in_term = r_d[sent_html]
                            break
                        if is_continue:
                            break

                        print('Введите main_term')
                        main_term = input()
                        print('Введите sub_terms')
                        sub_terms = input()
                        print('Введите definition')
                        definition = input()
                        print('Введите sentences_in_term')
                        sentences_in_term = input()

                        is_ok = input("Введите 1 для подтверждения") == '1'

                    if is_continue:
                        continue

                print(main_term, sub_terms, definition, sentences_in_term)

                term = ((' '.join(
                    (main_term.strip() + (
                        " " + sub_terms.strip() if sub_terms and bool(sub_terms.strip()) else "")).split())
                         .lower())
                        .replace("( ", "(")
                        .replace(" )", ")"))
                if term in terms_entities:
                    terms_entities[term].sub_sentences = []
                elif term in bad_terms:
                    new_term = bad_terms[term]
                    terms_entities[new_term].sub_sentences = []
                    terms_entities[term] = terms_entities[new_term]
                else:
                    add_words(term, terms_entities)

                    print(terms_entities)
                    print(f'term {term} not in in terms_entities')
                    old_term = term

                    while term not in terms_entities:
                        print(f'term {term} not in in terms_entities')
                        term = input()

                    terms_entities[term].sub_sentences = []
                    terms_entities[old_term] = terms_entities[term]
                for sentence_ent in re.findall(
                        r'(?=<p)(?:<p[^>]*>([^&#8212\-\-\–]*).([^<]*))<\/p>',
                        sentences_in_term
                ):
                    print(sentence_ent)
                    sentence, translate = sentence_ent
                    print(sentence, translate)
                    terms_entities[term].sub_sentences += [
                        CreateSentenceAsTreeDTO(
                            sentence=' '.join(sentence.split()),
                            translate=' '.join(translate.split())
                        )
                    ]
    except AttributeError as e:
        print(e)
        # sentences_html_piece = input("Введите sentences_html_piece")
    return list(terms_entities.values())


async def main():
    res = await get_3000_words()
    async_session = async_sessionmaker(CONFIG.engine, expire_on_commit=False)
    async with async_session() as session:
        async with session.begin():
            await create_folder_as_tree([res], session, UserDTO(
                id=UUID("0a720d5e-af90-4ed3-b03b-e63d153f044d"),
                username='string',
                email='string',
                name='string',
                surname='surname',
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ))


if __name__ == '__main__':
    sent_html = '''
    <ul>
<li><i class="sui sui-circle" style="color:#feb431"></i> <strong><a href="https://langformula.ru/english-grammar/to-be/">be</a> (was, been)</strong> &#8212; быть</li>
</ul>
<blockquote><p>To be or not to be? – Быть или не быть?</p>
<p>Be careful – Будь осторожен</p></blockquote>
    '''

    sent_html2 = '''
    <ul>
<li><i class="sui sui-circle" style="color:#feb431"></i> <strong>become</strong> (became, become) &#8212; становиться</li>
</ul>
<blockquote><p>I want to become a vet – Я хочу стать ветеринаром</p>
<p>She became a good teacher – Она стала хорошим учителем</p></blockquote>
become  (became, become)  ; становиться <p>I want to become a vet – Я хочу стать ветеринаром</p>
<p>She became a good teacher – Она стала хорошим учителем</p>
    '''

    # gr = re.search(
    #     r"(?:<\/i>[^<]*?<strong[^>]*>(?:(?:<a[^>]*>([^<]*)<\/a>([^<]*)(?=</strong>)</strong>([^—<&#8212–-]*)(?:—|&#8212;|&#8212|–|-))|(?:([^<]*)</strong>([^—<&#8212–-]*)(?:—|&#8212;|&#8212|–|-)))([^<]*)<\/li>)[^@]*?(?=<p)(<p[^<]*<\/p>[^@]*?)(?=<\/blockquote>)",
    #     sent_html
    # ).groups()
    # print(gr)
    # main_term2, sub_terms2, _, main_term1, sub_terms1, definition, sentences_in_term = gr
    # main_term = main_term1 or main_term2
    # sub_terms = sub_terms1 or sub_terms2
    # print(main_term, sub_terms, definition, sentences_in_term)
    # get_words_from_words_page('https://langformula.ru/voc3000/nouns-job/')
    # asyncio.run(main())
    print(get_3000_words())

    # get_words_from_words_page('https://langformula.ru/voc3000/verbs-stages/')
