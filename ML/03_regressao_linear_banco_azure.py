# pip list - para verificar bibliotecas instaladas 

# fazer instalação da biblioteca
# pip install mysql-connector-python 

# importa a biblioteca de conexão com mysql
import mysql.connector

# conexao com o banco
def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host='mysql-loja-tech-diego.mysql.database.azure.com',
            user='diegorodriguesdev',
            password='',
            database='lojatech'
        )

        if conexao.is_connected():
            print('Conexão realizada com sucesso!')
            return conexao
    except mysql.connector.Error as erro:
        print(f'Erro ao conectar ao banco. {erro}')
        return None
    
 
conexao = conectar_banco()


