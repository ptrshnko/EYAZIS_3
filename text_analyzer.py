from natasha import Segmenter, NewsEmbedding, NewsSyntaxParser, Doc
from pymorphy2 import MorphAnalyzer
from data_structures import SyntaxTree
from pos_rel_translations import translate_pos, translate_rel

class TextAnalyzer:
    """
    Класс для выполнения синтаксического анализа текста на русском языке с использованием Natasha и pymorphy2.
    """
    def __init__(self):
        """
        Инициализация компонентов Natasha и pymorphy2 для обработки текста.
        """
        try:
            self.segmenter = Segmenter()
            self.morph = MorphAnalyzer()
            self.emb = NewsEmbedding()
            self.syntax_parser = NewsSyntaxParser(self.emb)
        except Exception as e:
            raise Exception(f"Ошибка инициализации: {str(e)}")

    def analyze(self, text):
        """
        Выполняет синтаксический анализ текста.

        Args:
            text (str): Входной текст для анализа.

        Returns:
            list: Список объектов SyntaxTree, представляющих синтаксические деревья для каждого предложения.

        Raises:
            ValueError: Если входной текст пустой.
            Exception: Если произошла ошибка при анализе.
        """
        try:
            # Проверка на пустой текст
            if not text or not text.strip():
                raise ValueError("Входной текст пуст")

            # Создание объекта Doc для обработки текста
            doc = Doc(text)
            
            # Сегментация текста на предложения
            doc.segment(self.segmenter)
            
            # Морфологический анализ с использованием pymorphy2
            for sent in doc.sents:
                for token in sent.tokens:
                    parse = self.morph.parse(token.text)[0]  # Берем первую разборку
                    token.pos = parse.tag.POS  # Устанавливаем часть речи
                    token.tag = parse.tag  # Дополнительно сохраняем тег для совместимости

            # Синтаксический анализ
            doc.parse_syntax(self.syntax_parser)

            # Формирование списка синтаксических деревьев с переводом тегов
            results = []
            for sent in doc.sents:
                tree = SyntaxTree()
                for token in sent.tokens:
                    tree.add_node(
                        node_id=token.id,
                        text=token.text,
                        pos=translate_pos(token.pos),  # Перевод части речи
                        head_id=token.head_id,
                        rel=translate_rel(token.rel)   # Перевод связи
                    )
                results.append(tree)
            
            return results

        except Exception as e:
            raise Exception(f"Ошибка при синтаксическом анализе: {str(e)}")