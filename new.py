import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QHeaderView, QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QGridLayout, QDialog, QFormLayout, QDialogButtonBox, QComboBox, QDateEdit
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQueryModel, QSqlQuery
from PyQt5.QtCore import Qt, QDate


class MainWindow(QMainWindow):
    def __init__(self, cursor=None):
        super().__init__()

        # Инициализация базы данных
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('database.db')
        self.db.open()

        # Создание таблицы "Заказы"
        query = QSqlQuery()
        query.exec_("""
            CREATE TABLE IF NOT EXISTS Заказы (
                Номер_заказа INTEGER PRIMARY KEY,
                Номер_перевозчика INTEGER,
                Номер_заказчика INTEGER,
                Номер_транспорта INTEGER,
                Маршрут TEXT,
                Название_груза TEXT,
                Дата_загрузки TEXT,
                Дата_доставки TEXT,
                Статус TEXT
            )
        """)

        # Создание таблицы "Перевозчики"
        query.exec_("""
            CREATE TABLE IF NOT EXISTS Перевозчики (
                Номер_перевозчика INTEGER PRIMARY KEY,
                Контактное_лицо TEXT,
                Контактная_информация TEXT,
                Номер_транспорта INTEGER,
                Статус TEXT
            )
        """)

        # Создание таблицы "Транспорт"
        query.exec_("""
            CREATE TABLE IF NOT EXISTS Транспорт (
                Номер_транспорта INTEGER PRIMARY KEY,
                Номерной_знак TEXT,
                Название TEXT,
                Объем REAL,
                Статус TEXT
            )
        """)

        # Создание таблицы "Заказчики"
        query.exec_("""
            CREATE TABLE IF NOT EXISTS Заказчики (
                Номер_заказчика INTEGER PRIMARY KEY,
                Контактное_лицо TEXT,
                Контактная_информация TEXT,
                Номер_груза INTEGER
            )
        """)

        # Создание таблицы "Первая таблица"
        query.exec_("""
            CREATE TABLE IF NOT EXISTS Первая_таблица (
                Номер_заказа INTEGER PRIMARY KEY,
                Перевозчики INTEGER,
                Заказчики INTEGER,
                Транспорт INTEGER,
                Маршрут TEXT,
                Дата_доставки TEXT,
                Статус TEXT
            )
        """)
        # Вставка данных в таблицу "Заказы"
        query.exec_("""
                   INSERT INTO Заказы (Номер_заказа, Номер_перевозчика, Номер_заказчика, Номер_транспорта, Маршрут, 
                                      Название_груза, Дата_загрузки, Дата_доставки, Статус)
                   VALUES (1, 1, 1, 1, 'Маршрут 1', 'Груз 1', '2023-01-01', '2023-01-05', 'Доставлен')
               """)

        # Вставка данных в таблицу "Перевозчики"
        query.exec_("""
                   INSERT INTO Перевозчики (Номер_перевозчика, Контактное_лицо, Контактная_информация, Номер_транспорта, Статус)
                   VALUES (1, 'Контактное лицо 1', 'Информация о контакте 1', 1, 'Активен')
               """)

        # Вставка данных в таблицу "Транспорт"
        query.exec_("""
                   INSERT INTO Транспорт (Номер_транспорта, Номерной_знак, Название, Объем, Статус)
                   VALUES (1, 'ABC123', 'Транспортное средство 1', 100, 'Активен')
               """)

        # Вставка данных в таблицу "Заказчики"
        query.exec_("""
                   INSERT INTO Заказчики (Номер_заказчика, Контактное_лицо, Контактная_информация, Номер_груза)
                   VALUES (1, 'Контактное лицо 1', 'Информация о контакте 1', 1)
               """)

        # Вставка данных в таблицу "Первая таблица"
        query.exec_("""
                   INSERT INTO Первая_таблица (Номер_заказа, Перевозчики, Заказчики, Транспорт, Маршрут, Дата_доставки, Статус)
                   VALUES (1, 1, 1, 1, 'Маршрут 1', '2023-01-05', 'Доставлен')
               """)

        # Создание главного окна
        self.setWindowTitle('Информационная система для службы логистики')
        self.setMinimumSize(800, 600)

        # Создание виджета с таблицей "Первая таблица"
        self.first_table_widget = QTableView(self)
        self.first_table_widget.setSortingEnabled(True)
        self.first_table_widget.setSelectionBehavior(QTableView.SelectRows)
        self.first_table_widget.setSelectionMode(QTableView.SingleSelection)
        self.first_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.first_table_widget.verticalHeader().setVisible(False)
        self.setCentralWidget(self.first_table_widget)

        # Создание строки поиска
        self.search_line_edit = QLineEdit(self)
        self.search_line_edit.setPlaceholderText('Поиск по номеру заказа')
        self.search_line_edit.returnPressed.connect(self.search_order)
        self.search_button = QPushButton('Найти', self)
        self.search_button.clicked.connect(self.search_order)

        # Создание
        # Создание кнопок "Заказы", "Перевозчики", "Транспорт"
        self.orders_button = QPushButton('Заказы', self)
        self.orders_button.clicked.connect(self.show_orders)
        self.carriers_button = QPushButton('Перевозчики', self)
        self.carriers_button.clicked.connect(self.show_carriers)
        self.transport_button = QPushButton('Транспорт', self)
        self.transport_button.clicked.connect(self.show_transport)

        # Размещение элементов интерфейса
        self.toolbar = self.addToolBar('Toolbar')
        self.toolbar.addWidget(self.search_line_edit)
        self.toolbar.addWidget(self.search_button)
        self.toolbar.addWidget(self.orders_button)
        self.toolbar.addWidget(self.carriers_button)
        self.toolbar.addWidget(self.transport_button)

        # Создание модели данных для таблицы "Первая таблица"
        self.first_table_model = QSqlTableModel(self)
        self.first_table_model.setTable('Первая_таблица')
        self.first_table_model.select()
        self.first_table_widget.setModel(self.first_table_model)

    def search_order(self):
        order_number = self.search_line_edit.text()
        if order_number:
            query = QSqlQuery(f"SELECT * FROM Первая_таблица WHERE Номер_заказа = {order_number}")
            if query.next():
                row = query.record()
                self.first_table_widget.selectRow(row.row())
            else:
                QMessageBox.information(self, 'Поиск заказа', 'Заказ не найден.')

    def show_orders(self):
        orders_dialog = OrdersDialog(self)
        orders_dialog.exec_()

    def show_carriers(self):
        carriers_dialog = CarriersDialog(self)
        carriers_dialog.exec_()

    def show_transport(self):
        transport_dialog = TransportDialog(self)
        transport_dialog.exec_()


class OrdersDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Заказы')
        self.setMinimumSize(800, 600)

        self.orders_table_widget = QTableView(self)
        self.orders_table_widget.setSelectionBehavior(QTableView.SelectRows)
        self.orders_table_widget.setSelectionMode(QTableView.SingleSelection)
        self.orders_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.orders_table_widget.verticalHeader().setVisible(False)
        layout = QVBoxLayout(self)
        layout.addWidget(self.orders_table_widget)

        self.add_button = QPushButton('Добавить', self)
        self.add_button.clicked.connect(self.add_order)
        self.delete_button = QPushButton('Удалить', self)
        self.delete_button.clicked.connect(self.delete_order)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.delete_button)
        layout.addLayout(buttons_layout)

        self.orders_model = QSqlTableModel(self)
        self.orders_model.setTable('Заказы')
        self.orders_model.select()
        self.orders_table_widget.setModel(self.orders_model)

    def add_order(self):
        order_number = self.order_number_line_edit.text()
        customer = self.customer_line_edit.text()
        route = self.route_line_edit.text()
        delivery_date = self.delivery_date_edit.date().toString("yyyy-MM-dd")
        loading_date = self.loading_date_edit.date().toString("yyyy-MM-dd")
        status = "В пути"  # Setting the initial status here, you can change it as needed

        # Fetch the database connection
        db = QSqlDatabase.database("database.db")
        if not db.isValid():
            QMessageBox.critical(self, "Database Error", "Failed to access the database.")
            return

        # Prepare the SQL query to insert a new row in the "Orders" table
        query = QSqlQuery(db)
        query.prepare(
            "INSERT INTO Orders (order_number, customer, route, delivery_date, loading_date, status)"
            "VALUES (?, ?, ?, ?, ?, ?)"
        )
        query.addBindValue(order_number)
        query.addBindValue(customer)
        query.addBindValue(route)
        query.addBindValue(delivery_date)
        query.addBindValue(loading_date)
        query.addBindValue(status)

        # Execute the SQL query
        if query.exec():
            QMessageBox.information(self, "Добавление заказа", "Заказ успешно добавлен в базу данных.")
        else:
            QMessageBox.warning(self, "Добавление заказа", "Ошибка при добавлении заказа в базу данных.")

    def delete_order(self):
        selected_index = self.orders_table_widget.selectedIndexes()
        if selected_index:
            row = selected_index[0].row()
            self.orders_model.removeRow(row)
            self.orders_model.submitAll()

        else:
            QMessageBox.warning(self, 'Удаление заказа', 'Выберите заказ для удаления.')


class CarriersDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Перевозчики')
        self.setMinimumSize(800, 600)

        self.carriers_table_widget = QTableView(self)
        self.carriers_table_widget.setSelectionBehavior(QTableView.SelectRows)
        self.carriers_table_widget.setSelectionMode(QTableView.SingleSelection)
        self.carriers_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.carriers_table_widget.verticalHeader().setVisible(False)
        layout = QVBoxLayout(self)
        layout.addWidget(self.carriers_table_widget)

        self.add_button = QPushButton('Добавить', self)
        self.add_button.clicked.connect(self.add_carrier)
        self.delete_button = QPushButton('Удалить', self)
        self.delete_button.clicked.connect(self.delete_carrier)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.delete_button)
        layout.addLayout(buttons_layout)

        self.carriers_model = QSqlTableModel(self)
        self.carriers_model.setTable('Перевозчики')
        self.carriers_model.select()
        self.carriers_table_widget.setModel(self.carriers_model)

    def add_carrier(self):
        # В
        # Ваш код для добавления новой строки в таблицу "Перевозчики" и сохранения в базу данных
        pass

    def delete_carrier(self):
        selected_index = self.carriers_table_widget.selectedIndexes()
        if selected_index:
            row = selected_index[0].row()
            self.carriers_model.removeRow(row)
            self.carriers_model.submitAll()

        else:
            QMessageBox.warning(self, 'Удаление перевозчика', 'Выберите перевозчика для удаления.')

class TransportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Транспорт')
        self.setMinimumSize(800, 600)

        self.transport_table_widget = QTableView(self)
        self.transport_table_widget.setSelectionBehavior(QTableView.SelectRows)
        self.transport_table_widget.setSelectionMode(QTableView.SingleSelection)
        self.transport_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.transport_table_widget.verticalHeader().setVisible(False)
        layout = QVBoxLayout(self)
        layout.addWidget(self.transport_table_widget)

        self.add_button = QPushButton('Добавить', self)
        self.add_button.clicked.connect(self.add_transport)
        self.delete_button = QPushButton('Удалить', self)
        self.delete_button.clicked.connect(self.delete_transport)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.delete_button)
        layout.addLayout(buttons_layout)

        self.transport_model = QSqlTableModel(self)
        self.transport_model.setTable('Транспорт')
        self.transport_model.select()
        self.transport_table_widget.setModel(self.transport_model)

    def add_transport(self):
        # Ваш код для добавления новой строки в таблицу "Транспорт" и сохранения в базу данных
        pass

    def delete_transport(self):
        selected_index = self.transport_table_widget.selectedIndexes()
        if selected_index:
            row = selected_index[0].row()
            self.transport_model.removeRow(row)
            self.transport_model.submitAll()

        else:
            QMessageBox.warning(self, 'Удаление транспорта', 'Выберите транспорт для удаления.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
