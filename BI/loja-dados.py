# Estatística descritiva
# Estatística descritiva é um conjunto de técnicas utilizadas para organizar, resumir e compreender os dados que ja temos.

vendas = [
     {
        "produto":"Notebook Pro 14",
        "categoria":"Informática",
        "quantidade":8,
        "preco":3500
    },
    {
        "produto":"Mouse Gamer",
        "categoria":"Periférico",
        "quantidade":35,
        "preco":120 
    },
    {
        "produto":"Teclado Mecânico",
        "categoria":"Periférico",
        "quantidade":18,
        "preco":280 
    },
    {
        "produto":"Monitor 24",
        "categoria":"Informática",
        "quantidade":12,
        "preco":900 
    } 
]

faturamento = vendas[1]['quantidade'] * vendas[1]['preco']
print(f'Valor de faturamento para o produto {vendas[1]['produto']} é {faturamento}.')



faturamento_total = 0

for venda in vendas:
    faturamento = (
        venda['quantidade'] * venda['preco']
    )

    faturamento_total = ( 
        faturamento_total + faturamento
    )

print(faturamento_total)

print(f'Faturamento total: R$ {faturamento_total:.2f}')
  


# Quantidade de unidades de produtos foram vendidas?
# Quantos produtos foram vendidos no total?

quantidade_total = 0
for item in vendas:
    quantidade_total = quantidade_total + item['quantidade']
print(f'Total de unidades vendidas: {quantidade_total}')


# Qual produto vendeu mais?

maior_quantidade = 0
produto_mais_vendido = ''

for venda in vendas:
    if venda['quantidade'] > maior_quantidade:
        maior_quantidade = venda['quantidade']
        produto_mais_vendido = venda['produto']

print(f'produto mais vendido: {produto_mais_vendido}')
print(f'Quantidade: {maior_quantidade}')












# Qual produto gerou mais dinheiro?

# Qual produto ficaram acima da média?

# Calcule o faturamento somente da categoria "Periferico"