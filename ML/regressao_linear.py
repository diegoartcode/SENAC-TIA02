# Regressão Linear é um algoritmo que tenta encontrar uma linha que represente a relação entre uma variavel de entrada e um valor numerico que queremos prever.

import pandas as pd

# pip install scikit-learn
from sklearn.linear_model import LinearRegression

dados = {
    "mes": [1,2,3,4,5],
    "faturamento": [50000,53000,56000,59000,62000]
}

df = pd.DataFrame(dados)

# print(df)

# feature - entrada do modelo. 
x = df[['mes']]

# print(x)

# target - é uma variavel que queremos prever
y = df['faturamento']

modelo = LinearRegression()
# cria uma instancia (um objeto) do modelo de regressão linear, ainda vazio, sem ter aprendido nada 

modelo.fit(x,y)
#  treina o modelo: ele encontra a melhor reta que menhor se ajusta aos pontos (mes,faturamento) fornecidos

print('Modelo treinado!')

novo_mes = pd.DataFrame({"mes":[6]})
# criea um novo DataFrame com um unico valor mes 6, que ainda não esta nos dados originais. e é para esse mes que vamos prever o faturamento

print('----novo mes-----')
print(novo_mes)
print('----x-----')
print(x)
print('----df-----')
print(df)

print('-----------------------------')

previsao = modelo.predict(novo_mes)
# usa o modelo treinado para prever o faturamento do mes 6
# o resultado é um array numpy

print(previsao)

previsao = modelo.predict(novo_mes)[0]

print(f'Previsão: R$ {previsao:.2f}')

import matplotlib.pyplot as plt

plt.scatter(df['mes'],df['faturamento'])
plt.xlabel('Mês')

plt.ylabel('Faturamento')
plt.title('Loja Tech')
plt.show()