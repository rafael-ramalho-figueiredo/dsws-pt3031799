from flask import render_template, session, redirect, url_for, current_app, request
from .. import db
from ..models import User, Role, Email
from ..email import send_simple_message
from . import main
from .forms import NameForm, LoginForm
from datetime import datetime

@main.route('/', methods=['GET', 'POST'])
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

            if current_app.config['FLASKY_ADMIN']:
                print('Enviando mensagem...', flush=True)
                send_simple_message(f"{current_app.config['FLASKY_ADMIN']}, flaskaulasweb@zohomail.com", 'Novo usuário', form.name.data)
                print('Mensagem enviada...', flush=True)
        else:
            session['known'] = True

        session['name'] = form.name.data
        return redirect(url_for('main.index'))
    return render_template('index.html', users=users, roles=roles, form=form, name=session.get('name'),
                           known=session.get('known', False))

@main.route('/emailsEnviados')
def email_enviados():
    emails = Email.query.all()
    return render_template('emails.html', emails=emails)

@main.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@main.route('/user/<name>/<prontuario>/<instituto>')
def user2(name, prontuario, instituto):
    return render_template('id.html', name=name, prontuario=prontuario, instituto=instituto)
