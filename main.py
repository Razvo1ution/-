import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableWidget, QTableWidgetItem
from qt_material import apply_stylesheet
import sqlite3

class DatabaseApp(QMainWindow):
    def __init__(self, db_file):
        super().__init__()
        self.db_file = db_file
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Пример работы с базой данных')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.tableWidget = QTableWidget()
        layout.addWidget(self.tableWidget)

        button1 = QPushButton('Показать таблицу 1')
        button1.clicked.connect(self.show_table1)
        layout.addWidget(button1)

        button2 = QPushButton('Показать таблицу 2')
        button2.clicked.connect(self.show_table2)
        layout.addWidget(button2)

        button3 = QPushButton('Показать таблицу 3')
        button3.clicked.connect(self.show_table3)
        layout.addWidget(button3)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def show_table1(self):
        self.show_table('Заказы')  # Замените 'table1_name' на имя вашей первой таблицы

    def show_table2(self):
        self.show_table('Перевозчики')  # Замените 'table2_name' на имя вашей второй таблицы

    def show_table3(self):
        self.show_table('Тип_транспорта')  # Замените 'table3_name' на имя вашей третьей таблицы

    def show_table(self, table_name):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]

        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()

        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(columns))

        self.tableWidget.setHorizontalHeaderLabels(columns)

        for row, row_data in enumerate(data):
            for col, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tableWidget.setItem(row, col, item)

        self.tableWidget.resizeColumnsToContents()  # Автоматическое изменение размеров столбцов
        connection.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DatabaseApp('Orders.db')  # Замените путь_к_вашей_базе_данных.db на путь к вашему файлу базы данных
    window.show()
    sys.exit(app.exec_())
