import mysql.connector
import pandas as pd
# pip install sweetviz
import sweetviz as sv

def conectar_banco():
    """ Cria e retorna uma conexão
    """
    try:
        conexao = mysql.connector.connect(
            host= 'localhost',
            user= 'root',
            password='',
            database='lojatech'
        )
        if conexao.is_connected():
            print('Conexão realizada com sucesso!')
            return conexao
    except mysql.connector.Error as erro:
        print(f'Erro ao conectar: {erro}')
        return None
    
conexao = conectar_banco()

cursor = conexao.cursor(dictionary=True)
cursor.execute('SELECT * FROM produtos where produto_id = 1;')
produtos = cursor.fetchall()
print(produtos)
# df = pd.DataFrame(produtos)

# analise = sv.analyze(df)

# analise.show_html('analise_produtos.html')


