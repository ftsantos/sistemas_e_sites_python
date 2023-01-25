from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import os

app = Flask(__name__)

# import secrets # secrets.token_hex(16)
app.config['SECRET_KEY'] = '01308c4c0304a9e51138dd4eaa5c9938'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meusite.db'
app.config['SQLALCHEMY_DATABASE_URI'] =  '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'fsantos',
        senha = 'fsantos',
        servidor = 'localhost',
        database = 'lojav1'
    )

#UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
app.config['UPLOAD_PATH'] = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
# print(UPLOAD_PATH) -- /home/francisco/PycharmProjects/jogoteca/uploads

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# todos os links com @login_required vão ser redirecionados para login
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

# Os links
# no final, pois routes precisam do app pra funcionar.

#importar o arquivo de links
from loja import routes
from loja import routes_perfil
from loja import routes_usuario
from loja import routes_produtos