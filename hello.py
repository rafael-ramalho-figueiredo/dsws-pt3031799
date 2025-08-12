# A very simple Flask Hello World app for you to get started with...
from flask import Flask, request
app = Flask(__name__)
@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1><h2>Disciplina PTBDSWS</h2>'

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)

@app.route('/contextorequisicao')
def contextorequisicao():
    user_agent = request.headers.get('User-Agent');
    return '<p>Your browser is {}</p>'.format(user_agent);