from flask import render_template, redirect, url_for, flash, request
from loja import app, database, bcrypt
from loja.forms import FormLogin, FormCriarUsuario, FormEditarPerfil, FormBuscarUsuario #, FormEditarUsuario
from loja.models import Usuario
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image

@app.route("/contato")
def contato():
    return render_template('contato.html')

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout feito com sucesso', 'alert-success')
    return redirect(url_for('home'))

@app.route('/login', methods=['GET','POST'])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data) # faz o login
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            parametro_next = request.args.get('next')
            if parametro_next:
                return redirect(parametro_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no login: E-mail ou Senha Incorretos', 'alert-danger')
    return render_template('user/login.html', form_login=form_login)
