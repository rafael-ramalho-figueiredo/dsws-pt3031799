# A very simple Flask Hello World app for you to get started with...
from flask import Flask, request, redirect, render_template, session, url_for
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired
import os
from flask_sqlalchemy import SQLAlchemy
import requests
from dotenv import load_dotenv

project_folder = os.path.expanduser('~/flask')
load_dotenv(os.path.join(project_folder, '.env'))

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'PTDSWS'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

app.config['API_KEY'] = os.environ.get('API_KEY')
app.config['API_URL'] = os.environ.get('API_URL')
app.config['API_FROM'] = os.environ.get('API_FROM')

app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')

def send_simple_message(to, subject, newUser):
    print('Enviando mensagem (POST)...', flush=True)
    print('URL: ' + str(app.config['API_URL']), flush=True)
    print('api: ' + str(app.config['API_KEY']), flush=True)
    print('from: ' + str(app.config['API_FROM']), flush=True)
    print('to: ' + str(to), flush=True)
    print('subject: ' + str(app.config['FLASKY_MAIL_SUBJECT_PREFIX']) + ' ' + subject, flush=True)
    print('text: ' + "Novo usuário cadastrado: " + newUser, flush=True)

    resposta = requests.post(app.config['API_URL'],
                             auth=("api", app.config['API_KEY']), data={"from": app.config['API_FROM'],
                                                                        "to": to,
                                                                        "subject": app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                                                                        "text": "PT3031799\nRafael Ramalho Figueiredo\nNovo usuário cadastrado: " + newUser})

    print('Enviando mensagem (Resposta)...' + str(resposta) + ' - ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), flush=True)
    return resposta

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
    email = BooleanField('Deseja enviar e-mail para flaskaulasweb@zohomail.com?')
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
    roles = Role.query.all()
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        user_role = Role.query.filter_by(name='User').first()
        if user is None:
            user = User(username=form.name.data, role=user_role)
            db.session.add(user)
            db.session.commit()
            session['known'] = False

            print('Verificando variáveis de ambiente: Server log do PythonAnyWhere', flush=True)
            print('FLASKY_ADMIN: ' + str(app.config['FLASKY_ADMIN']), flush=True)
            print('URL: ' + str(app.config['API_URL']), flush=True)
            print('api: ' + str(app.config['API_KEY']), flush=True)
            print('from: ' + str(app.config['API_FROM']), flush=True)
            print('to: ' + str([app.config['FLASKY_ADMIN'], "flaskaulasweb@zohomail.com"]), flush=True)
            print('subject: ' + str(app.config['FLASKY_MAIL_SUBJECT_PREFIX']), flush=True)
            print('text: ' + "Novo usuário cadastrado: " + form.name.data, flush=True)

            if app.config['FLASKY_ADMIN']:
                print('Enviando mensagem...', flush=True)
                if form.email.data:
                    send_simple_message(f"{app.config['FLASKY_ADMIN']}, flaskaulasweb@zohomail.com", 'Novo usuário', form.name.data)
                else:
                    send_simple_message(f"{app.config['FLASKY_ADMIN']}", 'Novo usuário', form.name.data)
                print('Mensagem enviada...', flush=True)
        else:
            session['known'] = True

        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', users=users, roles=roles, form=form, name=session.get('name'),
                           known=session.get('known', False))

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