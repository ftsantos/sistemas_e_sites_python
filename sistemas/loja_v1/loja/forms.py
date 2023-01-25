from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from loja.models import Usuario
from flask_login import current_user

class FormCriarUsuario(FlaskForm):

    cpf = StringField('CPF', validators=[DataRequired()])
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação de Senha', validators=[DataRequired(), EqualTo('senha')])
    useradmin = BooleanField('Este Usuário é um Administrador?')
    ativo = BooleanField('Este Usuário está Ativo?')


    botao_submit_criar_conta = SubmitField('Criar Conta')

    # O nome da função tem que começar com validate_
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar')

class FormEditarUsuario(FlaskForm):

    cpf = StringField('CPF', validators=[DataRequired()])
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha_admin = PasswordField('Senha de Administrador', validators=[DataRequired(), Length(6, 20)])
    useradmin = BooleanField('Este Usuário é um Administrador?')
    ativo = BooleanField('Este Usuário está Ativo?')

    botao = SubmitField('Editar Usuário')

class FormBuscarUsuario(FlaskForm):

    username = StringField('Nome do Usuário', validators=[DataRequired()])
    botao_submit_buscar_perfil = SubmitField('Buscar')

class FormLogin(FlaskForm):

    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')

    botao_submit_login = SubmitField('Fazer Login')


class FormEditarPerfil(FlaskForm):

    cpf = StringField('CPF')

    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto de perfil', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

    senha = PasswordField('Senha Atual', validators=[DataRequired(), Length(6, 20)])
    senha_nova = PasswordField('Nova Senha', validators=[Optional(), Length(6, 20)])

    botao_submit_editar_perfil = SubmitField('Confirmar Edição')

    # O nome da função tem que começar com validate_
    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com este e-mail. Cadastre outro e-mail')

class FormularioProduto(FlaskForm):
    '''
    nome = StringField('Nome do jogo', [validators.DataRequired(), validators.Length(min=1, max=50)])
    categoria = StringField('Nome da categoria', [validators.DataRequired(), validators.Length(min=1, max=40)])
    console = StringField('Nome do console', [validators.DataRequired(), validators.Length(min=1, max=20)])
    '''
    nome = StringField('Nome do Produto', validators=[DataRequired(), Length(min=1, max=50)])
    categoria = StringField('Nome da categoria', validators=[DataRequired(), Length(min=1, max=40)])
    valor = StringField('Valor do Produto', validators=[DataRequired(), Length(min=1, max=20)])

    salvar = SubmitField('Cadastrar')

class FormBuscarProduto(FlaskForm):

    nome = StringField('Nome do Produto')
    categoria = StringField('Nome da categoria')
    valor = StringField('Valor do Produto')

    buscar = SubmitField('Buscar')