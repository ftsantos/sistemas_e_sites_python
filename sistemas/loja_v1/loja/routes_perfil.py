from flask import render_template, redirect, url_for, flash, request
from loja import app, database, bcrypt
from loja.forms import FormEditarPerfil
from flask_login import current_user, login_required
import secrets
import os
from PIL import Image

@app.route("/perfil/meuperfil")
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil/meuperfil.html', foto_perfil=foto_perfil)

def salvar_imagem(imagem):
    # adicionar código aleatório ao nome da imagem
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename) # separa o nome da extensão
    #nome_completo = os.path.join(nome, codigo, extensao)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    # reduzir o tamanho da imagem
    tamanho = (300, 300)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    # salvar a imagem na pasta fotos_perfil
    imagem_reduzida.save(caminho_completo)
    # mudar o campo foto_perfil do usuário para o novo nome da imagem
    return nome_arquivo

@app.route('/perfil/editar', methods=['GET','POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit(): # POST
        if bcrypt.check_password_hash(current_user.senha, form.senha.data):
            current_user.cpf = current_user.cpf #form.cpf.data
            current_user.email = form.email.data
            current_user.username = form.username.data
            if form.senha_nova.data:
                current_user.senha = bcrypt.generate_password_hash(form.senha_nova.data)

            if form.foto_perfil.data:
                nome_imagem = salvar_imagem(form.foto_perfil.data)
                current_user.foto_perfil = nome_imagem

            database.session.commit()
            flash(f'Perfil atualizado com sucesso', 'alert-success')
            return redirect(url_for('perfil'))
        else:
            flash(f'Perfil não atualizado. Senha atual errada.', 'alert-danger')

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.cpf.data = current_user.cpf

    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil/editar.html', foto_perfil=foto_perfil, form=form)
# bcrypt.check_password_hash(senha_crypt, senha)
