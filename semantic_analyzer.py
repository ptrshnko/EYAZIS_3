from pymorphy2 import MorphAnalyzer
from ruwordnet import RuWordNet

class SemanticAnalyzer:
    """
    Класс для выполнения семантического анализа текста с использованием RuWordNet.
    """
    def __init__(self):
        """
        Инициализация морфологического анализатора и RuWordNet.
        """
        self.morph = MorphAnalyzer()
        try:
            self.wn = RuWordNet()  # Инициализация RuWordNet
        except Exception as e:
            raise Exception(f"Ошибка инициализации RuWordNet: {str(e)}")

    def lemmatize(self, word):
        """
        Выполняет лемматизацию слова.

        Args:
            word (str): Входное слово.

        Returns:
            str: Лемма слова.
        """
        return self.morph.parse(word)[0].normal_form

    def determine_semantic_role(self, pos, rel):
        """
        Определяет семантическую роль на основе части речи и синтаксической связи.

        Args:
            pos (str): Часть речи.
            rel (str): Синтаксическая связь.

        Returns:
            str: Семантическая роль (или None, если не определена).
        """
        if rel == "подлежащее" and pos == "существительное":
            return "агент"
        elif rel == "дополнение" and pos == "существительное":
            return "пациент"
        elif rel == "сказуемое" and pos in ["глагол", "деепричастие"]:  # Добавляем деепричастие
            return "действие"
        elif rel == "косвенное дополнение" and pos == "существительное":
            return "место"
        elif rel == "определение" and pos == "прилагательное":
            return "характеристика"
        elif rel == "связка" and pos == "прилагательное":
            return "характеристика"
        elif rel == "падежный показатель" and pos == "предлог":
            return "указатель места"
        elif rel == "соединительный союз" and pos == "союз":
            return "связка"
        elif rel == "обстоятельство" and pos == "деепричастие":  # Деепричастие как обстоятельство
            return "действие"
        return None

    def get_word_meaning(self, lemma, pos, rel, text):
        """
        Возвращает значение слова на основе леммы, части речи, синтаксической связи и текста.

        Args:
            lemma (str): Лемма слова.
            pos (str): Часть речи.
            rel (str): Синтаксическая связь.
            text (str): Исходный текст токена.

        Returns:
            str: Значение слова (или "неизвестно", если не найдено).
        """
        lemma_lower = lemma.lower()
        text_lower = text.lower()

        # Пунктуация
        if pos == "пунктуация" or lemma == "." or lemma == ",":
            return "Знак препинания"

        # Имена собственные (проверяем заглавную букву и тег pymorphy2)
        parse = self.morph.parse(text)[0]
        if parse.tag and 'Name' in parse.tag and text[0].isupper():
            return "Имя собственное"

        # Извлечение значения из RuWordNet для существительных, глаголов, прилагательных, деепричастий
        if pos in ["существительное", "глагол", "прилагательное", "деепричастие"]:
            try:
                # Пробуем найти синсеты по лемме
                synsets = self.wn.get_synsets(lemma_lower)
                if not synsets:
                    # Если по лемме не найдено, пробуем исходное слово
                    synsets = self.wn.get_synsets(text_lower)
                # Проверяем все синсеты, выбираем первый с определением
                for synset in synsets:
                    if synset.definition:
                        # Приводим к нормальному регистру: первая буква заглавная
                        return synset.definition.capitalize()
                return "неизвестно"
            except Exception as e:
                print(f"Ошибка получения значения для леммы '{lemma}': {str(e)}")
                return "неизвестно"

        # Для остальных слов (предлоги, союзы, наречия) возвращаем "неизвестно"
        return "неизвестно"