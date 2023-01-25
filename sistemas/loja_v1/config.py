import os

#app.secret_key = 'senha_para_proteger_os_cookies'
SECRET_KEY = 'senha_para_proteger_os_cookies'

#app.config['SQLALCHEMY_DATABASE_URI'] = \
SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'fsantos',
        senha = 'fsantos',
        servidor = 'localhost',
        database = 'lojav1'
    )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
# print(UPLOAD_PATH) -- /home/francisco/PycharmProjects/jogoteca/uploads