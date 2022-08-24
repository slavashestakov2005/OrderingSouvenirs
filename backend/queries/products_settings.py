from backend import app
from flask import render_template, request
from flask_cors import cross_origin
from flask_login import login_required
from ..help import empty_checker, generate_filename
from ..database import ProductsTable, Product, TypesTable
from .help import render_type, create_product, render_product
from PIL import Image
import os
'''
                        TEMPLATE            Имя шаблона с настройкой товаров.
                        DEFAULT_IMAGE       Фото товара по умолчанию.
                        params()            Постоянные параметры этого шаблона.
                        get_image_name()    Сохраняет полученный файл под нужным именем.
    /products           products()          Пересылает на страницу с этим шаблоном.
    /add_product        add_product()       Создаёт товар.
    /edit_product       edit_product()      Редактирует товар.
    /delete_product     delete_product()    Удаляет товар.
'''


TEMPLATE, DEFAULT_IMAGE = 'settings_products.html', 'logo.png'


def params():
    return {'products': ProductsTable.select_all()}


def dist(rgb1, rgb2):
    return sum((rgb1[_] - rgb2[_]) ** 2 for _ in range(3))


def clear_image(filename):
    img = Image.open(filename)
    rgba = img.convert("RGBA")
    data = rgba.getdata()
    new_data = []
    old = data[0][:3]
    for item in data:
        d = dist(item, old)
        if d < 5000:
            new_data.append((255, 255, 255, 0))
        else:
            # print(d)
            new_data.append(item)
    rgba.putdata(new_data)
    filename = filename.rsplit('.', 1)
    filename[-1] = 'png'
    rgba.save('.'.join(filename), "PNG")
    return filename[0].split('/')[-1] + '.png'


def get_image_name(new, default=DEFAULT_IMAGE):
    if request.form.get('is_file') is not None:
        file = request.files['file-file']
        file_name, tail = generate_filename(file.filename, str(new))
        file.save(file_name)
        new_file = clear_image(file_name)
        if tail != new_file:
            os.remove(file_name)
        return new_file
    tail = request.form['file-name']
    return tail if tail else default


@app.route("/products")
@cross_origin()
@login_required
def products():
    return render_template(TEMPLATE, **params())


@app.route("/add_product", methods=['POST'])
@cross_origin()
@login_required
def add_product():
    try:
        typ = int(request.form['type'])
        name = request.form['name']
        cost = int(request.form['cost'])
        empty_checker(name)
    except Exception as ex:
        return render_template(TEMPLATE, error_add_product='Поля заполнены не правильно', **params())

    if TypesTable.select(typ).__is_none__:
        return render_template(TEMPLATE, error_add_product='Не правильный тип товара', **params())
    if cost < 0 or cost > 5000:
        return render_template(TEMPLATE, error_add_product='Товар не может столько стоить', **params())
    product = Product([None, typ, name, DEFAULT_IMAGE, cost])
    ProductsTable.insert(product)
    product = ProductsTable.select_last()
    product.photo = get_image_name(product.id)
    ProductsTable.update(product)
    render_type(typ)
    create_product(product.id)
    render_product(product.id)
    return render_template(TEMPLATE, error_add_product='Товар добавлен', **params())


@app.route("/edit_product", methods=['POST'])
@cross_origin()
@login_required
def edit_product():
    try:
        id = int(request.form['id'])
        typ = int(request.form['type']) if request.form['type'] else None
        name = request.form['name']
        cost = int(request.form['cost']) if request.form['cost'] else None
    except Exception:
        return render_template(TEMPLATE, error_edit_product='Поля заполнены не правильно', **params())

    product = ProductsTable.select(id)
    if product.__is_none__:
        return render_template(TEMPLATE, error_edit_product='Не верный ID товара', **params())
    if typ is not None and TypesTable.select(typ).__is_none__:
        return render_template(TEMPLATE, error_edit_product='Не правильный тип товара', **params())
    if cost is not None and (cost < 0 or cost > 5000):
        return render_template(TEMPLATE, error_edit_product='Товар не может столько стоить', **params())
    if typ:
        product.type, old_typ = typ, product.type
    if name:
        product.name = name
    if cost:
        product.cost = cost
    product.photo = get_image_name(product.id, product.photo)
    ProductsTable.update(product)
    if typ:
        render_type(old_typ)
    render_type(product.type)
    render_product(product.id)
    return render_template(TEMPLATE, error_edit_product='Товар изменён', **params())


@app.route("/delete_product", methods=['POST'])
@cross_origin()
@login_required
def delete_product():
    try:
        id = int(request.form['id'])
    except Exception:
        return render_template(TEMPLATE, error_delete_product='Поля заполнены не правильно', **params())

    product = ProductsTable.select(id)
    if product.__is_none__:
        return render_template(TEMPLATE, error_delete_product='Не верный ID товара', **params())
    ProductsTable.delete(product)
    render_type(product.type)
    delete_product(product.id)
    return render_template(TEMPLATE, error_delete_product='Товар удалён', **params())
