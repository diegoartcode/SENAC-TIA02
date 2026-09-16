# pip list - para verificar bibliotecas instaladas 

# fazer instalação da biblioteca
# pip install mysql-connector-python 

#importa a biblioteca de conexão com mysql
import mysql.connector

# conexao com o banco
def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
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

cursor = conexao.cursor(
    dictionary=True
)

cursor.execute(
    '''
        SELECT atualizado_em, valor_total 
from pedidos where year(atualizado_em) = 2026 
and month(atualizado_em) = 6;
    '''
)

produtos = cursor.fetchall()
print(produtos)