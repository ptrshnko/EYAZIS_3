import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow
import time

def main():
    """
    Основная функция для запуска приложения с замером времени.
    """
    app = QApplication(sys.argv)
    start_time = time.time()
    window = MainWindow()
    window.show()
    print(f"Время запуска интерфейса: {time.time() - start_time} секунд")
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()