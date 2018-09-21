from flask import redirect, url_for, request
from app import admin, db
from app.models import Employee, Workshop, Response
from app.users import User
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

class AdminModelView(ModelView):
    def is_accessible(self):
        return (current_user.is_authenticated and
                current_user.email == 'samuel@algorit.ma')
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

class EmployeeView(ModelView):
    def is_accessible(self):
        return (current_user.is_authenticated and
                current_user.leadership is True)

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

    column_searchable_list = ['name', 'degree', 'university']
    column_editable_list = ['active', 'degree', 'university', 'assigned_ta']
    column_filters = ['active', 'join_date']

class WorkshopView(ModelView):
    create_modal = True
    edit_modal = True
    can_export = True

class AnalyticsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/analytics_index.html', user=current_user)

admin.add_view(AdminModelView(User, db.session))
admin.add_view(EmployeeView(Employee, db.session))
admin.add_view(WorkshopView(Workshop, db.session))
admin.add_view(ModelView(Response, db.session))
admin.add_view(AnalyticsView(name='Analytics', endpoint='analytics'))
