# A very simple Flask Hello World app for you to get started with...
from flask import Flask, request, redirect
app = Flask(__name__)
@app.route('/')
def hello_world():
    return '<h1>Avaliação contínua: Aula 030</h1><ul><li><a href="/">Home</a></li><li><a href="/user/Rafael%20Ramalho/PT3031799/IFSP">Identificação</a></li><li><a href="/contextorequisicao">Contexto da requisição</a></li></ul>'

@app.route('/user/<name>/<prontuario>/<instituto>')
def user(name, prontuario, instituto):
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
