# -*- coding: utf-8 -*-
import os, re
from app import app, db, lm
from flask import g,request, render_template, Flask, url_for, flash, redirect,session, abort, session, send_from_directory,send_file
from app.forms import LoginForm, MailForm
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from models import Admin,projects
from flask.ext.login import login_user , logout_user , current_user , login_required
from flask.ext.sqlalchemy import SQLAlchemy
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, DATA_FOLDER, DOWNLOAD_FOLDER, ADMINS
from flask.ext.login import UserMixin
from werkzeug.utils import secure_filename
from flask.ext.bcrypt import generate_password_hash, check_password_hash

from flask_admin import Admin as fl_admin
from flask.ext.admin.base import MenuLink, Admin, BaseView, expose,AdminIndexView
import flask_admin.contrib.fileadmin as FileAdmin
from flask_admin.contrib.sqlamodel import ModelView
from models import Admin, projects
from flask.ext.admin.base import BaseView
from admin import MyView
import models
from flask_mail import Message
from app import mail


from flask import request
from flask import jsonify

@lm.user_loader
def load_user(id):
    return Admin.query.get(int(id))


@app.route('/')
def index():
	form = MailForm()
	return render_template('index.html',form=form)

@app.route('/send_mail', methods=["POST"])
def sender():
	if request.method == 'GET':
		form = MailForm()
		return render_template('form.html',form = form)
	name = request.form['name']
	email= request.form['email']
	comment = request.form['comment']
	msg = Message('About your portfolio', sender = ADMINS[0], recipients = ADMINS)
	msg.body = email+'('+name+'), write you:'+ comment
	#msg.html =  '<p>text</p>'
	with app.app_context():
		mail.send(msg)
	return redirect(url_for('index'))


def get_dir(*args):
	dirs = DATA_FOLDER
	for arg in args:
		dirs = os.path.join(dirs, arg)
	return dirs

def getlist(pathFile):
	List = []
	for file in os.listdir(pathFile):
	    path = os.path.join(pathFile, file)
	    if not os.path.isdir(path):
	    	newList=path.split('/')
	    	for i in xrange(newList.index('projects')+1):
	    		newList.pop(0)
	    	typeList=[]
	    	for i in xrange(len(newList)):
	    		if re.findall(r'[.]',newList[i-1]) == []:
	    			typeList.append([newList[i-1],{'type':'folder'}])
	    		else:
	    			typeList.append([newList[i-1],{'type':'file'}])
	    	typeList.reverse()
	        List.append(typeList)
	    else:
	        List += getlist(path)
	return List

@app.route('/add_article')
def article():
    user = session.get('nickname')
    if user:
        return render_template('admin_panel.html',nickname = user)
    else:
        return render_template('root_blog.html')

@app.route('/add_in_blog')
def add():
	user = session.get('nickname')
	if user:
		return render_template('add_article.html',nickname = user)
	else:
		nickname = user
		form = LoginForm()
		return render_template('insp_login.html',nickname=nickname,form=form)

@app.route('/test-templ',methods=['POST','GET'])
def get_form():
	data = request.args.get('hidden')
	return render_template('test.html',data=data)

@app.route('/down_page')
def download_page():
    return render_template('filedownload.html')

@app.route('/portfolio')
def portfolio():
	projects = models.projects.query.all()
	return render_template('gallery.html',projects = projects)

@app.route('/login_page')
def login_page():
	form = LoginForm()
	return render_template('insp_login.html',form = form)

@app.route('/logout')
def logout():
    logout_user()
    session.pop('loged_in', None)
    session.pop('nickname',None)
    session.pop('password', None)
    return redirect(url_for('index')) 


@app.route('/review/<sitename>')
def preview(sitename):
    project = projects.query.filter_by(name = sitename).first()
    return render_template('review.html',project = project)


@app.route('/template')
def template():
	return render_template('template.html')

@app.route('/blog')
def get_blog():
	return render_template('blog.html')

@app.route('/sendtempl', methods=['POST','GET'])
def send_templ():
	data = request.form
	data = dict(data)
	data = data.get('editor1')
	my_str = ''.join(data)
	f = open('templ.html', 'w')
	f.write(my_str)
	f.close()
	return render_template('test.html',data = my_str)




@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == 'GET':
		form = LoginForm()
		return render_template('form.html',form = form)
	nickname = request.form['nickname']
	password = request.form['password']
	auth_user = Admin.query.filter_by(nickname=nickname).first()
	if auth_user is None:
		form = LoginForm()
		error = [u'Введите правильно имя пользователя или пароль']
		return render_template('insp_login.html', form=form, error = error)
	if Admin.check_password(auth_user,password) is False:
		form = LoginForm()
		error = 'Извините, но у вас не достаточно прав для этой операции'
		return render_template('insp_login.html', form=form, error = error)
	inst = Admin.check_password(auth_user,password)
	login_user(auth_user)
	current_user = Admin.query.get(nickname)
	session['nickname'] = nickname
	session['loged_in'] = True
	return render_template('admin_panel.html',nickname = nickname,inst = inst)
	#return redirect(url_for('admin'))



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/download', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            #return redirect(url_for('uploaded_file',filename=filename))
            return render_template('down_info.html',filename=filename)
    return render_template("filedownload.html", args=args)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory([UPLOAD_FOLDER,DOWNLOAD_FOLDER],
                               filename)

@app.route('/projects/<path:filename>')
def uploaded_file_form_project(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)


#использовать в крайней необходимости
#@app.route('/register/<nickname>/<password>')
#def register(nickname,password):
	#if db.session.query(Admin).filter_by(nickname=nickname).count() <1:
		#hash_pass = generate_password_hash(password)
		#user = Admin(nickname = nickname, email='sadasfafsafasf', password = hash_pass)
		#db.session.add(user)
		#db.session.commit()
		#return redirect('/')
	#else:
		#return 'lol'

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
	return jsonify({'ip': request.remote_addr}), 200
