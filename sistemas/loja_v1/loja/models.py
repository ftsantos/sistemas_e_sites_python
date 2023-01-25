#from comunidade import database, login_manager
from loja import database, login_manager
from datetime import datetime
from flask_login import UserMixin

# função que carrega o usuário
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    cpf = database.Column(database.String, nullable=False)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')
    useradmin = database.Column(database.Boolean, server_default='f')
    ativo = database.Column(database.Boolean, server_default='t')
    #posts = database.relationship('Post', backref='autor', lazy=True)
    #cursos = database.Column(database.String, nullable=False, default='Não Informado')
    '''
    def contar_posts(self):
        return len(self.posts)
    '''
    
class Produto(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    nome = database.Column(database.String(50), nullable=False)
    categoria = database.Column(database.String(40), nullable=False)
    valor = database.Column(database.Numeric(6), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name