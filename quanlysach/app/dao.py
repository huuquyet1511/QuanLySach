# from app import app
from app.models import Category, Product, User
from app import db
import hashlib


def load_categories():
    # with open('%s/data/categories.json' % app.root_path, encoding='utf-8') as f:
    #     return json.load(f)
    return Category.query.all()


def load_products(category_id=None, kw=None):
    query = Product.query

    if category_id:
        query = query.filter(Product.category_id.__eq__(category_id))

    if kw:
        query = query.filter(Product.name.contains(kw))

    return query.all()


def get_product_by_id(product_id):
    return Product.query.get(product_id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()

def register(name, username, password, avatar):#phuong thuc them user
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    u = User(name=name, username=username, password=password, avatar=avatar)
    db.session.add(u)
    db.session.commit()

def get_user_by_id(user_id):
    return User.query.get(user_id)
