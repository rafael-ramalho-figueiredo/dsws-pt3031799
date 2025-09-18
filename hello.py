# A very simple Flask Hello World app for you to get started with...
from flask import Flask, request, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'PTDSWS'
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('Informe o seu nome:', validators=[DataRequired()])
    surname = StringField('Informe o seu sobrenome:', validators=[DataRequired()])
    institution = StringField('Informe a sua instituição de ensino:', validators=[DataRequired()])
    course = SelectField('Informe a sua disciplina:', choices=[('DSWA5', 'DSWA5'), ('DSWA4', 'DSWA4'), ('Gestão de Projetos', 'Gestão de Projetos')])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    ip = request.remote_addr;
    url = request.host
    if request.method == 'POST' and form.validate():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Você alterou o seu nome!')
        session['name'] = form.name.data
        session['surname'] = form.surname.data
        session['institution'] = form.institution.data
        session['course'] = form.course.data
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.utcnow(), ip=ip, url=url, form=form, name=session.get('name'), surname=session.get('surname'), institution=session.get('institution'), course=session.get('course'))

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