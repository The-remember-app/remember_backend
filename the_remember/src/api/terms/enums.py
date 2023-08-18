import enum

from the_remember.src.utils.db import AbstractPydanticEnum


class AddInfoTypeEnum(AbstractPydanticEnum):
    usual_term = "usual_term"
    other_form = 'other_form'  # указать что за форма
    help_phrase_with_word = 'help_phrase_with_word'  # написать фразу без этого слова
    help_phrase_without_word = 'help_phrase_without_word'  # указать до / после / без разницы
    # dialect_or_area = 'dialect_or_area'  # указать источник
    abbreviation = "abbreviation"
    composite_word = 'composite_word'  # указать номер составности
    sound = 'sound'
    transcription = 'transcription'


