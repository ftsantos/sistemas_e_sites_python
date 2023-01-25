from flask import render_template, redirect, url_for, flash, request
from loja import app, database, bcrypt
from loja.forms import FormCriarUsuario, FormBuscarUsuario, FormEditarUsuario
from loja.models import Usuario
from flask_login import current_user, login_required

@app.route("/user/usuarios")
def usuarios():
    # if current_user.useradmin:
    lista_usuarios = Usuario.query.all()
    # else:
    #    lista_usuarios = []
    return render_template('user/usuarios.html', lista_usuarios=lista_usuarios)

@app.route("/user/criar", methods=['GET','POST'])
@login_required
def criar_usuario():
    form_usuario = FormCriarUsuario()
    if form_usuario.validate_on_submit() and 'botao_submit_criar_conta' in request.form:
        senha_crypt = bcrypt.generate_password_hash(form_usuario.senha.data)
        usuario = Usuario(cpf=form_usuario.cpf.data, username=form_usuario.username.data, email=form_usuario.email.data, senha=senha_crypt,
                          useradmin=form_usuario.useradmin.data)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Login feito com sucesso no e-mail: {form_usuario.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('user/criar_usuario.html', form_usuario=form_usuario)


@app.route("/user/buscar", methods=['GET','POST'])
@login_required
def buscar_usuario():
    form_buscar = FormBuscarUsuario()
    lista_usuarios = []
    if form_buscar.validate_on_submit() and request.method == 'POST':

        lista_usuarios = Usuario.query.filter(Usuario.username.like(form_buscar.username.data +"%")).all()
        #category = Category.query.filter(Category.title.like(category_param_value + "%")).all()

        print('-----------')
        for usuario in lista_usuarios:
            print(usuario.username)

    return render_template('user/buscar_usuario.html', lista_usuarios=lista_usuarios, form_buscar=form_buscar)
'''
@app.route("/user/buscar_", methods=['GET','POST'])
@login_required
def buscar_usuario_x():
    form_buscar = FormBuscarUsuario()
    form_usuario = FormEditarUsuario()

    print('AQUI AQUI AQYUI')

    if form_buscar.validate_on_submit() and request.method == 'GET':
        #username = form.username.data
        #usuarios = Usuario.query.filter_by(username=form.username.data).order_by(username) #.first()
        #usuario = Usuario.query.filter_by(username=form_buscar.username.data).first()


        if usuario:
            form_usuario.cpf.data = usuario.cpf
            form_usuario.email.data = usuario.email
            form_usuario.username.data = usuario.username
            form_usuario.useradmin.data = usuario.useradmin
            form_usuario.ativo.data = usuario.ativo
            form_usuario.senha_admin.data = ''

    return render_template('user/buscar_usuario.html', form_buscar=form_buscar)
'''
'''
@app.route("/user/editar", methods=['GET','POST'])
@login_required
def editar_usuario():
    form_usuario = FormCriarUsuario()
    if form_usuario.validate_on_submit() and 'botao_submit_criar_conta' in request.form:
        senha_crypt = bcrypt.generate_password_hash(form_usuario.senha.data)
        usuario = Usuario(cpf=form_usuario.cpf.data, username=form_usuario.username.data, email=form_usuario.email.data, senha=senha_crypt,
                          useradmin=form_usuario.useradmin.data)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Login feito com sucesso no e-mail: {form_usuario.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('user/editar_usuario.html', form_usuario=form_usuario)
'''

@app.route("/user/editar/<int:id>", methods=['GET','POST'])
@login_required
def editar_usuario(id):
    form_usuario = FormEditarUsuario()

    usuario = Usuario.query.filter_by(id=id).first()
    # category = Category.query.filter(Category.title.like(category_param_value + "%")).all()

    form_usuario.username.data = usuario.username
    form_usuario.email.data = usuario.email
    form_usuario.cpf.data = usuario.cpf
    form_usuario.useradmin.data = usuario.useradmin
    form_usuario.ativo.data = usuario.ativo

    print('Editar Usuário')

    return render_template('user/editar_usuario.html', form_usuario=form_usuario, id=id)

@app.route('/user/atualizar', methods=['POST',])
def atualizar_usuario():

    form_usuario = FormEditarUsuario(request.form)

    print('Atualizar Usuário')

    if form_usuario.validate_on_submit():

        if bcrypt.check_password_hash(current_user.senha, form_usuario.senha_admin.data):

            usuario = Usuario.query.filter_by(id=request.form['id']).first()         #usuario = Usuario.query.filter_by(id).first()
            usuario.username = form_usuario.username.data
            usuario.email = form_usuario.email.data
            usuario.cpf = form_usuario.cpf.data
            usuario.useradmin = form_usuario.useradmin.data
            usuario.ativo = form_usuario.ativo.data
            database.session.add(usuario)
            database.session.commit()
            return redirect(url_for('usuarios'))

        else:
            flash(f'Perfil não atualizado. Senha de Administrador errada.', 'alert-danger')


    return redirect(url_for('usuarios'))