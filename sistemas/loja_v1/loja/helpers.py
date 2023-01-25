import os
from loja import app

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa_{id}' in nome_arquivo:
            return nome_arquivo

    return 'default.jpg'

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'default.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))