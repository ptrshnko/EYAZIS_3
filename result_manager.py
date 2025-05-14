import json
import os
from data_structures import SyntaxTree

class ResultManager:
    """
    Класс для управления результатами синтаксического анализа: сохранение, загрузка и редактирование.
    """
    def save_results(self, results, file_path):
        """
        Сохраняет результаты синтаксического анализа в JSON-файл.

        Args:
            results (list): Список объектов SyntaxTree с результатами анализа.
            file_path (str): Путь к файлу для сохранения.

        Raises:
            ValueError: Если результаты пусты или путь к файлу некорректен.
            Exception: Если произошла ошибка при сохранении.
        """
        try:
            if not results:
                raise ValueError("Результаты анализа пусты")
            if not file_path.lower().endswith('.json'):
                raise ValueError("Файл должен быть в формате JSON")

            # Преобразование результатов в список словарей
            data = [tree.to_dict() for tree in results]
            
            # Сохранение в JSON
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        
        except Exception as e:
            raise Exception(f"Ошибка при сохранении результатов: {str(e)}")

    def load_results(self, file_path):
        """
        Загружает результаты синтаксического анализа из JSON-файла.

        Args:
            file_path (str): Путь к JSON-файлу.

        Returns:
            list: Список объектов SyntaxTree.

        Raises:
            FileNotFoundError: Если файл не найден.
            ValueError: Если файл пуст или некорректен.
            Exception: Если произошла ошибка при загрузке.
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Файл {file_path} не найден")
            if not file_path.lower().endswith('.json'):
                raise ValueError("Файл должен быть в формате JSON")

            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not data:
                raise ValueError("Файл JSON пуст")

            # Преобразование данных в список объектов SyntaxTree
            results = []
            for tree_data in data:
                tree = SyntaxTree()
                for node_id, node in tree_data.items():
                    tree.add_node(
                        node_id=node_id,
                        text=node['text'],
                        pos=node['pos'],
                        head_id=node['head_id'],
                        rel=node['rel']
                    )
                results.append(tree)
            
            return results
        
        except Exception as e:
            raise Exception(f"Ошибка при загрузке результатов: {str(e)}")

    def document_results(self, results, file_path):
        """
        Документирует результаты в текстовом формате для отчета.

        Args:
            results (list): Список объектов SyntaxTree.
            file_path (str): Путь к текстовому файлу для сохранения.

        Raises:
            ValueError: Если результаты пусты или путь к файлу некорректен.
            Exception: Если произошла ошибка при сохранении.
        """
        try:
            if not results:
                raise ValueError("Результаты анализа пусты")
            if not file_path.lower().endswith('.txt'):
                raise ValueError("Файл должен быть в формате TXT")

            with open(file_path, 'w', encoding='utf-8') as f:
                for i, tree in enumerate(results):
                    f.write(f"Предложение {i+1}:\n")
                    for node_id, node in tree.to_dict().items():
                        f.write(
                            f"  ID: {node_id}, Слово: {node['text']}, "
                            f"Часть речи: {node['pos']}, Связь: {node['rel']}, "
                            f"Родитель: {node['head_id']}\n"
                        )
                    f.write("\n")
        
        except Exception as e:
            raise Exception(f"Ошибка при документировании результатов: {str(e)}")

    def edit_result(self, results, sentence_index, node_id, new_head_id=None, new_rel=None, new_pos=None):
        """
        Редактирует параметры узла в дереве синтаксического анализа.

        Args:
            results (list): Список объектов SyntaxTree.
            sentence_index (int): Индекс предложения в списке результатов.
            node_id (str): ID узла для редактирования.
            new_head_id (str, optional): Новый ID родительского узла.
            new_rel (str, optional): Новый тип синтаксической связи.
            new_pos (str, optional): Новая часть речи.

        Returns:
            list: Обновленный список объектов SyntaxTree.

        Raises:
            ValueError: Если параметры некорректны.
        """
        try:
            if not (0 <= sentence_index < len(results)):
                raise ValueError("Некорректный индекс предложения")
            tree = results[sentence_index]
            if node_id not in tree.nodes:
                raise ValueError(f"Узел с ID {node_id} не найден")

            if new_head_id is not None:
                tree.nodes[node_id]['head_id'] = new_head_id
            if new_rel is not None:
                tree.nodes[node_id]['rel'] = new_rel
            if new_pos is not None:
                tree.nodes[node_id]['pos'] = new_pos
            
            return results
        
        except Exception as e:
            raise Exception(f"Ошибка при редактировании результатов: {str(e)}")