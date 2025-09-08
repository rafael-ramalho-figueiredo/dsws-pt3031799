# A very simple Flask Hello World app for you to get started with...
from flask import Flask, request, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'PTDSWS'
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'))

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