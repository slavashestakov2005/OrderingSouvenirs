from backend import app
from flask import render_template, request
from flask_cors import cross_origin
from flask_login import login_required
from ..help import empty_checker, SplitFile, Config
from ..database import TypesTable, Type
from .help import render_type, create_type, delete_type
'''
                        update_types()      Обновляет списки типов товаров.
                        TEMPLATE            Имя шаблона с настройкой типов товаров.
                        params()            Постоянные параметры этого шаблона.
    /types              types()             Пересылает на страницу с этим шаблоном.
    /add_type           add_type()          Создаёт тип товара.
    /edit_type          edit_type()         Редактирует тип товара.
    /delete_type        delete_type()       Удаляет тип товара.
'''


def update_types():
    types, str1, str2 = TypesTable.select_all(), '\n', '\n'
    for typ in types:
        str1 += '\t' * 8 + '<a class="dropdown-item" href="{0}">{1}</a>\n'.format(typ.page(), typ.name)
        str2 += '\t' * 8 + '<a class="dropdown-item" href="../{0}">{1}</a>\n'.format(typ.page(), typ.name)
    f = SplitFile(Config.TEMPLATES_FOLDER + '/page1.html')
    f.insert_after_comment(' list of types (1) ', str1 + '\t' * 7)
    f.save_file()
    f = SplitFile(Config.TEMPLATES_FOLDER + '/page2.html')
    f.insert_after_comment(' list of types (2) ', str2 + '\t' * 7)
    f.save_file()


TEMPLATE = 'settings_types.html'


def params():
    return {'types': TypesTable.select_all()}


@app.route("/types")
@cross_origin()
@login_required
def types():
    return render_template(TEMPLATE, **params())


@app.route("/add_type", methods=['POST'])
@cross_origin()
@login_required
def add_type():
    try:
        name = request.form['name']
        empty_checker(name)
    except Exception:
        return render_template(TEMPLATE, error_add_type='Поля заполнены не правильно', **params())

    typ = Type([None, name])
    TypesTable.insert(typ)
    update_types()
    create_type(typ.id)
    render_type(TypesTable.select_last().id)
    return render_template(TEMPLATE, error_add_type='Тип добавлен', **params())


@app.route("/edit_type", methods=['POST'])
@cross_origin()
@login_required
def edit_type():
    try:
        id = int(request.form['id'])
        name = request.form['name']
        empty_checker(name)
    except Exception:
        return render_template(TEMPLATE, error_edit_type='Поля заполнены не правильно', **params())

    typ = TypesTable.select(id)
    if typ.__is_none__:
        return render_template(TEMPLATE, error_edit_type='Не верный ID типа', **params())
    typ.name = name
    TypesTable.update(typ)
    update_types()
    render_type(typ.id)
    return render_template(TEMPLATE, error_edit_type='Тип изменён', **params())


@app.route("/delete_type", methods=['POST'])
@cross_origin()
@login_required
def delete_type():
    try:
        id = int(request.form['id'])
    except Exception:
        return render_template(TEMPLATE, error_delete_type='Поля заполнены не правильно', **params())

    typ = TypesTable.select(id)
    if typ.__is_none__:
        return render_template(TEMPLATE, error_delete_type='Не верный ID типа', **params())
    TypesTable.delete(typ)
    update_types()
    delete_type(typ.id)
    return render_template(TEMPLATE, error_delete_type='Тип удалён', **params())
