import os
from ..help import save_template
from ..database import TypesTable, ProductsTable
from ..config import Config


def type_filename(typ: int):
    return Config.TEMPLATES_FOLDER + '/Types/{}.html'.format(typ)


def create_type(typ: int):
    with open(type_filename(typ), mode='a'):
        pass


def render_type(typ: int):
    params = {'name': TypesTable.select(typ).name, 'products': ProductsTable.select_by_type(typ)}
    save_template('template_type.html', type_filename(typ), **params)


def delete_type(typ: int):
    os.remove(type_filename(typ))


def product_filename(product: int):
    return Config.TEMPLATES_FOLDER + '/Products/{}.html'.format(product)


def create_product(product: int):
    with open(product_filename(product), mode='a'):
        pass


def render_product(product: int):
    product = ProductsTable.select(product)
    typ = TypesTable.select(product.type)
    params = {'type': typ, 'product': product}
    save_template('template_product.html', product_filename(product.id), head_size=5, **params)


def delete_product(product: int):
    os.remove(product_filename(product))
