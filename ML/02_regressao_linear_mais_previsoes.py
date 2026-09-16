# Regressão Linear é um algoritmo que tenta encontrar uma linha que represente a relação entre uma variavel de entrada e um valor numerico que queremos prever.

import pandas as pd

# pip install scikit-learn
from sklearn.linear_model import LinearRegression

# pip install matplotlib
import matplotlib.pyplot as plt

dados = {
    "mes": [1,2,3,4,5,6],
    "faturamento": [50000,54500,52000,61000,59000,66000]
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

novo_mes = pd.DataFrame({"mes":[7]})
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



plt.scatter(df['mes'],df['faturamento'])
# cria um grafico de dispersão (pontos) com meses no eixo x e o fatumento
# no eixo y, usando dados originais do (df)

plt.xlabel('Mês')
# define o rotulo do eixo x como Mês

plt.ylabel('Faturamento')
# define o rotulo do eixo y como Faturamento

plt.title('Loja Tech')
# define o titulo do grafico

plt.show()
# Exibe o grafico na tela (abre uma janela ou renderiza no notebook)



previsao_historica = modelo.predict(x)
# usa o modelo para prever o faturamento dos Mesmos meses que já exitem 
# isso serve para desenhar a linha do modelo sobre os dados reais e comparar visualmente o ajuste
print('---------------------')
print(previsao_historica)

plt.scatter(
    df['mes'],
    df['faturamento'],
    label='Valores reais'
)
# novo grafico de dispersão com os pontos reais, agora com um rotulo 
# valores reais que vai aparecer na legenda

plt.plot(
    df['mes'],
    previsao_historica,
    label='Linha do modelo'
)
# desenha uma linha conectando os valores PREVISTOS pelo modelo para os meses 1 a 5 - essa é a reta de regressão aprendida

plt.ylabel('Mês')
# rotulo do eixo x

plt.xlabel('Faturamento')
# rotulo do eixo y

plt.title('Regressão linear')
# titulo do segundo grafico

plt.legend()
# mostra a legenda no gráfico, usando os textos 
# definidos em label='....' scatter e plot


plt.show()
# exibe o segundo grafico: pontos reais + reta do modelo

print(modelo.intercept_) 

print(modelo.coef_)




# -------------------------------------------------------------

# previsões para os meses que já possuem faturamento
previsao_historica = modelo.predict(x)

# previsões para os meses futuros
novos_meses = pd.DataFrame({'mes':[7,8,9]})
previsoes = modelo.predict(novos_meses)

# grafico dos valores reais
plt.scatter(
    df['mes'],
    df['faturamento'],
    color='blue',
    label='Valores reais'
)

# linha do modelo nos meses historiocos
plt.plot(
    df['mes'],
    previsao_historica,
    color='green',
    label='Linha do modelo'
)

# linha das previsões futuras
plt.plot(
    novos_meses['mes'],
    previsoes,
    color='red',
    linestyle='--',
    marker='o',
    label='previsão'
)

# colocar o valor da previsão ao lado de cada ponto
for mes, valor in zip(novos_meses['mes'],previsoes):
    plt.text(
        mes,
        valor,
        f'R$ {valor:,.2f}',
        ha='center',
        va='bottom'
    )

plt.xlabel('Mês')
plt.ylabel('Faturamento')
plt.legend()

plt.grid(True,alpha=0.3)

plt.show()

