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

cursor.execute("DROP DATABASE IF EXISTS `lojav1`;")

cursor.execute("CREATE DATABASE `lojav1`;")

cursor.execute("USE `lojav1`;")

# criando tabelas
TABLES = {}

TABLES['Usuario'] = ('''
      CREATE TABLE `usuario` (
      `id` int(4) AUTO_INCREMENT,
      `cpf` varchar(20) NOT NULL,
      `username` varchar(20) NOT NULL,
      `email` varchar(100) NOT NULL,
      `senha` varchar(100) NOT NULL,
      `foto_perfil` varchar(100) NOT NULL,
      `useradmin` BOOLEAN,
      `ativo` BOOLEAN,
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


# inserindo usuarios
usuario_sql = 'INSERT INTO usuario (cpf, username, email, senha, foto_perfil, useradmin, ativo) VALUES (%s, %s, %s, %s, %s, %s, %s)'
usuarios = [
      ("03320202020", "fsantos", "fsantos@gmail.com", generate_password_hash("123456").decode('utf-8'), 'default.jpg', 1, 1),
      ("03400042420", "rayane", "rayane@gmail.com", generate_password_hash("rayane").decode('utf-8'), 'default.jpg', 0, 1),
      ("12500002022", "sofia", "sofia@gmail.com", generate_password_hash("sofia123").decode('utf-8'), 'default.jpg', 0, 1)
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from lojav1.usuario')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[2])
'''
# inserindo jogos
jogos_sql = 'INSERT INTO jogos (nome, categoria, console) VALUES (%s, %s, %s)'
jogos = [
      ('Tetris', 'Puzzle', 'Atari'),
      ('God of War', 'Hack n Slash', 'PS2'),
      ('Mortal Kombat', 'Luta', 'PS2'),
      ('Valorant', 'FPS', 'PC'),
      ('Crash Bandicoot', 'Hack n Slash', 'PS2'),
      ('Need for Speed', 'Corrida', 'PS2'),
]
cursor.executemany(jogos_sql, jogos)

cursor.execute('select * from lojav1.jogos')
print(' -------------  Jogos:  -------------')
for jogo in cursor.fetchall():
    print(jogo[1])
'''
# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()