from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from app.models import Category, Product, Publishing, Author, UserRole
from app import app, db
from flask import redirect
from flask_login import logout_user, current_user

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN #phải là admin mới mở các tùy chọn

class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

class ProductModelView(AuthenticatedModelView):
    column_filters = ['name','author','price']
    column_searchable_list = ['name']
    column_exclude_list = ['image', 'description'] #ẩn trường
    can_view_details = True
    can_export = True
    column_labels = {
        'name': 'Tên sản phẩm'#đổi tên trường
    }



class StatsView(AuthenticatedView):
    @expose("/")
    def index(self):
        return self.render('admin/stats.html')

class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

admin = Admin(app=app, name='Quản lý sách', template_mode='bootstrap4')
admin.add_view(AuthenticatedModelView(Category, db.session, name='Danh mục'))
admin.add_view(ProductModelView(Product, db.session, name='Sản phẩm'))
admin.add_view(StatsView(name='Thống kê - báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))