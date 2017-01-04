from flask_admin import Admin as fl_admin
from flask.ext.admin.base import MenuLink, Admin, BaseView, expose,AdminIndexView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqlamodel import ModelView
from app import app, db
from models import Admin,projects
import os.path as op

import os
from app.forms import LoginForm
from flask import Flask, url_for, redirect, render_template, request,session
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import form, fields, validators
from flask.ext import admin, login
from flask.ext.admin.contrib import sqla
from flask.ext.admin import helpers, expose
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import Security
path = op.join(op.dirname(__file__),'projects')


def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(uid):
		return db.session.query(Admin).get(uid)

class MyAdminIndexView(admin.AdminIndexView):
    
    @expose('/')
    def index(self):
        user = session.get('nickname')
        if user:
        	#return render_template('layout.html',nickname=user)
        	return render_template('admin_panel.html',nickname = user)
        else:
			nickname = user
			form = LoginForm()
			return render_template('insp_login.html',nickname=nickname,form=form)
    
    @expose('/fileadmin/')
    @expose('/projects/')
    def add_project(self):
        user = session.get('nickname')
        if user:
            #return render_template('layout.html',nickname=user)
            return render_template('admin_panel.html',nickname = user)
        else:
            nickname = user
            form = LoginForm()
            return render_template('insp_login.html',nickname=nickname,form=form)

    @expose('/login/', methods=('GET', 'POST'))
    def login_view():
		if request.method == 'GET':
			form = LoginForm()
			return render_template('form.html',form = form)
		nickname = request.form['nickname']
		password = request.form['password']
		auth_user = Admin.query.filter_by(nickname=nickname).first()
		if auth_user is None:
			form = LoginForm()
			error = [u'Enter right password or nickname']
			return render_template('insp_login.html', form=form, error = error)
		if Admin.check_password(auth_user,password) is False:
			form = LoginForm()
			error = "Sorry, but you don't have right enough for this operation"
			return render_template('insp_login.html', form=form, error = error)
		inst = Admin.check_password(auth_user,password)
		login_user(auth_user)
		current_user = Admin.query.get(nickname)
		session['nickname'] = nickname
		session['loged_in'] = True
		return redirect(url_for('admin.index'))
		#return render_template('layout.html')

	#@expose('/loginpage/')
    #def login_page(self):
        #form = LoginForm()
		#return render_template('insp_login.html',form = form)

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        session.pop('loged_in', None)
        session.pop('nickname',None)
        session.pop('password', None)
        return redirect(url_for('index')) 


#admin = fl_admin(app,name='portfolio', template_mode='bootstrap3')
admin = fl_admin(app, index_view=MyAdminIndexView(), base_template='layout.html')
class MyView(BaseView):
  @expose('/')
  def index(self):
  	return self.render('admin/index.html')

#admin.add_view(MyView(name='Hello'))

class ProjectAdmin(ModelView):
    column_display_pk = True
    #form_columns = ['uid', 'name','review','link','prev_link','cover']
    columns = ['uid', 'name','review','link','prev_link','cover']
    page_size = 5
    can_view_details = True
    column_list=('uid', 'name','review','link','prev_link','cover')

class MicroBlogModelView(ModelView):
    edit_template = 'edit.html'
    create_template = 'create.html'
    list_template = 'list.html'

admin.add_view(FileAdmin(path,'/projects/', name='Projects Files'))
admin.add_view(ProjectAdmin(projects, db.session,name='Projects db'))
#def security_context_processor():
    #return dict(
        #admin_base_template=admin.base_template,
        #admin_view=admin.index_view,
        #h=admin_helpers,
    #)
