nome = "diego"
idade = 34
altura = 1.71
verdade = False

print(nome)
print(idade)
print(altura)
print(verdade)

produtos = [
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
print(produtos[3]['produto'])
print(produtos[3]['categoria'])


for produto in produtos:
    # print(produto)
    
    faturamento = (
        produto['quantidade'] * produto['preco']
    )

    print(
       "Produto: ", produto['produto'], "Valor unitario: ", produto['preco'], "Faturamento:  R$", faturamento
    )


# maior faturamento
maior_faturamento = 0
produto_maior_faturamento = ""

for produto in produtos:
    # print(produto)
    
    faturamento = (
        produto['quantidade'] * produto['preco']
    )

    if faturamento > maior_faturamento:
        maior_faturamento = faturamento
        produto_maior_faturamento = (produto["produto"])

print('Produto com maior faturamento: ', produto_maior_faturamento)
print('Faturamento: R$ ', maior_faturamento)

# BI - BUSINESS INTELLIGENCE

# DADOS > INFORMAÇÃO > ANALISE > DECISÃO

# PYTHON
# POWER BI
# TABLEAU 
# QLIK