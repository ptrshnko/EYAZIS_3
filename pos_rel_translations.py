from enum import Enum

class PosTranslation(Enum):
    """Перевод частей речи на русский язык."""
    NOUN = "существительное"
    VERB = "глагол"
    ADJF = "прилагательное"
    ADVB = "наречие"
    PREP = "предлог"
    PRTF = "причастие"
    PRTS = "деепричастие"
    CONJ = "союз"
    PUNCT = "пунктуация"
    UNKNOWN = " "

class RelTranslation(Enum):
    """Перевод синтаксических связей на русский язык."""
    nsubj = "подлежащее"
    root = "сказуемое"
    amod = "определение"
    obj = "дополнение"
    punct = "пунктуация"
    acl = "придаточное"
    case = "падежный показатель"
    obl = "косвенное дополнение"
    conj = "связка"
    advmod = "обстоятельство"
    cc = "соединительный союз"  # Добавлен новый тег
    UNKNOWN = "неизвестно"

def translate_pos(pos):
    """Переводит часть речи на русский язык."""
    return PosTranslation[pos.upper() if pos else "UNKNOWN"].value if pos else PosTranslation.UNKNOWN.value

def translate_rel(rel):
    """Переводит синтаксическую связь на русский язык."""
    try:
        return RelTranslation[rel.lower() if rel else "UNKNOWN"].value
    except KeyError:
        return RelTranslation.UNKNOWN.value  # Обработка неизвестных тегов