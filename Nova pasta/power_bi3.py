# ============================================================
# LOJA TECH
# PREVISÃO DE RECEITA PARA JULHO DE 2026
# ============================================================

# O Power BI cria automaticamente um DataFrame chamado "dataset"
# com os campos adicionados ao visual Python.
#
# Exemplo de campos utilizados:
# pedido_id
# Ano
# Numero_mes
# status
# valor_total


# ------------------------------------------------------------
# 1. IMPORTAR AS BIBLIOTECAS
# ------------------------------------------------------------

# Importa a biblioteca Pandas.
# Ela será utilizada para trabalhar com tabelas,
# organizar, filtrar e transformar os dados.
import pandas as pd


# Importa a biblioteca Matplotlib.
# Ela será utilizada para criar o visual final
# que será exibido dentro do Power BI.
import matplotlib.pyplot as plt


# Importa o algoritmo de Regressão Linear
# da biblioteca Scikit-Learn.
#
# Esse será o modelo de Machine Learning
# utilizado para prever a receita de julho.
from sklearn.linear_model import LinearRegression



# ------------------------------------------------------------
# 2. COPIAR OS DADOS RECEBIDOS DO POWER BI
# ------------------------------------------------------------

# O Power BI disponibiliza os dados através
# de um DataFrame chamado "dataset".
#
# Aqui criamos uma cópia chamada "df"
# para trabalhar com os dados sem alterar
# diretamente o DataFrame original.
df = dataset.copy()



# ------------------------------------------------------------
# 3. PADRONIZAR A COLUNA STATUS
# ------------------------------------------------------------

# Selecionamos a coluna "status".
df["status"] = (

    # Converte todos os valores da coluna para texto.
    df["status"]
    .astype(str)

    # Remove espaços extras antes e depois do texto.
    # Exemplo:
    # " ENTREGUE " -> "ENTREGUE"
    .str.strip()

    # Converte todos os textos para letras maiúsculas.
    # Exemplo:
    # "Entregue" -> "ENTREGUE"
    .str.upper()
)



# ------------------------------------------------------------
# 4. CONVERTER AS COLUNAS PARA VALORES NUMÉRICOS
# ------------------------------------------------------------

# Converte a coluna Ano para número.
#
# errors="coerce" significa que, se existir algum valor
# que não possa ser convertido para número,
# ele será transformado em NaN.
df["Ano"] = pd.to_numeric(
    df["Ano"],
    errors="coerce"
)


# Converte a coluna Numero_mes para número.
#
# Exemplo:
# "1" -> 1
# "2" -> 2
df["Numero_mes"] = pd.to_numeric(
    df["Numero_mes"],
    errors="coerce"
)


# Converte a coluna valor_total para número.
#
# Essa conversão é necessária porque mais adiante
# iremos somar os valores dos pedidos.
df["valor_total"] = pd.to_numeric(
    df["valor_total"],
    errors="coerce"
)



# ------------------------------------------------------------
# 5. REMOVER REGISTROS INVÁLIDOS
# ------------------------------------------------------------

# Remove linhas que tenham valores inválidos
# nas colunas:
#
# Ano
# Numero_mes
# valor_total
#
# Se algum desses campos tiver NaN,
# a linha será removida.
df = df.dropna(
    subset=[
        "Ano",
        "Numero_mes",
        "valor_total"
    ]
)



# ------------------------------------------------------------
# 6. FILTRAR OS DADOS QUE SERÃO UTILIZADOS
# ------------------------------------------------------------

# Vamos trabalhar somente com:
#
# Ano = 2026
# Status = ENTREGUE
# Meses de janeiro até junho
#
# Janeiro = 1
# Fevereiro = 2
# Março = 3
# Abril = 4
# Maio = 5
# Junho = 6

df_filtrado = df[

    # Primeira condição:
    # mantém somente os registros de 2026.
    (df["Ano"] == 2026)

    &

    # Segunda condição:
    # mantém somente os pedidos entregues.
    (df["status"] == "ENTREGUE")

    &

    # Terceira condição:
    # mantém somente os meses entre 1 e 6.
    (df["Numero_mes"].between(1, 6))

].copy()



# ------------------------------------------------------------
# 7. CALCULAR A RECEITA TOTAL DE CADA MÊS
# ------------------------------------------------------------

# Agrupamos os pedidos pelo número do mês
# e somamos o valor_total.
#
# Exemplo:
#
# Janeiro:
# 1000
# 500
# 200
#
# Receita de Janeiro = 1700

receita_mensal = (

    df_filtrado

    # Agrupa os dados pela coluna Numero_mes.
    .groupby(
        "Numero_mes",

        # Mantém Numero_mes como uma coluna normal
        # no resultado.
        as_index=False
    )

    # Seleciona a coluna que queremos somar.
    ["valor_total"]

    # Soma os valores de cada mês.
    .sum()
)



# ------------------------------------------------------------
# 8. ORDENAR OS MESES
# ------------------------------------------------------------

# Ordena os dados pelo número do mês.
#
# Isso garante a sequência:
#
# 1 - Janeiro
# 2 - Fevereiro
# 3 - Março
# 4 - Abril
# 5 - Maio
# 6 - Junho

receita_mensal = receita_mensal.sort_values(
    by="Numero_mes"
)



# ------------------------------------------------------------
# 9. VERIFICAR SE EXISTEM DADOS SUFICIENTES
# ------------------------------------------------------------

# len() verifica quantas linhas existem
# no DataFrame receita_mensal.
#
# Para realizar a Regressão Linear
# precisamos ter pelo menos dois meses.
#
# Se existirem menos de dois meses,
# não faremos a previsão.

if len(receita_mensal) < 2:


    # --------------------------------------------------------
    # CRIAR VISUAL DE AVISO
    # --------------------------------------------------------

    # Cria uma área para o visual.
    #
    # figsize define:
    # largura = 7
    # altura = 3
    plt.figure(
        figsize=(7, 3)
    )


    # Adiciona o título.
    plt.text(

        # Posição horizontal.
        0.5,

        # Posição vertical.
        0.60,

        # Texto exibido.
        "PREVISÃO DE RECEITA",

        # Centraliza horizontalmente.
        ha="center",

        # Centraliza verticalmente.
        va="center",

        # Tamanho da fonte.
        fontsize=16,

        # Coloca o texto em negrito.
        fontweight="bold"
    )


    # Adiciona a mensagem principal.
    plt.text(
        0.5,
        0.38,
        "Dados insuficientes para realizar a previsão.",
        ha="center",
        va="center",
        fontsize=12
    )


    # Adiciona uma explicação complementar.
    plt.text(
        0.5,
        0.20,
        "São necessários pelo menos dois meses com dados.",
        ha="center",
        va="center",
        fontsize=9
    )


    # Remove os eixos do gráfico.
    #
    # Como queremos criar um visual parecido
    # com um cartão, não precisamos de eixo X ou Y.
    plt.axis("off")


    # Ajusta automaticamente os elementos
    # dentro da área do visual.
    plt.tight_layout()


    # Exibe o visual no Power BI.
    plt.show()



# ------------------------------------------------------------
# 10. CASO EXISTAM DADOS SUFICIENTES
# ------------------------------------------------------------

else:


    # --------------------------------------------------------
    # 11. DEFINIR A VARIÁVEL X
    # --------------------------------------------------------

    # X representa a informação que será usada
    # pelo modelo para tentar prever a receita.
    #
    # Neste exemplo, X será o número do mês.
    #
    # Janeiro = 1
    # Fevereiro = 2
    # Março = 3
    # Abril = 4
    # Maio = 5
    # Junho = 6
    #
    # Os dois pares de colchetes são utilizados
    # porque o Scikit-Learn espera uma estrutura
    # bidimensional para X.

    X = receita_mensal[
        ["Numero_mes"]
    ]



    # --------------------------------------------------------
    # 12. DEFINIR A VARIÁVEL y
    # --------------------------------------------------------

    # y representa aquilo que queremos prever.
    #
    # Neste caso:
    #
    # y = receita de cada mês.

    y = receita_mensal[
        "valor_total"
    ]



    # --------------------------------------------------------
    # 13. CRIAR O MODELO DE MACHINE LEARNING
    # --------------------------------------------------------

    # Criamos um objeto utilizando o algoritmo
    # de Regressão Linear.
    #
    # Neste momento o modelo ainda não foi treinado.

    modelo = LinearRegression()



    # --------------------------------------------------------
    # 14. TREINAR O MODELO
    # --------------------------------------------------------

    # O método fit() realiza o treinamento.
    #
    # O modelo recebe:
    #
    # X = número do mês
    # y = receita daquele mês
    #
    # Com essas informações ele tenta encontrar
    # uma relação matemática entre mês e receita.

    modelo.fit(
        X,
        y
    )



    # --------------------------------------------------------
    # 15. INFORMAR O MÊS QUE QUEREMOS PREVER
    # --------------------------------------------------------

    # Julho é o mês número 7.
    #
    # Criamos um pequeno DataFrame contendo
    # apenas esse mês.

    julho = pd.DataFrame({

        "Numero_mes": [7]

    })



    # --------------------------------------------------------
    # 16. REALIZAR A PREVISÃO
    # --------------------------------------------------------

    # O método predict() pede para o modelo
    # realizar uma previsão.
    #
    # Estamos perguntando:
    #
    # "Qual seria a receita estimada
    # para o mês número 7?"
    #
    # O [0] pega o primeiro valor retornado
    # pelo modelo.

    previsao_julho = modelo.predict(
        julho
    )[0]



    # --------------------------------------------------------
    # 17. EVITAR PREVISÃO NEGATIVA
    # --------------------------------------------------------

    # Dependendo da tendência dos dados,
    # uma Regressão Linear pode gerar
    # um valor negativo.
    #
    # Para esse exemplo de receita,
    # não queremos mostrar uma previsão negativa.
    #
    # max() compara:
    #
    # previsão
    # e
    # zero
    #
    # e mantém o maior valor.

    previsao_julho = max(
        previsao_julho,
        0
    )



    # --------------------------------------------------------
    # 18. FORMATAR O VALOR COMO MOEDA BRASILEIRA
    # --------------------------------------------------------

    # Inicialmente o Python utiliza o formato:
    #
    # 291,460.67
    #
    # Queremos transformar para:
    #
    # 291.460,67

    valor_formatado = (

        # Formata com separador de milhar
        # e duas casas decimais.
        f"{previsao_julho:,.2f}"

        # Troca temporariamente a vírgula por X.
        .replace(",", "X")

        # Troca o ponto decimal por vírgula.
        .replace(".", ",")

        # Troca o X pelo ponto de milhar.
        .replace("X", ".")
    )



    # --------------------------------------------------------
    # 19. CRIAR O VISUAL FINAL
    # --------------------------------------------------------

    # Cria a área do visual.
    plt.figure(
        figsize=(7, 3)
    )



    # --------------------------------------------------------
    # 20. TÍTULO DO VISUAL
    # --------------------------------------------------------

    plt.text(

        # Centraliza horizontalmente.
        0.5,

        # Define a posição vertical.
        0.75,

        # Texto exibido.
        "PREVISÃO DE RECEITA",

        ha="center",
        va="center",

        # Tamanho da fonte.
        fontsize=16,

        # Texto em negrito.
        fontweight="bold"
    )



    # --------------------------------------------------------
    # 21. SUBTÍTULO
    # --------------------------------------------------------

    plt.text(
        0.5,
        0.60,
        "Julho de 2026",
        ha="center",
        va="center",
        fontsize=12
    )



    # --------------------------------------------------------
    # 22. MOSTRAR O VALOR PREVISTO
    # --------------------------------------------------------

    # Utilizamos uma f-string para juntar:
    #
    # R$
    #
    # com:
    #
    # valor_formatado

    plt.text(
        0.5,
        0.38,

        f"R$ {valor_formatado}",

        ha="center",
        va="center",

        # Valor grande para destacar a previsão.
        fontsize=60,

        # Deixa o valor em negrito.
        fontweight="bold"
    )



    # --------------------------------------------------------
    # 23. INFORMAÇÃO SOBRE O MODELO
    # --------------------------------------------------------

    plt.text(
        0.5,
        0.15,
        "Modelo: Regressão Linear",
        ha="center",
        va="center",
        fontsize=9
    )



    # --------------------------------------------------------
    # 24. REMOVER OS EIXOS
    # --------------------------------------------------------

    # Remove os eixos X e Y.
    #
    # Dessa forma o gráfico fica com aparência
    # semelhante a um cartão do Power BI.

    plt.axis("off")



    # --------------------------------------------------------
    # 25. AJUSTAR O LAYOUT
    # --------------------------------------------------------

    # Organiza automaticamente os elementos
    # para evitar cortes no visual.

    plt.tight_layout()



    # --------------------------------------------------------
    # 26. EXIBIR O VISUAL NO POWER BI
    # --------------------------------------------------------

    # Exibe o resultado final.

    plt.show()