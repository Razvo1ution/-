import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget

class OrderWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список заказов")
        self.setGeometry(630, 315, 640, 480)

        # Создаем виджеты
        self.search_label = QLabel("Поиск:")
        self.search_box = QLineEdit()
        self.search_button = QPushButton("Найти")
        self.order_list = QListWidget()
        self.drivers_button = QPushButton("Водители")
        self.orders_button = QPushButton("Заказы")
        self.history_button = QPushButton("История заказов")

        # Создаем главный виджет и компонуем его
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # Создаем виджет для строки поиска и кнопки
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_label)
        search_layout.addWidget(self.search_box)
        search_layout.addWidget(self.search_button)

        main_layout.addLayout(search_layout)

        # Создаем виджет для списка заказов
        main_layout.addWidget(self.order_list)

        # Создаем виджет для кнопок
        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.drivers_button)
        buttons_layout.addWidget(self.orders_button)
        buttons_layout.addWidget(self.history_button)

        main_layout.addLayout(buttons_layout)

        # Устанавливаем главный виджет в окне
        self.setCentralWidget(central_widget)

class DriversWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список водителей")

class OrdersWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список заказов")

class HistoryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("История заказов")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Создаем и отображаем главное окно
    main_window = OrderWindow()
    main_window.show()

    # Создаем экземпляры окон для кнопок
    drivers_window = DriversWindow()
    orders_window = OrdersWindow()
    history_window = HistoryWindow()

    # Подключаем слоты к кнопкам
    main_window.drivers_button.clicked.connect(drivers_window.show)
    main_window.orders_button.clicked.connect(orders_window.show)
    main_window.history_button.clicked.connect(history_window.show)

    sys.exit(app.exec())