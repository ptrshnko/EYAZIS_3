import json

class SyntaxTree:
    """
    Класс для хранения синтаксического и семантического дерева предложения.
    """
    def __init__(self):
        """
        Инициализация пустого дерева.
        """
        self.nodes = {}

    def add_node(self, node_id, text, pos, head_id, rel, lemma=None, semantic_role=None, word_meaning=None):
        """
        Добавляет узел в синтаксическое дерево с семантическими данными.

        Args:
            node_id (str): Уникальный идентификатор узла.
            text (str): Текст токена (слово).
            pos (str): Часть речи токена.
            head_id (str): ID родительского узла.
            rel (str): Тип синтаксической связи.
            lemma (str, optional): Лемма слова.
            semantic_role (str, optional): Семантическая роль.
            word_meaning (str, optional): Значение слова.
        """
        self.nodes[node_id] = {
            'text': text,
            'pos': pos,
            'head_id': head_id,
            'rel': rel,
            'lemma': lemma,
            'semantic_role': semantic_role,
            'word_meaning': word_meaning
        }

    def to_dict(self):
        """
        Возвращает дерево в виде словаря.

        Returns:
            dict: Словарь с узлами дерева.
        """
        return self.nodes

    def to_json(self):
        """
        Сериализует дерево в JSON-строку.

        Returns:
            str: JSON-представление дерева.
        """
        return json.dumps(self.nodes, ensure_ascii=False, indent=2)