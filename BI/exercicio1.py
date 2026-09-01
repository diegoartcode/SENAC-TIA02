# 1 conecte ao banco
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


# 2 liste todos os produtos
cursor.execute(
    'SELECT * FROM produtos'
)

produtos = cursor.fetchall()
print(produtos)

for produto in produtos:
    print(produto['nome'])
# 3 mostre nome e preço de venda

cursor.execute(
    'SELECT nome, preco_venda FROM produtos'
)
produtos = cursor.fetchall()
for produto in produtos:
    print(f'Nome do produto: {produto['nome']} - Preço: {produto['preco_venda']}')
# 4 identifique o produto mais caro

produto_mais_caro = max(
    produtos,
    key = lambda produto: produto['preco_venda']
)

print(f'Produto mais caro: {produto_mais_caro['nome']} - Preço: R$ {produto_mais_caro['preco_venda']}')


# 5 identifique o produto mais barato
produto_mais_barato = min(
    produtos,
    key = lambda produto: produto['preco_venda']
)

print(f'Produto mais barato: {produto_mais_barato['nome']} - Preço: R$ {produto_mais_barato['preco_venda']}')



# 6 calcule a diferença entre preço de custo e preço de venda 

cursor.execute(
    'SELECT nome, preco_venda,preco_custo FROM produtos'
)

produtos = cursor.fetchall()

for produto in produtos:
    preco_custo = produto['preco_custo']
    preco_venda = produto['preco_venda']

    diferenca = preco_venda - preco_custo
    # diferenca =  produto['preco_venda'] - produto['preco_custo']

    print(f'Produto: {produto['nome']}  - Diferença: {diferenca} ')

# 7 conte quantos produtos foram retornados
# 8 busque os registros da tabela itens_pedido
# 9 some todas as quatidade de vendas
# 10 some todos os subtotais dos produtos