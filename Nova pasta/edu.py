# O código a seguir para criar um dataframe e remover as linhas duplicadas sempre é executado e age como um preâmbulo para o script:
 
# dataset = pandas.DataFrame(undefined, undefined.1, undefined.2, undefined.3, undefined.4)
# dataset = dataset.drop_duplicates()
 
# Cole ou digite aqui seu código de script:
 
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
 
# Copiar os dados recebidos do power bi (dataset)
 
df = dataset.copy()
 
# Padronizar a coluna status
 
# Selecionando a coluna 'status'
 
df["status"] = (
    # converte todoos os valores da coluna para texto
 
    df["status"].astype(str)
 
    # remove espaçosextrasantes e depois do texto
    # " ENTREGUE " > "ENTREGUE"
    .str.strip()
 
    # converte todos os textos em letras maiúsculas
    # "Entregue" > "ENTREGUE"
 
    .str.upper()
 
)
 
# converte a coluna Ano para numero
 
# errors = 'coerce' siginifica que, se existir algum valor que não pode ser convertido para numero, ele sera transformado em NaN
 
df['Ano'] = pd.to_numeric(
    df['Ano'],
    errors = 'coerce'
)
 
# converter a coluna Numero_mes para numero
# "1" > 1
# "2" > 2
 
df['numero_mes'] = pd.to_numeric(
    df['numero_mes'],
    errors = 'coerce'
)
 
# converter a coluna valor_total para numero
 
df['valor_total'] = pd.to_numeric(
    df['valor_total'],
    errors = 'coerce'
)
 
# remover ou remove linhas que tenha valores invalidos
# se algum desses campos tiver NaN, a linha sera removida
 
df = df.dropna(
    subset = [
        "Ano",
        "numero_mes",
        "valor_total"
    ]
)
 
# filtrar os dados que serão utilizados
df_filtrado = df[
    # primeira condição
    # mantem somente os registros de 2026
    (df['Ano'] == 2026)
    &
    # segunda condição
    # mantem somente os pedidos entregues
    (df["status"] == "ENTREGUE")
 
    &
 
    # terceira condição
    #mantem somente os meses entre 1 e 6
    (df["numero_mes"].between(1,6))

].copy()
 
# calcular a receita total de cada mes
 
receita_mensal = (
    df_filtrado
   
    # agrupa os dados pela coluna Numero_mes
    .groupby(
        "numero_mes",
        # mantem Numero_mes como uma coluna normal
        as_index = False
    )
    # seleciona a coluna que queremos somar
    ["valor_total"]
 
    # soma os valores de cadad mes
    .sum()
)
 
# ordena os dados pelo Numero_mes
 
receita_mensal = receita_mensal.sort_values(
    by = "numero_mes"
)
 
# verificar se existem daods suficientes
# len() verifica quantas linhas existem
 
# para realizar a Regressão Linear precisamos ter pelo menos dois meses
 
# se existirem menos de dois meses, nao faremos a previsao
 
if len(receita_mensal) < 2:
    # criar visual
 
    # cria uma area para o visual
    # figsize define:
    # largura de 7
    # altura de 3
    plt.figure(
        figsize = (7,3)
    )
 
    # adicionar o titulo
    plt.text(
        0.5, # posição horizontal
        0.60, # posição vertical
        "PREVISÃO DE RECEITA", # texto exibido
        ha = 'center', # centraliza horizontalmente
        va = 'center', # centraliza verticalmente
        fontsize = 16, # tamanho da fonte
        fontweight = "bold" # colocar o texto em negrito
    )
 
    # adicionar a menssagem principal
    plt.text(
        0.5,
        0.38,
        "Dados insuficientes para realizar a previsão",
        ha = "center",
        va = "center",
        fontsize = 12
    )
 
    # adicionar uma explicação complementar
    plt.text(
        0.5,
        0.2,
        "São necessários pelo menos dois meses com dados",
        ha = 'center',
        va = 'center',
        fontsize = 9
    )
 
    # remove os eixos do gráfico
    plt.axis("off")
 
    # ajuste automatico dos elementos dentro da area do visual
    plt.tight_layout()
 
    # exibe o visual no PowerBI
    plt.show()
 
else:
    # definir o X e o Y
   
    #  x representa o numero mes
    x = receita_mensal[['numero_mes']]
    # y representa a receita daquele mes
    y = receita_mensal['valor_total']
   
    # modelo de regressão linear
   
    modelo = LinearRegression()
   
    #treinar modelo
   
    modelo.fit(x,y)
   
    # informar o mes que queremos prever
   
    julho = pd.DataFrame(
        {
            "numero_mes" : [7]
           
        }
    )
   
    # realizar a previsão
    previsao_julho = modelo.predict(
        julho
    )[0]
   
    # formatar como moeda brasileira
   
    valor_formatado = (
        f"{previsao_julho:,.2f}"
        .replace(',','X')
        .replace('.',',')
        .replace('X','.')
    )
   
    # criar o visual com a aparencia de cartão
   
    plt.figure(
        figsize=(7,3)
    )
   
    # titulo principal
   
    plt.text(
        0.5,
        0.75,
        "Previsão do Receita",
        ha='center',
        va='center',
        fontsize=16,
        fontweight="bold"
    )
 
    # subtitulo
    plt.text(
        0.5,
        0.60,
        "Julho de 2026",
        ha = "center",
        va = "center",
        fontsize = 12
    )
 
    # valor previsto
    plt.text(
        0.5,
        0.38,
        f"R$ {valor_formatado}",
        ha = "center",
        va = "center",
        fontsize = 60,
        fontweight = "bold",
        fontstyle = "italic"
    )
   
    # informações do modelo utilizado
    plt.text(
        0.5,
        0.15,
        "Modelo; Regressão Linear",
        ha = "center",
        va = "center",
        fontsize = 13
    )
   
    # remover os eixos do grafico
    plt.axis("off")
 
    plt.show()
 