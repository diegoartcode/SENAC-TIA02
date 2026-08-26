# instalar o conector MySQL
# pip install mysql-connector-python
# essa biblioteca permitira que o python e mysql se comuniquem


import mysql.connector

conexao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'lojatech'
)

if conexao.is_connected():
    print('Conexão realizada com sucesso!')

cursor = conexao.cursor(
    dictionary=True
)

cursor.execute(
    'SELECT nome, preco_venda FROM produtos;'
)

produtos = cursor.fetchall()
print(produtos)

for produto in produtos:
    print(f'O produto {produto['nome']} tem o preço {produto['preco_venda']}')


cursor.close()
conexao.close()

# Quanto existe de difereça entre o preço de venda e o preço de custo?
# Qual produto possui maior preço de venda 
# Quantidade total de unidades vendidas

# 1 conecte ao banco
# 2 liste todos os produtos
# 3 mostre nome e preço de venda
# 4 identifique o produto mais caro
# 5 identifique o produto mais barato
# 6 calcule a diferença entre preço de custo e preço de venda 
# 7 conte quantos produtos foram retornados
# 8 busque os registros da tabela itens_pedido
# 9 some todas as quatidade de vendas
# 10 some todos os subtotais dos produtos