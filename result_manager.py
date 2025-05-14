import json
import os
from data_structures import SyntaxTree

class ResultManager:
    """
    Класс для управления результатами синтаксического и семантического анализа.
    """
    def save_results(self, results, file_path):
        """
        Сохраняет результаты анализа в JSON-файл.
        """
        try:
            if not results:
                raise ValueError("Результаты анализа пусты")
            if not file_path.lower().endswith('.json'):
                if not file_path.endswith('.'):
                    file_path += '.json'
                else:
                    file_path += 'json'

            data = [tree.to_dict() for tree in results]
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise Exception(f"Ошибка при сохранении результатов: {str(e)}")

    def load_results(self, file_path):
        """
        Загружает результаты анализа из JSON-файла.
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

            results = []
            for tree_data in data:
                tree = SyntaxTree()
                for node_id, node in tree_data.items():
                    tree.add_node(
                        node_id=node_id,
                        text=node['text'],
                        pos=node['pos'],
                        head_id=node['head_id'],
                        rel=node['rel'],
                        lemma=node.get('lemma'),
                        semantic_role=node.get('semantic_role'),
                        word_meaning=node.get('word_meaning')
                    )
                results.append(tree)
            
            return results
        except Exception as e:
            raise Exception(f"Ошибка при загрузке результатов: {str(e)}")

    def document_results(self, results, file_path):
        """
        Документирует результаты в текстовом формате для отчета.
        """
        try:
            if not results:
                raise ValueError("Результаты анализа пусты")
            if not file_path.lower().endswith('.txt'):
                if not file_path.endswith('.'):
                    file_path += '.txt'
                else:
                    file_path += 'txt'

            with open(file_path, 'w', encoding='utf-8') as f:
                for i, tree in enumerate(results):
                    f.write(f"Предложение {i+1}:\n")
                    for node_id, node in tree.to_dict().items():
                        f.write(
                            f"  ID: {node_id}, Слово: {node['text']}, "
                            f"Часть речи: {node['pos']}, Член предложения: {node['rel']}, "
                            f"К какому слову относится: {node['head_id']}, "
                            f"Лемма: {node.get('lemma', '')}, Семантическая роль: {node.get('semantic_role', '')}, "
                            f"Значение слова: {node.get('word_meaning', '')}\n"
                        )
                    f.write("\n")
        except Exception as e:
            raise Exception(f"Ошибка при документировании результатовlift: {str(e)}")

    def edit_result(self, results, sentence_index, node_id, new_head_id=None, new_rel=None, new_pos=None, 
                    new_lemma=None, new_semantic_role=None, new_word_meaning=None):
        """
        Редактирует параметры узла в дереве анализа.
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
            if new_lemma is not None:
                tree.nodes[node_id]['lemma'] = new_lemma
            if new_semantic_role is not None:
                tree.nodes[node_id]['semantic_role'] = new_semantic_role
            if new_word_meaning is not None:
                tree.nodes[node_id]['word_meaning'] = new_word_meaning
            
            return results
        except Exception as e:
            raise Exception(f"Ошибка при редактировании результатов: {str(e)}")