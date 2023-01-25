# pip install mysql-connector-python==8.0.28
# pip install flask-sqlalchemy==2.5.1
import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

# https://cursos.alura.com.br/forum/topico-access-denied-for-user-root-localhost-prepara_banco-py-175417
# link para resolver problema de conexão com o Banco de Dados
'''
Pra resolver isso eu só criei outro user no mysql pra usar no projeto e mudei a config no prepara_banco.py.
sudo mysql (ou mariadb)
CREATE USER 'user1'@localhost IDENTIFIED BY 'password1';
GRANT ALL PRIVILEGES ON *.* TO 'user1'@'localhost';
prepara_banco.py
conn = MySQLdb.connect(user='user1', passwd='password1', host='127.0.0.1', port=3306)C
-----------
CREATE USER 'fsantos'@localhost IDENTIFIED BY 'fsantos';
grant all privileges on *.* to 'fsantos'@'localhost';

'''
print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='fsantos',
            password='fsantos'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("USE `lojav1`;")

# criando tabelas
TABLES = {}

TABLES['Produto'] = ('''
      CREATE TABLE `produto` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,
      `categoria` varchar(40) NOT NULL,
      `valor` decimal NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# inserindo produtos
produto_sql = 'INSERT INTO produto (nome, categoria, valor) VALUES (%s, %s, %s)'
produto = [
      ('iPhone', 'Smart Phone', '7.000'),
      ('WebCam', 'Eletrônicos', '400'),
      ('Onix Plus', 'Veículos', '102.000'),
      ('Gol', 'Veículos', '75.000'),
]
cursor.executemany(produto_sql, produto)

cursor.execute('select * from lojav1.produto')
print(' -------------  produto:  -------------')
for produto in cursor.fetchall():
    print(produto[1]+' - '+produto[2])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()