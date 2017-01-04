from app import db
from flask.ext.bcrypt import generate_password_hash, check_password_hash
from flask_admin.contrib.sqlamodel import ModelView


ROLE_ADMIN = 1
def cut(self):
    String = self[:64]
    return String

class Admin(db.Model):
    uid = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_ADMIN)
    password =db.Column(db.String(64),default = 'admin')

    def __init__(self , nickname ,password,email):
        self.nickname = nickname
        self.password = password
        self.email = email


    def check_password(self, password):
        return check_password_hash(self.password, password)
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def __repr__(self):
        return '<Admin %r>' % (self.nickname)
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.uid
    def is_authenticated(self):
        return True
    def __unicode__(self):
        return self.nickname

class projects(db.Model):
    uid = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    review = db.Column(db.String(1000),default='not text')
    cut_review = db.Column(db.String(64))
    link = db.Column(db.String(128), unique = True)
    prev_link  = db.Column(db.String(128), unique = True)
    desktop = db.Column(db.SmallInteger, default = None)
    mobile_version = db.Column(db.SmallInteger, default = None)
    interactive = db.Column(db.SmallInteger, default = None)
    inter_map = db.Column(db.SmallInteger, default = None)
    using = db.Column(db.SmallInteger, default = None)
    cover = db.Column(db.String(128), unique = True)
    def __repr__(self):
        return '<projects %r>' % (self.name)
    
class Articles(db.Model):
    art_id = db.Column(db.Integer, primary_key = True) 
    art_name = db.Column(db.String(64), unique = True)
    review = db.Column(db.String(254))
    cover = db.Column(db.String(128), unique = True)
    page = db.Column(db.String(128), unique = True)
    visits = db.Column(db.Integer, default = 0)
    
