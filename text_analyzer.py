from natasha import Segmenter, NewsEmbedding, NewsSyntaxParser, Doc
from pymorphy2 import MorphAnalyzer
from data_structures import SyntaxTree
from pos_rel_translations import translate_pos, translate_rel
from semantic_analyzer import SemanticAnalyzer
import time

class TextAnalyzer:
    """
    Класс для выполнения синтаксического и семантического анализа текста на русском языке.
    """
    def __init__(self):
        """
        Инициализация компонентов Natasha, pymorphy2 и семантического анализатора.
        """
        try:
            self.segmenter = Segmenter()
            self.morph = MorphAnalyzer()
            self.emb = NewsEmbedding()
            self.syntax_parser = NewsSyntaxParser(self.emb)
            self.semantic_analyzer = SemanticAnalyzer()
        except Exception as e:
            raise Exception(f"Ошибка инициализации: {str(e)}")

    def analyze(self, text):
        """
        Выполняет синтаксический и семантический анализ текста.

        Args:
            text (str): Входной текст для анализа.

        Returns:
            list: Список объектов SyntaxTree, представляющих деревья для каждого предложения.

        Raises:
            ValueError: Если входной текст пустой.
            Exception: Если произошла ошибка при анализе.
        """
        try:
            start_time = time.time()
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
                    parse = self.morph.parse(token.text)[0]
                    token.pos = parse.tag.POS

            # Синтаксический анализ
            doc.parse_syntax(self.syntax_parser)

            # Формирование списка синтаксических деревьев с переводом тегов и семантикой
            results = []
            for sent in doc.sents:
                tree = SyntaxTree()
                sentence_text = sent.text
                for token in sent.tokens:
                    pos = translate_pos(token.pos)
                    rel = translate_rel(token.rel)
                    lemma = self.semantic_analyzer.lemmatize(token.text)
                    semantic_role = self.semantic_analyzer.determine_semantic_role(pos, rel)
                    word_meaning = self.semantic_analyzer.get_word_meaning(lemma, pos, rel, token.text)
                    tree.add_node(
                        node_id=token.id,
                        text=token.text,
                        pos=pos,
                        head_id=token.head_id,
                        rel=rel,
                        lemma=lemma,
                        semantic_role=semantic_role,
                        word_meaning=word_meaning
                    )
                results.append(tree)
            
            print(f"Время анализа: {time.time() - start_time} секунд")
            return results

        except Exception as e:
            raise Exception(f"Ошибка при синтаксическом анализе: {str(e)}")