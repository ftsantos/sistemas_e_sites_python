from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from loja import app, database
from loja.models import Produto
from loja.helpers import recupera_imagem, deleta_arquivo
from loja.forms import FormularioProduto, FormBuscarProduto
from flask_login import login_required
import time

@app.route('/produtos')
@login_required
def listar_produtos():
    lista = Produto.query.order_by(Produto.id)
    print('XXXXXXXXXXXXX')
    return render_template('produto/lista.html', produtos=lista)

@app.route('/novo')
@login_required
def novo_produto():
    #if 'usuario_logado' not in session or session['usuario_logado'] == None:
     #   return redirect(url_for('login', proxima=url_for('novo')))

    form = FormularioProduto()
    return render_template('produto/novo.html', titulo='Novo Produto', form=form)

@app.route('/editar/<int:id>')
@login_required
def editar_produto(id):
    #if 'usuario_logado' not in session or session['usuario_logado'] == None:
    #    return redirect(url_for('login', proxima=url_for('produto/editar', id=id)))

    produto = Produto.query.filter_by(id=id).first()

    form = FormularioProduto()
    form.nome.data = produto.nome
    form.categoria.data = produto.categoria
    form.valor.data = produto.valor

    capa_produto = recupera_imagem(id)

    return render_template('produto/editar.html', titulo='Editando Produto', id=id, capa_produto=capa_produto, form=form)

@app.route('/atualizar', methods=['POST',])
@login_required
def atualizar_produto():
    form = FormularioProduto(request.form)

    if form.validate_on_submit():
        produto = Produto.query.filter_by(id=request.form['id']).first()
        produto.nome = form.nome.data
        produto.categoria = form.categoria.data
        produto.valor = form.valor.data

        database.session.add(produto)
        database.session.commit()

        arquivo = request.files['arquivo']
        uploads_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(produto.id)
        arquivo.save(f'{uploads_path}/capa_{produto.id}-{timestamp}.jpg')

    return redirect(url_for('listar_produtos'))

@app.route('/deletar/<int:id>')
@login_required
def deletar_produto(id):
    #if 'usuario_logado' not in session or session['usuario_logado'] == None:
    #    return redirect(url_for('login'))

    Produto.query.filter_by(id=id).delete()
    database.session.commit()
    flash('Produto deletado com sucesso!')
    return redirect(url_for('listar_produtos'))


@app.route('/criar', methods=['POST',])
def criar_produto():
    form = FormularioProduto(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    categoria = form.categoria.data
    valor = form.valor.data

    produto = Produto.query.filter_by(nome=nome).first()

    if produto:
        flash('Produto já existente!')
        return redirect(url_for('listar_produtos'))

    novo_produto = Produto(nome=nome, categoria=categoria, valor=valor)
    database.session.add(novo_produto)
    database.session.commit()

    arquivo = request.files['arquivo']
    #arquivo.save(f'../uploads/{arquivo.filename}')
    #arquivo.save(f'../uploads/capa_{novo_produto.id}.jpg')
    uploads_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{uploads_path}/capa_{novo_produto.id}-{timestamp}.jpg')

    return redirect(url_for('listar_produtos'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads',nome_arquivo)

@app.route("/produto/buscar_produto", methods=['GET','POST'])
@login_required
def buscar_produto():
    form_buscar = FormBuscarProduto()
    lista_produtos = []
    if form_buscar.validate_on_submit() and request.method == 'POST':

        if form_buscar.nome.data:
            lista_produtos = Produto.query.filter(Produto.nome.like(form_buscar.nome.data +"%")).all()
        #category = Category.query.filter(Category.title.like(category_param_value + "%")).all()

        print('------- PRODUTO ----')
        for produto in lista_produtos:
            print(produto.nome)

    return render_template('produto/buscar_produto.html', lista_produtos=lista_produtos, form_buscar=form_buscar)
