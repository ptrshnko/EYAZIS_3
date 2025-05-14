import json

class SyntaxTree:
    """
    Класс для хранения синтаксического дерева предложения.
    """
    def __init__(self):
        """
        Инициализация пустого дерева.
        """
        self.nodes = {}

    def add_node(self, node_id, text, pos, head_id, rel):
        """
        Добавляет узел в синтаксическое дерево.

        Args:
            node_id (str): Уникальный идентификатор узла.
            text (str): Текст токена (слово).
            pos (str): Часть речи токена.
            head_id (str): ID родительского узла.
            rel (str): Тип синтаксической связи.
        """
        self.nodes[node_id] = {
            'text': text,
            'pos': pos,
            'head_id': head_id,
            'rel': rel
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