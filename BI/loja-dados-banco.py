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




# Quanto existe de difereça entre o preço de venda e o preço de custo?
cursor.execute(
    "SELECT nome, preco_venda, preco_custo FROM produtos;"
)

produtos = cursor.fetchall()

for produto in produtos:
    diferenca = produto['preco_venda'] - produto['preco_custo']
    
    print(f'Produto: {produto['nome']}')

    print(f'Preço de custo R$ {produto['preco_custo']}')

    print(f'Preço de venda R$ {produto['preco_venda']}')

    print(f'Diferença: R$ {diferenca}')

    print('---------------------')


# Qual produto possui maior preço de venda 
maior_preco = 0

for produto in produtos:
    if produto['preco_venda'] > maior_preco:
        maior_preco = produto['preco_venda']
        produto_maior_preco = produto['nome']

print(f'Produto com maior preço: {produto_maior_preco}')
print(f'Preço R$ {maior_preco}')


# Quantidade total de unidades vendidas

cursor.execute(
    "SELECT status, valor FROM pagamentos;"
)
pagamentos = cursor.fetchall()

quantidade_total = 0

for pagamento in pagamentos:
    if pagamento['status'] == 'APROVADO':
        quantidade_total = quantidade_total + pagamento['valor']

print(f'Quantidade total: {quantidade_total}')

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


cursor.close()
conexao.close()