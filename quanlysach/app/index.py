from flask import render_template, request, redirect
from app import app, dao, login
from app import admin
from flask_login import login_user, logout_user
import cloudinary.uploader


@app.route('/')
def index():
    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    products = dao.load_products(category_id=cate_id, kw=kw)
    return render_template('index.html',
                           products=products)


@app.route('/products/<int:product_id>')
def product_detail(product_id):
    p = dao.get_product_by_id(product_id)
    return render_template('details.html', product=p)


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ''
    if request.method == 'POST':
        password = request.form['password']
        confirm = request.form['confirm']

        if password.__eq__(confirm):  # kiem tra xem mat khau co trung khop khong
            # upload avatar
            avatar = ''
            if request.files:
                res = cloudinary.uploader.upload(request.files['avatar'])
                avatar = res['secure_url']

            # luu user
            try:
                dao.register(name=request.form['name'],
                             username=request.form['username'],
                             password=request.form['password'],
                             avatar=avatar)
                return redirect('/')
            except:
                err_msg = 'Có lỗi xảy ra! vui lòng quay lại sau!'
        else:
            err_msg = 'Mat khau khong khop'

    return render_template('register.html', err_msg=err_msg)


@app.route('/login', methods=['get', 'post'])
def login_my_user():
    err_msg = ''
    if request.method == 'POST':
        username =request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user)
            return redirect('/')
        else:
            err_msg = 'Đăng nhập không thành công!'
    return render_template('login.html')

@app.route('/logout')
def logout_my_user():
    # login_user()
    logout_user()
    return redirect('/login')

@app.route('/login-admin', methods=['post'])
def login_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.context_processor
def common_attr():
    categories = dao.load_categories()
    return {
        'categories': categories
    }


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(debug=True)
