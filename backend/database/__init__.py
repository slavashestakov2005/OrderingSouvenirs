from .config import *
from .database import *
from .design import *
from .order import *
from .product import *
from .type import *
from .user import *


def create_tables():
    if Config.DROP_DB:
        DesignsTable.create_table()
        OrdersTable.create_table()
        ProductsTable.create_table()
        TypesTable.create_table()
        UsersTable.create_table()
