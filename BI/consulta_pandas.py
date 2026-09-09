# Pandas é um biblioteca python utilizada para organizar, consultar, tranformar e analisar dados.
# Ela trabalha principalmente com uma estrutura chamada DataFrame
# instalar o pandas: pip install pandas


import pandas as pd
import mysql.connector 

# Criar uma função 
def conectar_banco():
    
    """
        Docstring: Documentação da função
        Cria e retorna uma conexão com o banco de dados. Retorna None se falhar
    """
    
    # O try tenta executar o codigo 
    # se acontecer algum erro, o programa vai para o except
    try:
        conexao = mysql.connector.connect(
            # Endereço onde o MySQL esta instalado
            # localhost significa que esta neste proprio computador
            host= 'localhost', 
            # Usuario utilizado para acessar o MySQL
            user= 'root',
            # Senha do usuario 
            password='',
            # Nome do banco de dados que queremos utilizar
            database='lojatech'
        )
        #  verificar se a conexão com banco foi realizada
        if conexao.is_connected():
            print('Conexão realizada com sucesso!')
            return conexao
    except mysql.connector.Error as erro:
        print(f'Erro ao conectar: {erro}')
        return None

conexao = conectar_banco()

cursor = conexao.cursor(
    dictionary=True
)
cursor.execute('select * from produtos')
produtos = cursor.fetchall()


df = pd.DataFrame(produtos)

print(df)

print('------------------------')

# sem pandas
for produto in produtos:
    print(f'nome: {produto['nome']} - preço: {produto['preco_venda']}')

print('------------------------')
# com pandas
print(df['nome'])

print('------------------------')
print(df[['nome','preco_venda']])

print('------------------------')
print(df.loc[0]) # mostrar a primeira linha do DataFrame
print(df.loc[5]) # mostrar a quinta linha do DataFrame

print('------------------------')
print(df['preco_venda'].sum()) # soma os valores da coluna

print('------------------------')
print(df['preco_venda'].mean()) # media dos valores da coluna

print('------------------------')
print(df['preco_venda'].max()) # maior valor desta coluna

print('------------------------')
print(df['preco_venda'].min()) # menor valor desta coluna

print('------------------------')
print(df['preco_venda'].idxmax()) # indice do maior valor da coluna

print('------------------------')
print(df['preco_venda'].idxmin()) # indice do menor valor da coluna

indice = df['preco_venda'].idxmax()

print(df.loc[indice])

