import os
from jogoteca import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField #, validators
from wtforms.validators import DataRequired, Length

class FormularioJogo(FlaskForm):
    '''
    nome = StringField('Nome do jogo', [validators.DataRequired(), validators.Length(min=1, max=50)])
    categoria = StringField('Nome da categoria', [validators.DataRequired(), validators.Length(min=1, max=40)])
    console = StringField('Nome do console', [validators.DataRequired(), validators.Length(min=1, max=20)])
    '''
    nome = StringField('Nome do jogo', validators=[DataRequired(), Length(min=1, max=50)])
    categoria = StringField('Nome da categoria', validators=[DataRequired(), Length(min=1, max=40)])
    console = StringField('Nome do console', validators=[DataRequired(), Length(min=1, max=20)])

    salvar = SubmitField('Salvar')

class FormularioUsuario(FlaskForm):
    nickname = StringField('Nickname', validators=[DataRequired(), Length(min=1, max=8)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=1, max=100)])
    login = SubmitField('Login')

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa_{id}' in nome_arquivo:
            return nome_arquivo

    return 'default.jpg'

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'default.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))
