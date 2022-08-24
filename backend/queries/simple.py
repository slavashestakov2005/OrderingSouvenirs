from backend import app
from flask import render_template
from flask_cors import cross_origin
from jinja2 import TemplateNotFound
from ..help import not_found_error
'''
    /               index()             Возвращает стартовую страницу.
    /<path>         static_file(path)   Возвращает страницу или файл.
'''


@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')


@app.route('/<path:path>')
@cross_origin()
def static_file(path):
    parts = [x.lower() for x in path.rsplit('.', 1)]
    try:
        if len(parts) >= 2 and parts[1] == 'html':
            return render_template(path)
        return app.send_static_file(path)
    except TemplateNotFound:
        return not_found_error()


'''
@app.route('/Types/<path:path>')
@cross_origin()
def products_file(path):
    parts = path.split('.')
    try:
        return render_template('Types/' + path, products=ProductsTable.select_by_type(int(parts[0])))
    except Exception:
        return not_found_error()
'''