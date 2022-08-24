from backend import app, Config
from flask import request, send_file, render_template
from flask_cors import cross_origin
from flask_login import login_required
from ..database import DesignsTable, Design, ProductsTable, Order, OrdersTable
from ..help import not_found_error, forbidden_error, unix_time, TinkoffCard
import os
import shutil
import pickle
from PIL import Image


class DesignFile:
    def __init__(self):
        self.is_empty = request.form.get('empty_file') is not None
        self.file = request.files['file'] if request.form.get('empty_file') is None else None
        self.cx = float(request.form["cx"])
        self.cy = float(request.form["cy"])
        self.w = float(request.form["w"])
        self.h = float(request.form["h"])
        self.aw = float(request.form["aw"])
        self.ah = float(request.form["ah"])
        self.product = int(request.form['product'])

    def design(self, directory, filename):
        product = ProductsTable.select(self.product)
        im1 = Image.open(Config.UPLOAD_FOLDER + '/Images/' + product.photo)
        if self.is_empty:
            im1.save(directory + '/design.png')
            im1.close()
            return
        im2 = Image.open(filename)
        w, h = im1.size
        kw, kh = w / self.aw, h / self.ah

        im2 = im2.resize((round(kw * self.w), round(kh * self.h)))
        im1.paste(im2, (round(kw * (self.cx - self.w / 2)), round(kh * (self.cy - self.h / 2))))
        im1.save(directory + '/design.png')
        im1.close()
        im2.close()

    def save(self, directory):
        filename = directory + '/image.png'
        if self.file:
            self.file.save(filename)
        else:
            shutil.copy(Config.UPLOAD_FOLDER + '/Images/empty.png', filename)
        data = {'cx': self.cx, 'cy': self.cy, 'w': self.w, 'h': self.h, 'aw': self.aw, 'ah': self.ah}
        with open(directory + '/data.txt', 'wb') as f:
            pickle.dump(data, f)
        self.design(directory, filename)


def get_status(status):
    if status in Config.PAID_STATES:
        return Order.PAID
    elif status in Config.NOT_PAID_STATES:
        return Order.NOT_PAID
    return None


@app.route('/save_design', methods=['POST'])
@cross_origin()
def save_design():
    try:
        df = DesignFile()
    except Exception:
        return {'id': -1}

    design = Design([None, df.product])
    DesignsTable.insert(design)
    design = DesignsTable.select_last()
    directory = Config.DESIGNS_FOLDER + '/' + str(design.id)
    if os.path.exists(directory):
        return {'id': -1}
    os.makedirs(directory)
    df.save(directory)
    return {'id': design.id}


@app.route('/get_design', methods=['POST'])
@cross_origin()
def get_design():
    bad = {'name': '', 'cost': ''}
    try:
        design = int(request.form['design'])
    except Exception:
        return bad

    design = DesignsTable.select(design)
    if design.__is_none__:
        return bad
    product = ProductsTable.select(design.product)
    if product.__is_none__:
        return bad
    return {'name': product.name, 'cost': product.cost}


@app.route('/design_image')
@cross_origin()
def design_image():
    try:
        design = int(request.args.get('id'))
    except Exception:
        return not_found_error()
    return send_file('designs/{}/design.png'.format(design))


@app.route('/src_design_image')
@cross_origin()
def src_design_image():
    try:
        design = int(request.args.get('id'))
    except Exception:
        return not_found_error()
    return send_file('designs/{}/image.png'.format(design))


@app.route('/add_order', methods=['POST'])
@cross_origin()
def add_order():
    try:
        raw_info = request.form['info']
        info = list(int(_) for _ in raw_info.split('='))
        if len(info) % 2:
            raise ValueError
    except Exception:
        return forbidden_error()

    desc, sm = '', 0
    for i in range(0, len(info), 2):
        design = DesignsTable.select(info[i])
        if design.__is_none__:
            return forbidden_error()
        product = ProductsTable.select(design.product)
        if product.__is_none__:
            return forbidden_error()
        if desc:
            desc += '; '
        desc += '{}: {} шт'.format(product.name, info[i + 1])
        sm += product.cost * info[i + 1]
    order = Order([None, raw_info, Order.ORDERED, 0, unix_time()])
    OrdersTable.insert(order)
    order = OrdersTable.select_last()
    error, url, payment = TinkoffCard.receipt(sm, order.id, desc)
    if error != '0':
        order.status = Order.ERROR
        OrdersTable.update(order)
        return forbidden_error()
    order.payment = payment
    OrdersTable.update(order)
    return {'url': url, 'id': order.id}


TEMPLATE = 'settings_orders.html'


def params():
    return {'orders': OrdersTable.select_all()}


@app.route("/orders")
@cross_origin()
@login_required
def orders():
    return render_template(TEMPLATE, **params())


@app.route("/complete_order")
@cross_origin()
@login_required
def complete_order():
    try:
        order = OrdersTable.select(int(request.args.get('id')))
        if order.__is_none__:
            raise ValueError
    except Exception:
        return forbidden_error()

    order.status = Order.COMPLETED
    OrdersTable.update(order)
    return render_template(TEMPLATE, **params())


@app.route("/delete_order")
@cross_origin()
@login_required
def delete_order():
    try:
        order = OrdersTable.select(int(request.args.get('id')))
        if order.__is_none__:
            raise ValueError
    except Exception:
        return forbidden_error()

    OrdersTable.delete(order)
    return render_template(TEMPLATE, **params())


@app.route("/update_order")
@app.route('/t_success')
@app.route('/t_fail')
@cross_origin()
def tinkoff():
    try:
        order = OrdersTable.select(int(request.args.get('id')))
        if order.__is_none__:
            raise ValueError
    except Exception:
        return forbidden_error()

    if order.status == Order.COMPLETED:
        return render_template(TEMPLATE, **params())
    error, status = TinkoffCard.get_state(order.payment)
    new_status = get_status(status)
    if new_status:
        order.status = new_status
        OrdersTable.update(order)
    return render_template(TEMPLATE, **params())
