from .database import Table, Row


class Product(Row):
    """
        Строка таблицы ProductsTable
        id              INT     NOT NULL    PK  AI  UNIQUE
        type            INT     NOT NULL
        name            TEXT    NOT NULL
        photo           TEXT    NOT NULL
        cost            INT     NOT NULL
    """
    fields = ['id', 'type', 'name', 'photo', 'cost']

    def __init__(self, row):
        Row.__init__(self, Product, row)


class ProductsTable:
    table = "product"

    @staticmethod
    def create_table() -> None:
        Table.drop_and_create(ProductsTable.table, '''(
        "id"	INTEGER NOT NULL UNIQUE,
        "type"	INTEGER NOT NULL,
        "name"	TEXT NOT NULL,
        "photo"	TEXT NOT NULL,
        "cost"	INTEGER NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
        );''')

    @staticmethod
    def select_all() -> list:
        return Table.select_list(ProductsTable.table, Product)

    @staticmethod
    def select(id: int) -> Product:
        return Table.select_one(ProductsTable.table, Product, 'id', id)

    @staticmethod
    def select_last() -> Product:
        return Table.select_last(ProductsTable.table, Product)

    @staticmethod
    def select_by_type(typ: int) -> list:
        return Table.select_list(ProductsTable.table, Product, 'type', typ)

    @staticmethod
    def update(product: Product) -> None:
        return Table.update(ProductsTable.table, product)

    @staticmethod
    def insert(product: Product) -> None:
        return Table.insert(ProductsTable.table, product)

    @staticmethod
    def delete(product: Product) -> None:
        return Table.delete(ProductsTable.table, product)
