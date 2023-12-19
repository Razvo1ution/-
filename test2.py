import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableWidget, \
    QTableWidgetItem, QHeaderView
from qt_material import apply_stylesheet
import sqlite3


class TableWindow(QMainWindow):
    def __init__(self, table_name, db_file):
        super().__init__()
        self.table_name = table_name
        self.db_file = db_file
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f'{self.table_name}')
        self.setGeometry(100, 100, 600, 400)
        self.resize(1280, 720)
        self.setMinimumSize(1280, 720)
        self.setMaximumSize(1280, 720)
        self.setGeometry(320, 180, 1280, 720)

        layout = QVBoxLayout()

        self.tableWidget = QTableWidget()
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget.setFixedSize(1000, 900)  # Размер таблицы, можно изменить на нужный
        self.tableWidget.setGeometry(240, 60, 1000, 900)  # Позиция таблицы в окне
        self.tableWidget.move(240, 60)
        layout.addWidget(self.tableWidget)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        self.show_table()

    def show_table(self):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute(f"PRAGMA table_info({self.table_name})")
        columns = [col[1] for col in cursor.fetchall()]  # Получаем названия столбцов

        cursor.execute(f"SELECT * FROM {self.table_name}")
        data = cursor.fetchall()

        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(columns))

        self.tableWidget.setHorizontalHeaderLabels(columns)  # Устанавливаем заголовки столбцов

        for row, row_data in enumerate(data):
            for col, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tableWidget.setItem(row, col, item)

        self.tableWidget.resizeColumnsToContents()  # Автоматическое изменение размеров столбцов
        connection.close()

class DatabaseApp(QMainWindow):
    def __init__(self, db_file):
        super().__init__()
        self.db_file = db_file
        self.table_windows = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Информационная система службы логистики')
        self.setGeometry(320, 180, 1280, 720)

        layout = QVBoxLayout()

        button1 = QPushButton('Заказы')
        button1.clicked.connect(lambda: self.show_table_window('Заказы'))
        button1.setStyleSheet("width: 120px; height: 80px; max-width: 120px;")
        layout.addWidget(button1)

        button2 = QPushButton('Перевозчики')
        button2.clicked.connect(lambda: self.show_table_window('Перевозчики'))
        button2.setStyleSheet("width: 120px; height: 80px; max-width: 120px;")
        layout.addWidget(button2)

        button3 = QPushButton('Тип транспорта')
        button3.clicked.connect(lambda: self.show_table_window('Тип_транспорта'))
        button3.setStyleSheet("width: 120px; height: 80px; max-width: 120px;")
        layout.addWidget(button3)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def show_table_window(self, table_name):
        table_window = TableWindow(table_name, self.db_file)
        self.table_windows.append(table_window)
        table_window.show()  # Показываем окно

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DatabaseApp('Логистика v2.db')
    apply_stylesheet(app, theme='dark_teal.xml')
    window.show()
    sys.exit(app.exec_())