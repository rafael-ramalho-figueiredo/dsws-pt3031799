# A very simple Flask Hello World app for you to get started with...
from flask import Flask, request, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'PTDSWS'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

class NameForm(FlaskForm):
    name = StringField('Informe o seu nome:', validators=[DataRequired()])
    role = SelectField('Função:', choices=[('Admin', 'Admin'), ('Moderator', 'Moderator'), ('User', 'User')])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

@app.route('/', methods=['GET', 'POST'])
def index():
    users = User.query.all()
    total_users = User.query.count()
    roles = Role.query.all()
    total_roles = Role.query.count()
    form = NameForm()
    ip = request.remote_addr
    url = request.host
    if request.method == 'POST' and form.validate():
        old_name = session.get('name')
        user_role = Role.query.filter_by(name=form.role.data).first()
        if old_name is not None and old_name != form.name.data:
            flash('Você alterou o seu nome!')
        existing_user = User.query.filter_by(username=form.name.data).first()
        if not existing_user:
            new_user = User(username=form.name.data, role=user_role)
            db.session.add(new_user)
            db.session.commit()
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.utcnow(), ip=ip, url=url, form=form, name=session.get('name'), users=users, roles=roles, total_users=total_users, total_roles=total_roles)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        session['username'] = form.username.data
        return redirect('loginResponse')
    return render_template('login.html', current_time=datetime.utcnow(), form=form)

@app.route('/loginResponse', methods=['GET', 'POST'])
def loginResponse():
    return render_template('loginResponse.html', current_time=datetime.utcnow(), username=session.get('username'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/user/<name>/<prontuario>/<instituto>')
def user2(name, prontuario, instituto):
    return render_template('id.html', name=name, prontuario=prontuario, instituto=instituto)

@app.route('/contextorequisicao')
def contextorequisicao():
    user_agent = request.headers.get('User-Agent');
    ip = request.remote_addr;
    url = request.host
    return '<h1>Avaliação contínua: Aula 030</h1><h2>Seu navegador é: {}</h2><h2>O IP do computador remoto é: {}</h2><h2>O host da aplicação é: {}</h2><a href="/">Voltar</a>'.format(user_agent, ip, url)

@app.route('/contextorequisicao/<name>')
def contextouser(name):
    user_agent = request.headers.get('User-Agent');
    ip = request.remote_addr;
    url = request.host
    return render_template('contexto.html', name=name, user_agent=user_agent, ip=ip, url=url)

@app.route('/codigostatusdiferente')
def codigostatusdiferente():
    return '<p>Bad request</p>'

@app.route('/objetoresposta')
def objetoresposta():
    return '<h1>This document carries a cookie!</h1>'

@app.route('/redirecionamento')
def redirecionamento():
    return redirect('https://ptb.ifsp.edu.br/', code=302)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500