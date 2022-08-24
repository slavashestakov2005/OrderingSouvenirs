from .database import Table, Row
from datetime import datetime


class Order(Row):
    """
        Строка таблицы OrdersTable
        id              INT     NOT NULL    PK  AI  UNIQUE
        products        TEXT    NOT NULL
        status          INT     NOT NULL
        payment         INT     NOT NULL
        time            INT     NOT NULL
    """
    fields = ['id', 'products', 'status', 'payment', 'time']
    ORDERED, PAID, NOT_PAID, ERROR, COMPLETED = 0, 1, 2, 3, 4
    STATUSES = ['Заказано', 'Оплачено', 'Не оплачено', 'Ошибка', 'Выполнено']

    def __init__(self, row):
        Row.__init__(self, Order, row)

    def get_status(self):
        return Order.STATUSES[self.status]

    def get_time(self):
        return datetime.fromtimestamp(self.time).strftime('%Y.%m.%d %H:%M:%S')


class OrdersTable:
    table = "orders"

    @staticmethod
    def create_table() -> None:
        Table.drop_and_create(OrdersTable.table, '''(
        "id"	INTEGER NOT NULL UNIQUE,
        "products"	TEXT NOT NULL,
        "status"	INTEGER NOT NULL,
        "payment"	INTEGER NOT NULL,
        "time"	INTEGER NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
        );''')

    @staticmethod
    def select_all() -> list:
        return Table.select_list(OrdersTable.table, Order)

    @staticmethod
    def select(id: int) -> Order:
        return Table.select_one(OrdersTable.table, Order, 'id', id)

    @staticmethod
    def select_last() -> Order:
        return Table.select_last(OrdersTable.table, Order)

    @staticmethod
    def update(order: Order) -> None:
        return Table.update(OrdersTable.table, order)

    @staticmethod
    def insert(order: Order) -> None:
        return Table.insert(OrdersTable.table, order)

    @staticmethod
    def delete(order: Order) -> None:
        return Table.delete(OrdersTable.table, order)
