# O que é estatistica descritiva
# é a parte da estatistica que busca organizar, resumir e apresentar dados de maneira que possamos entende-los melhor

# A estatistica descritiva permite resumir informações usando
# Tabelas, Gráficos, Média, Mediana, Moda, Amplitude, Variancia, Desvio-padrão, quantis e percentis

# a ideia principal é transformar muitos dados em informações faceis de interpretar

# População e amostra
# População é o conjunto completo que queremos estudar
# Amostra é uma parte da população escolhida para ser analisada


valores_pedidos = [
    100,
    120,
    150,
    180,
    200
]

# soma = 0

# for valor in valores_pedidos:
#     soma = soma + valor

soma = sum(valores_pedidos)

quantidade = len(valores_pedidos)

media = soma / quantidade

print(f'Média: {media}')

# ---------------------------------
valores_pedidos = [
    100,
    120,
    150,
    180,
    200,
    2000
]

media = sum(valores_pedidos)/len(valores_pedidos)
print(f'Média2: {media}')

# media - valores muito altos ou muito baixos podem influenciar bastante

# ---------------------------

# mediana é o valor que fica no centro dos dados quando eles estão organizados

valores_pedidos = [
    100,
    120,
    150,
    180,
    200
]

# mediana 150

valores_pedidos = [
    100,
    120,
    150,
    180,
    200,
    2000
]

# 150 + 180 / 2


# media e mediana 

# media considera todos os valores
# mediana observa o centro da distribuição


import statistics

valores_pedidos = [
    150,
    120,
    100,
    2000,
    200,
    180
]

mediana = statistics.median(valores_pedidos)
print(f'Mediana {mediana}')

# Moda é o valor que aparece com maior frequencia



valores_pedidos = [
    100,
    120,
    180,
    180,
    180,
    150,
    150,
    150
   
]

moda = statistics.mode(valores_pedidos)
print(f'Moda: {moda}')

formas_pagamento = [
    'PIX',
    'PIX',
    'CARTAO_CREDITO',
    'PIX',
    'CARTAO_DEBITO',
    'BOLETO'
]

moda = statistics.mode(formas_pagamento)
print(f'Moda: {moda}')


# amplitude mostra a distancia entre o menor e o maior valor

valores_pedidos = [
    100,
    120,
    150,
    180,
    200
]

amplitude = max(valores_pedidos) - min(valores_pedidos)
print(f'Amplitude: {amplitude}')


# Desvio-padrão ajuda a perceber o quanto os valores costumam ficar afastados da media

# desvio padrão pequeno - valores mais proximos da media
# desvio padrão grande - valores mais espalhados

amostra1 = [
    98,
    99,
    100,
    101,
    102
]

media = sum(amostra1)/len(amostra1)
print(f'amostra1: {media}')

amostra2 = [
    20,
    60,
    100,
    140,
    180
]
media = sum(amostra2)/len(amostra2)
print(f'Amostra2: {media}')

# variancia é uma medida que indica o quanto os valores de um conjunto de dados estão espalhados em relação a media


valores_pedidos = [
    100,
    120,
    150,
    180,
    200
]

# variancia de amostra
media = sum(valores_pedidos) / len(valores_pedidos)
variancia_amostra = sum((x - media) ** 2 for x in valores_pedidos) / (len(valores_pedidos) - 1) 

print(f'Variancia de amostra {variancia_amostra}')

# variancia de população
media = sum(valores_pedidos) / len(valores_pedidos)
variancia_populacao = sum((x - media) ** 2 for x in valores_pedidos) / (len(valores_pedidos)) 
print(f'Variancia de população {variancia_populacao}')
# ---------------------------------------

import pandas as pd

dados = {
    'pedido':[
        1,
        2,
        3,
        4,
        5,
        6,
        7
    ],
    'valor':[
        100,
        120,
        100,
        150,
        180,
        200,
        2000    
        ]
}

df = pd.DataFrame(dados)
print(df)

# media 
media = df['valor'].mean()

print(f'Media com pandas: {media}')

# mediana

mediana = df['valor'].median()
print(f'Mediana com pandas: {mediana}')

# moda
moda = df['valor'].mode()
print(f'Moda com pandas: {moda}')

# min e max
menor = df['valor'].min()
maior = df['valor'].max()

# amplitude
amplitude = maior - menor
print(f'Amplitude com pandas {amplitude}')

# variancia
variancia = df['valor'].var()
print(f'Variancia com pandas {variancia}')

# Desvio padrão 
desvio_padrao = df['valor'].std()
print(f'Desvio padrão {desvio_padrao}')

print(df['valor'].describe())