from flask import Flask, render_template

from loja.models import Usuario

#app = Flask(__name__)

# do arquivo __init__
from loja import app

#app.config.from_pyfile('config.py')

if __name__ == '__main__':
    app.run(debug=True) # as mudanças são refletidas direto no site, sem precisar parar e executar novamente