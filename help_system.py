from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton
from PyQt5.QtCore import Qt

def show_help():
    """
    Отображает окно справки с инструкциями по использованию программы.
    """
    dialog = QDialog()
    dialog.setWindowTitle("Справка по программе")
    dialog.setMinimumSize(500, 400)

    layout = QVBoxLayout()

    help_text = QTextEdit()
    help_text.setReadOnly(True)
    help_text.setText("""
    <h2>Справка по использованию программы</h2>
    <p>Эта программа предназначена для синтаксического и семантического анализа текста на русском языке из RTF-файлов.</p>
    <h3>Инструкции по использованию:</h3>
    <ul>
        <li><b>Загрузка файла:</b> Нажмите кнопку "Загрузить RTF" и выберите файл в формате RTF. Текст отобразится в текстовом поле.</li>
        <li><b>Анализ текста:</b> Нажмите кнопку "Анализировать" для выполнения анализа. Результаты появятся в виде дерева зависимостей.</li>
        <li><b>Просмотр результатов:</b> Дерево показывает Идентификатор, Слово, Часть речи, Член предложения, К какому слову относится, Лемму, Семантическую роль и Значение слова.</li>
        <li><b>Сохранение результатов:</b> Нажмите "Сохранить результаты" для экспорта в JSON-файл.</li>
        <li><b>Редактирование:</b> Дважды щелкните по узлу для Редактирования данных.</li>
        <li><b>Документирование:</b> Результаты можно экспортировать в текстовый формат через "Документировать".</li>
    </ul>
    <h3>Советы:</h3>
    <ul>
        <li>Убедитесь, что RTF-файл содержит текст на русском языке.</li>
        <li>При возникновении ошибок программа выдаст сообщение.</li>
        <li>Для больших текстов анализ может занять несколько секунд.</li>
    </ul>
    """)
    help_text.setStyleSheet("QTextEdit { font-size: 14px; padding: 10px; }")
    layout.addWidget(help_text)

    close_button = QPushButton("Закрыть")
    close_button.clicked.connect(dialog.accept)
    close_button.setStyleSheet("QPushButton { padding: 5px; }")
    layout.addWidget(close_button, alignment=Qt.AlignRight)

    dialog.setLayout(layout)
    dialog.exec_()