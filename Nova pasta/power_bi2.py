# O código a seguir para criar um dataframe e remover as linhas duplicadas sempre é executado e age como um preâmbulo para o script:
 
# dataset = pandas.DataFrame(pedido_id,Ano,Numero_mes,status,valor_total)
# dataset = dataset.drop_duplicates()
 
# Cole ou digite aqui seu código de script:
# ============================================================
# LOJA TECH - PREVISÃO DE FATURAMENTO 2026
# POWER BI + PYTHON + MACHINE LEARNING
# ============================================================
 
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
 
 
# ------------------------------------------------------------
# FUNÇÃO PARA FORMATAR VALORES EM REAL
# ------------------------------------------------------------
 
def formatar_real(valor):
   
    # Exemplo:
    # 11264.28 -> R$ 11.264,28
   
    valor_formatado = f"{valor:,.2f}"
   
    valor_formatado = (
        valor_formatado
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )
   
    return f"R$ {valor_formatado}"
 
 
# ------------------------------------------------------------
# 1. RECEBER OS DADOS DO POWER BI
# ------------------------------------------------------------
 
df = dataset.copy()
 
 
# ------------------------------------------------------------
# 2. CONVERTER TIPOS
# ------------------------------------------------------------
 
df['Ano'] = pd.to_numeric(
    df['Ano'],
    errors='coerce'
)
 
df['Numero_mes'] = pd.to_numeric(
    df['Numero_mes'],
    errors='coerce'
)
 
df['valor_total'] = pd.to_numeric(
    df['valor_total'],
    errors='coerce'
)
 
 
# ------------------------------------------------------------
# 3. FILTRAR SOMENTE 2026
# ------------------------------------------------------------
 
df = df[
    df['Ano'] == 2026
]
 
 
# ------------------------------------------------------------
# 4. FILTRAR SOMENTE PEDIDOS ENTREGUES
# ------------------------------------------------------------
 
df = df[
    df['status'] == 'ENTREGUE'
]
 
 
# ------------------------------------------------------------
# 5. REMOVER VALORES INVÁLIDOS
# ------------------------------------------------------------
 
df = df.dropna(
    subset=[
        'Numero_mes',
        'valor_total'
    ]
)
 
 
# ------------------------------------------------------------
# 6. AGRUPAR FATURAMENTO POR MÊS
# ------------------------------------------------------------
 
faturamento_mensal = (
    df.groupby('Numero_mes')['valor_total']
      .sum()
      .reset_index()
)
 
 
# Ordenar pelos meses
faturamento_mensal = (
    faturamento_mensal
    .sort_values('Numero_mes')
)
 
 
# ------------------------------------------------------------
# 7. DESCOBRIR O ÚLTIMO MÊS
# ------------------------------------------------------------
 
ultimo_mes = int(
    faturamento_mensal['Numero_mes'].max()
)
 
 
# ------------------------------------------------------------
# 8. PREPARAR DADOS PARA MACHINE LEARNING
# ------------------------------------------------------------
 
# FEATURE
X = faturamento_mensal[
    ['Numero_mes']
]
 
 
# TARGET
y = faturamento_mensal[
    'valor_total'
]
 
 
# ------------------------------------------------------------
# 9. CRIAR E TREINAR MODELO
# ------------------------------------------------------------
 
modelo = LinearRegression()
 
modelo.fit(
    X,
    y
)
 
 
# ------------------------------------------------------------
# 10. CALCULAR LINHA DE TENDÊNCIA
# ------------------------------------------------------------
 
faturamento_mensal['tendencia'] = (
    modelo.predict(X)
)
 
 
# ------------------------------------------------------------
# 11. CRIAR MESES FUTUROS
# ------------------------------------------------------------
 
meses_futuros = list(
    range(
        ultimo_mes + 1,
        13
    )
)
 
 
df_futuro = pd.DataFrame({
    'Numero_mes': meses_futuros
})
 
 
# ------------------------------------------------------------
# 12. FAZER PREVISÕES
# ------------------------------------------------------------
 
if not df_futuro.empty:
 
    df_futuro['faturamento_previsto'] = (
        modelo.predict(
            df_futuro[['Numero_mes']]
        )
    )
 
 
# ------------------------------------------------------------
# 13. CRIAR GRÁFICO
# ------------------------------------------------------------
 
plt.figure(
    figsize=(14, 7)
)
 
 
# ------------------------------------------------------------
# DADOS REAIS
# ------------------------------------------------------------
 
plt.plot(
    faturamento_mensal['Numero_mes'],
    faturamento_mensal['valor_total'],
    marker='o',
    markersize=8,
    linewidth=3,
    label='Faturamento Real'
)
 
 
# ------------------------------------------------------------
# VALORES ESCRITOS NOS DADOS REAIS
# ------------------------------------------------------------
 
for _, linha in faturamento_mensal.iterrows():
 
    mes = linha['Numero_mes']
    valor = linha['valor_total']
 
    plt.annotate(
        formatar_real(valor),
 
        # Posição do ponto
        (mes, valor),
 
        # Distância do texto em relação ao ponto
        xytext=(0, 12),
 
        # Coordenadas relativas ao ponto
        textcoords='offset points',
 
        # Centraliza o texto
        ha='center',
 
        # Tamanho da fonte
        fontsize=9,
 
        # Deixa o texto em negrito
        fontweight='bold'
    )
 
 
# ------------------------------------------------------------
# LINHA DE TENDÊNCIA
# ------------------------------------------------------------
 
plt.plot(
    faturamento_mensal['Numero_mes'],
    faturamento_mensal['tendencia'],
    linestyle='--',
    linewidth=2,
    label='Tendência'
)
 
 
# ------------------------------------------------------------
# PREVISÕES
# ------------------------------------------------------------
 
if not df_futuro.empty:
 
    plt.plot(
        df_futuro['Numero_mes'],
        df_futuro['faturamento_previsto'],
        marker='o',
        markersize=8,
        linestyle='--',
        linewidth=3,
        label='Previsão'
    )
 
 
    # --------------------------------------------------------
    # VALORES ESCRITOS NAS PREVISÕES
    # --------------------------------------------------------
 
    for _, linha in df_futuro.iterrows():
 
        mes = linha['Numero_mes']
        valor = linha['faturamento_previsto']
 
        plt.annotate(
            formatar_real(valor),
 
            # Localização do ponto
            (mes, valor),
 
            # Coloca o texto abaixo do ponto
            xytext=(0, -22),
 
            textcoords='offset points',
 
            ha='center',
 
            fontsize=9,
 
            fontweight='bold'
        )
 
 
    # --------------------------------------------------------
    # CONECTAR ÚLTIMO VALOR REAL À PRIMEIRA PREVISÃO
    # --------------------------------------------------------
 
    plt.plot(
        [
            ultimo_mes,
            df_futuro.iloc[0]['Numero_mes']
        ],
 
        [
            faturamento_mensal.iloc[-1]['valor_total'],
            df_futuro.iloc[0]['faturamento_previsto']
        ],
 
        linestyle='--',
        linewidth=2
    )
 
 
# ------------------------------------------------------------
# NOMES DOS MESES
# ------------------------------------------------------------
 
nomes_meses = [
    'Jan',
    'Fev',
    'Mar',
    'Abr',
    'Mai',
    'Jun',
    'Jul',
    'Ago',
    'Set',
    'Out',
    'Nov',
    'Dez'
]
 
 
plt.xticks(
    range(1, 13),
    nomes_meses,
    fontsize=10
)
 
 
# ------------------------------------------------------------
# CONFIGURAÇÕES
# ------------------------------------------------------------
 
plt.title(
    'Faturamento Real e Previsão - 2026',
    fontsize=16,
    fontweight='bold'
)
 
 
plt.xlabel(
    'Mês',
    fontsize=11
)
 
 
plt.ylabel(
    'Faturamento (R$)',
    fontsize=11
)
 
 
plt.grid(
    True,
    alpha=0.3
)
 
 
plt.legend()
 
 
# Cria um espaço extra acima e abaixo
# para os valores não serem cortados
 
plt.margins(
    x=0.03,
    y=0.20
)
 
 
plt.tight_layout()
 
 
# ------------------------------------------------------------
# EXIBIR GRÁFICO
# ------------------------------------------------------------
 
plt.show()