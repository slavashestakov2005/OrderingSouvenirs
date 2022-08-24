from .database import Table, Row


class Type(Row):
    """
        Строка таблицы TypesTable
        id              INT     NOT NULL    PK  AI  UNIQUE
        name            TEXT    NOT NULL
    """
    fields = ['id', 'name']

    def __init__(self, row):
        Row.__init__(self, Type, row)

    def page(self) -> str:
        return 'Types/{}.html'.format(self.id)


class TypesTable:
    table = "type"

    @staticmethod
    def create_table() -> None:
        Table.drop_and_create(TypesTable.table, '''(
        "id"	INTEGER NOT NULL UNIQUE,
        "name"	TEXT NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
        );''')

    @staticmethod
    def select_all() -> list:
        return Table.select_list(TypesTable.table, Type)

    @staticmethod
    def select(id: int) -> Type:
        return Table.select_one(TypesTable.table, Type, 'id', id)

    @staticmethod
    def select_last() -> Type:
        return Table.select_last(TypesTable.table, Type)

    @staticmethod
    def update(typ: Type) -> None:
        return Table.update(TypesTable.table, typ)

    @staticmethod
    def insert(typ: Type) -> None:
        return Table.insert(TypesTable.table, typ)

    @staticmethod
    def delete(typ: Type) -> None:
        return Table.delete(TypesTable.table, typ)
