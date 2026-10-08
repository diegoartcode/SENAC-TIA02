# O código a seguir para criar um dataframe e remover as linhas duplicadas sempre é executado e age como um preâmbulo para o script: 

# dataset = pandas.DataFrame(undefined, undefined.1, undefined.2, undefined.3, undefined.4)
# dataset = dataset.drop_duplicates()

# Cole ou digite aqui seu código de script:

# importar as bibliotecas 
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


# copiar os dados recebidos do power bi (dataset)

df = dataset.copy()

# padronizar a coluna status

# selecionando a coluna 'status'
df["status"] = (
    # converte todos os valores da coluna para texto

    df["status"].astype(str)

    # remover espaços extras antes e depois do texto
    # " ENTREGUE " > "ENTREGUE"
    .str.strip()

    # converter todos os textos em letras maiuscula
    # "Entregue" > "ENTREGUE"
    .str.upper()

)


# coverte a coluna Ano para numero

#errors='coerce' significa que, se existir algum valor que não possa ser convertido para numero, ele sera tranformado em NaN.
df['Ano'] = pd.to_numeric(
    df['Ano'],
    errors='coerce'
)

# converte a coluna Numero_mes para numero   
# "1" > 1
# "2" > 2
df['Numero_mes'] = pd.to_numeric(
    df['Numero_mes'], 
    errors='coerce'
)

# converte a coluna valor_total para numero
df['valor_total'] = pd.to_numeric(
    df['valor_total'], 
    errors='coerce'
)

# remove linhas que tenham valores invalidos 
# se algum desses campos tiver NaN, a linha sera removida

df = df.dropna(
    subset=[
        "Ano",
        "Numero_mes",
        "valor_total"
    ]
)


# filtrar os dados que serão utilizados

df_filtrado = df[
    # primeira condição
    # mantem somente os registros de 2026
    (df["Ano"] == 2026)

    &

    # segunda condição
    # mantem somente os pedidos entregue
    (df["status"] == "ENTREGUE")

    & 

    # terceira condição
    # mantem somente os meses entre 1 e 6
    (df["Numero_mes"].between(1,6))  

].copy()

# calcular a receita total de cada mes

receita_mensal = (

    df_filtrado

    # agrupa os dados pela coluna Numero_mes
    .groupby(
        "Numero_mes",
        # mantem Numero_mes como uma coluna normal 
        as_index=False
    )

    # seleciona a coluna que queremos somar 
    ["valor_total"]

    # soma os valores de cada mes
    .sum()
)

# Ordena os dados pelo Numero_mes

receita_mensal = receita_mensal.sort_values(
    by="Numero_mes"
)

# Verificar se existem dados suficientes
# len() verifica quantas linha existem 

# para realizar a Regressão Linear 
# precisamos ter pelo menos dois meses

# se existirem menos de dois meses, 
# não faremos a previsão

if len(receita_mensal) < 2:
    # criar visual 

    # cria uma area para o visual
    # figsize define:
    # largura de 7
    # altura de 3
    plt.figure(
        figsize=(7,3)
    )

    # adicionar o titulo
    plt.text(
        0.5, # posição horizontal
        0.60, # posição vertical
        "PREVISÃO DE RECEITA", # texto exibido
        ha = 'center', # centraliza horiontalmente
        va = 'center', # centraliza verticalmente
        fontsize=16,# tomanho da fonte
        fontweight= "bold" # colocar o texto em negrito
    )

    # adicionar a mensagem principal
    plt.text(
        0.5,
        0.38,
        "Dados insuficientes para realizar a previsão",
        ha="center",
        va="center",
        fontsize=12
    )

    # adicionar uma explicação complementar 
    plt.text(
        0.5,
        0.20,
        "São necessarios pelo menos dois meses com dados",
        ha='center',
        va='center',
        fontsize=9
    )

    # remove os eixos do grafico
    plt.axis("off")

    # ajute automaticamente os elementos 
    # dentro da area do visual
    plt.tight_layout()

    # exibe o visual no power bi
    plt.show()

else:
    #  definir X e y

    # X representa o numero do mes
    X = receita_mensal[['Numero_mes']]

    # y representa a receita daquele mes 
    y = receita_mensal['valor_total']

    # modelo de regressão linear

    modelo = LinearRegression()

    # treinar o modelo

    modelo.fit(X,y)

   # ------------------------------------------------------------
# criar os meses que queremos prever
# ------------------------------------------------------------

meses_futuros = pd.DataFrame(
    {
        "Numero_mes": [7, 8, 9, 10, 11, 12]
    }
)


# ------------------------------------------------------------
# realizar as previsões
# ------------------------------------------------------------

previsoes = modelo.predict(
    meses_futuros
)


# adicionar as previsões ao dataframe
meses_futuros["Previsao"] = previsoes


# impedir valores negativos
# meses_futuros["Previsao"] = (
#     meses_futuros["Previsao"]
#     .clip(lower=0)
# )


# ------------------------------------------------------------
# nomes dos meses
# ------------------------------------------------------------

nomes_meses = {
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro"
}


# ------------------------------------------------------------
# criar visual
# ------------------------------------------------------------

plt.figure(
    figsize=(10, 6)
)


# ------------------------------------------------------------
# título
# ------------------------------------------------------------

plt.text(
    0.5,
    0.92,
    "PREVISÃO DE RECEITA",
    ha="center",
    va="center",
    fontsize=18,
    fontweight="bold",
    transform=plt.gca().transAxes
)


# ------------------------------------------------------------
# mostrar cada previsão
# ------------------------------------------------------------

posicao_y = 0.78


for _, linha in meses_futuros.iterrows():

    mes = int(
        linha["Numero_mes"]
    )

    valor = linha["Previsao"]


    # formatar valor
    valor_formatado = (
        f"{valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


    texto = (
        f"{nomes_meses[mes]}: "
        f"R$ {valor_formatado}"
    )


    plt.text(
        0.5,
        posicao_y,
        texto,
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold",
        transform=plt.gca().transAxes
    )


    # desce a posição do próximo mês
    posicao_y -= 0.11


# ------------------------------------------------------------
# informação sobre o modelo
# ------------------------------------------------------------

plt.text(
    0.5,
    0.05,
    "Modelo: Regressão Linear",
    ha="center",
    va="center",
    fontsize=11,
    transform=plt.gca().transAxes
)


# remover eixos
plt.axis("off")


plt.tight_layout()


plt.show()