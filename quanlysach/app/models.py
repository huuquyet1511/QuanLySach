from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from app import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin

class UserRole(UserEnum):
    USER = 1
    ADMIN = 2
    EMPLOYEE = 3


class BaseModel(db.Model):
    __abstract__ = True  # lớp thành lớp trừu tượng
    id = Column(Integer, primary_key=True, autoincrement=True)


class Category(BaseModel):
    __tablename__ = 'category'

    # id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=False)

    def __str__(self):
        return self.name


class Author(BaseModel):
    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='author', lazy=False)

    def __str__(self):
        return self.name


class Publishing(BaseModel):
    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='publishing', lazy=False)

    def __str__(self):
        return self.name


class Product(BaseModel):
    # __tablename__ = 'product'

    # id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    price = Column(Float, default=0)
    image = Column(String(100))
    active = Column(Boolean, default=True)  # kiểm tra sản phẩm còn kinh doanh hay không
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)  # Khóa ngoại kết nối voi bảng Category
    author_id = Column(Integer, ForeignKey(Author.id), nullable=False)
    publishing_id = Column(Integer, ForeignKey(Publishing.id), nullable=False)

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():

        import hashlib
        password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        u = User(name='Phạm Hữu Quyết', username='admin',
                 password=password, user_role=UserRole.ADMIN,
                 avatar='https://cdn0.fahasa.com/media/catalog/product/m/a/mat-biec_bia-mem_in-lan-thu-44.jpg')
        db.session.add(u)
        db.session.commit()

        c1 = Category(name='Tiểu thuyết')
        c2 = Category(name='Truyện tranh')
        c3 = Category(name='Light novel')
        c4 = Category(name='Truyện dài')

        db.session.add_all([c1, c2, c3, c4])
        db.session.commit()

        a1 = Author(name='Nguyễn Nhật Ánh')
        a2 = Author(name='J.K.Rowling')
        a3 = Author(name='FUJIMOTO Tatsuki')
        a4 = Author(name='Maruyama Kugane')
        a5 = Author(name='Ao Jyumonji')
        a6 = Author(name='Gege Akutami')
        a7 = Author(name='Paulo Coelho')
        a8 = Author(name='Toriyama Akira')

        db.session.add_all([a1, a2, a3, a4, a5, a6, a7, a8])
        db.session.commit()

        l1 = Publishing(name='NXB Kim Đồng')
        l2 = Publishing(name='NXB Thanh Niên')
        l3 = Publishing(name='NXB Trẻ')
        l4 = Publishing(name='IPM')
        l5 = Publishing(name='Nhã Nam')

        db.session.add_all([l1, l2, l3, l4, l5])
        db.session.commit()

        p1 = Product(name='Mắt biếc', description='Khi một lá thư được gởi đến cho cậu bé Harr', price=160000,
                     image='https://cdn0.fahasa.com/media/catalog/product/m/a/mat-biec_bia-mem_in-lan-thu-44.jpg',
                     category_id=1, author_id=1, publishing_id=1)

        p2 = Product(name='7 viên ngọc rồng 9', description='Người cưa', price=160000,
                         image='https://photos.google.com/u/3/photo/AF1QipOgVGX0oKESWgWwdXhZQjH_zP5su0iUSFVdb8fg',
                         category_id=3, author_id=2, publishing_id=3)
        p3 = Product(name='Nhà giả kim', description='Thức giậy từ bóng tối', price=160000,
                         image='https://photos.google.com/u/3/photo/AF1QipOgVGX0oKESWgWwdXhZQjH_zP5su0iUSFVdb8fg',
                         category_id=2, author_id=7, publishing_id=3)
        p4 = Product(name='Mắt biếc', description='Khi một lá thư được gởi đến cho cậu bé Harr', price=160000,
                     image='https://photos.google.com/u/3/photo/AF1QipOgVGX0oKESWgWwdXhZQjH_zP5su0iUSFVdb8fg',
                     category_id=1, author_id=1, publishing_id=5)
        p5 = Product(name='7 viên ngọc rồng 9', description='Người cưa', price=160000,
                     image='https://photos.google.com/u/3/photo/AF1QipOgVGX0oKESWgWwdXhZQjH_zP5su0iUSFVdb8fg',
                     category_id=3, author_id=6, publishing_id=4)
        p6 = Product(name='Nhà giả kim', description='Thức giậy từ bóng tối', price=160000,
                     image='https://photos.google.com/u/3/photo/AF1QipOgVGX0oKESWgWwdXhZQjH_zP5su0iUSFVdb8fg',
                     category_id=2, author_id=5, publishing_id=4)
        p7 = Product(name='Mắt biếc', description='Khi một lá thư được gởi đến cho cậu bé Harr', price=160000,
                     image='https://photos.google.com/u/3/photo/AF1QipOgVGX0oKESWgWwdXhZQjH_zP5su0iUSFVdb8fg',
                     category_id=4, author_id=2, publishing_id=5)
        p8 = Product(name='7 viên ngọc rồng 9', description='Người cưa', price=160000,
                     image='https://photos.google.com/u/3/photo/AF1QipOgVGX0oKESWgWwdXhZQjH_zP5su0iUSFVdb8fg',
                     category_id=3, author_id=7, publishing_id=2)
        p9 = Product(name='Nhà giả kim', description='Thức giậy từ bóng tối', price=160000,
                     image='https://photos.google.com/u/3/photo/AF1QipOgVGX0oKESWgWwdXhZQjH_zP5su0iUSFVdb8fg',
                     category_id=4, author_id=4, publishing_id=3)

        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)

        db.session.add(p4)
        db.session.add(p5)
        db.session.add(p6)
        db.session.add(p7)
        db.session.add(p8)
        db.session.add(p9)
        db.session.commit()
        # db.create_all()


