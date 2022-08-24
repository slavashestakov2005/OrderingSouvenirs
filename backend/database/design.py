from .database import Table, Row


class Design(Row):
    """
        Строка таблицы DesignsTable
        id              INT     NOT NULL    PK  AI  UNIQUE
        product         INT     NOT NULL
    """
    fields = ['id', 'product']

    def __init__(self, row):
        Row.__init__(self, Design, row)


class DesignsTable:
    table = "design"

    @staticmethod
    def create_table() -> None:
        Table.drop_and_create(DesignsTable.table, '''(
        "id"	INTEGER NOT NULL UNIQUE,
        "product"	INTEGER NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
        );''')

    @staticmethod
    def select_all() -> list:
        return Table.select_list(DesignsTable.table, Design)

    @staticmethod
    def select(id: int) -> Design:
        return Table.select_one(DesignsTable.table, Design, 'id', id)

    @staticmethod
    def select_last() -> Design:
        return Table.select_last(DesignsTable.table, Design)

    @staticmethod
    def insert(design: Design) -> None:
        return Table.insert(DesignsTable.table, design)

    @staticmethod
    def delete(design: Design) -> None:
        return Table.delete(DesignsTable.table, design)
