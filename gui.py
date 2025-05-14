from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTextEdit, QTreeWidget, QTreeWidgetItem, QFileDialog,
                             QMessageBox, QMenuBar, QDialog, QFormLayout, QLineEdit, QDialogButtonBox)
from PyQt5.QtCore import Qt
from rtf_reader import read_rtf_file
from text_analyzer import TextAnalyzer
from result_manager import ResultManager
from help_system import show_help
from pos_rel_translations import translate_pos, translate_rel

class MainWindow(QMainWindow):
    """
    Основное окно приложения для синтаксического и семантического анализа текста.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Синтаксический и семантический анализатор текста")
        self.setGeometry(100, 100, 1200, 600)
        self.analyzer = TextAnalyzer()
        self.result_manager = ResultManager()
        self.current_results = []
        self.init_ui()
        self.setAcceptDrops(True)

    def init_ui(self):
        """
        Инициализация пользовательского интерфейса.
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Меню
        menubar = self.menuBar()
        help_menu = menubar.addMenu("Справка")
        help_action = help_menu.addAction("Открыть справку")
        help_action.triggered.connect(show_help)

        # Панель кнопок
        button_layout = QHBoxLayout()
        load_btn = QPushButton("Загрузить RTF")
        load_btn.clicked.connect(self.load_file)
        analyze_btn = QPushButton("Анализировать")
        analyze_btn.clicked.connect(self.analyze_text)
        save_btn = QPushButton("Сохранить результаты (JSON)")
        save_btn.clicked.connect(self.save_results)
        doc_btn = QPushButton("Документировать (TXT)")
        doc_btn.clicked.connect(self.document_results)
        for btn in [load_btn, analyze_btn, save_btn, doc_btn]:
            btn.setStyleSheet("QPushButton { padding: 5px; font-size: 14px; }")
            button_layout.addWidget(btn)
        main_layout.addLayout(button_layout)

        # Текстовое поле для исходного текста
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Загрузите RTF-файл или введите текст для анализа")
        self.text_edit.setStyleSheet("QTextEdit { font-size: 14px; padding: 10px; }")
        main_layout.addWidget(self.text_edit)

        # Дерево для отображения результатов анализа
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels([
            "Идентификатор", "Слово", "Часть речи", "Член предложения", 
            "К какому слову относится", "Лемма", "Семантическая роль", 
            "Тип лексического значения", "Значение слова"
        ])
        self.tree_widget.setStyleSheet("QTreeWidget { font-size: 14px; }")
        self.tree_widget.setColumnWidth(0, 50)
        self.tree_widget.setColumnWidth(1, 100)
        self.tree_widget.setColumnWidth(2, 100)
        self.tree_widget.setColumnWidth(3, 100)
        self.tree_widget.setColumnWidth(4, 100)
        self.tree_widget.setColumnWidth(5, 100)
        self.tree_widget.setColumnWidth(6, 120)
        self.tree_widget.setColumnWidth(7, 120)
        self.tree_widget.setColumnWidth(8, 150)
        self.tree_widget.itemDoubleClicked.connect(self.edit_node)
        main_layout.addWidget(self.tree_widget)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith('.rtf'):
                self.load_file(file_path)
                event.accept()
                return
        QMessageBox.warning(self, "Ошибка", "Перетаскивайте только RTF-файлы")

    def load_file(self, file_path=None):
        if not file_path:
            file_path, _ = QFileDialog.getOpenFileName(self, "Выберите RTF-файл", "", "RTF Files (*.rtf)")
        if file_path:
            try:
                text = read_rtf_file(file_path)
                self.text_edit.setText(text)
                self.tree_widget.clear()
                self.current_results = []
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def analyze_text(self):
        text = self.text_edit.toPlainText()
        if not text:
            QMessageBox.warning(self, "Предупреждение", "Загрузите или введите текст для анализа")
            return
        try:
            self.current_results = self.analyzer.analyze(text)
            self.display_results(self.current_results)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка анализа: {str(e)}")

    def display_results(self, results):
        self.tree_widget.clear()
        for i, tree in enumerate(results):
            root = QTreeWidgetItem(self.tree_widget, [f"Предложение {i+1}", "", "", "", "", "", "", "", ""])
            for node_id, node in tree.to_dict().items():
                item = QTreeWidgetItem(root, [
                    node_id,
                    node['text'],
                    node['pos'],
                    node['rel'],
                    node['head_id'],
                    node.get('lemma', ''),
                    node.get('semantic_role', ''),
                    node.get('lexical_type', ''),
                    node.get('word_meaning', '')
                ])
                item.setData(0, Qt.UserRole, (i, node_id))
            root.setExpanded(True)

    def edit_node(self, item, column):
        if item.text(0).startswith("Предложение"):
            return
        sentence_index, node_id = item.data(0, Qt.UserRole)
        current_pos = item.text(2)
        current_rel = item.text(3)
        current_head_id = item.text(4)
        current_lemma = item.text(5)
        current_semantic_role = item.text(6)
        current_lexical_type = item.text(7)
        current_word_meaning = item.text(8)

        dialog = QDialog(self)
        dialog.setWindowTitle("Редактировать узел")
        layout = QFormLayout()

        pos_edit = QLineEdit(current_pos)
        rel_edit = QLineEdit(current_rel)
        head_id_edit = QLineEdit(current_head_id)
        lemma_edit = QLineEdit(current_lemma)
        semantic_role_edit = QLineEdit(current_semantic_role)
        lexical_type_edit = QLineEdit(current_lexical_type)
        word_meaning_edit = QLineEdit(current_word_meaning)

        layout.addRow("Часть речи:", pos_edit)
        layout.addRow("Член предложения:", rel_edit)
        layout.addRow("К какому слову относится (ID):", head_id_edit)
        layout.addRow("Лемма:", lemma_edit)
        layout.addRow("Семантическая роль:", semantic_role_edit)
        layout.addRow("Тип лексического значения:", lexical_type_edit)
        layout.addRow("Значение слова:", word_meaning_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.setLayout(layout)

        if dialog.exec_():
            try:
                new_pos = translate_pos(pos_edit.text().strip()) if pos_edit.text().strip() else None
                new_rel = translate_rel(rel_edit.text().strip()) if rel_edit.text().strip() else None
                new_head_id = head_id_edit.text().strip() or None
                new_lemma = lemma_edit.text().strip() or None
                new_semantic_role = semantic_role_edit.text().strip() or None
                new_lexical_type = lexical_type_edit.text().strip() or None
                new_word_meaning = word_meaning_edit.text().strip() or None
                self.current_results = self.result_manager.edit_result(
                    self.current_results, sentence_index, node_id,
                    new_head_id=new_head_id, new_rel=new_rel, new_pos=new_pos,
                    new_lemma=new_lemma, new_semantic_role=new_semantic_role,
                    new_lexical_type=new_lexical_type, new_word_meaning=new_word_meaning
                )
                self.display_results(self.current_results)
                QMessageBox.information(self, "Успех", "Узел успешно отредактирован")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка редактирования: {str(e)}")

    def save_results(self):
        if not self.current_results:
            QMessageBox.warning(self, "Предупреждение", "Нет результатов для сохранения")
            return
        try:
            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить результаты", "", "JSON Files (*.json)")
            if file_path:
                if not file_path.lower().endswith('.json'):
                    file_path += '.json'
                self.result_manager.save_results(self.current_results, file_path)
                QMessageBox.information(self, "Успех", "Результаты сохранены в JSON")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка сохранения: {str(e)}")

    def document_results(self):
        if not self.current_results:
            QMessageBox.warning(self, "Предупреждение", "Нет результатов для документирования")
            return
        try:
            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить документацию", "", "Text Files (*.txt)")
            if file_path:
                if not file_path.lower().endswith('.txt'):
                    file_path += '.txt'
                self.result_manager.document_results(self.current_results, file_path)
                QMessageBox.information(self, "Успех", "Результаты задокументированы в TXT")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка документирования: {str(e)}")