# A very simple Flask Hello World app for you to get started with...
from flask import Flask, request, redirect, render_template
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_moment import Moment

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/')
def hello_world():
    return render_template('index.html', current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/user/<name>/<prontuario>/<instituto>')
def user2(name, prontuario, instituto):
    return '<h1>Avaliação contínua: Aula 030</h1><h2>Aluno: {}</h2><h2>Prontuário: {}</h2><h2>Instituição: {}</h2><a href="/">Voltar</a>'.format(name, prontuario, instituto)

@app.route('/contextorequisicao')
def contextorequisicao():
    user_agent = request.headers.get('User-Agent');
    ip = request.remote_addr;
    url = request.host
    return '<h1>Avaliação contínua: Aula 030</h1><h2>Seu navegador é: {}</h2><h2>O IP do computador remoto é: {}</h2><h2>O host da aplicação é: {}</h2><a href="/">Voltar</a>'.format(user_agent, ip, url)

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