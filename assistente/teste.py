
import pandas as pd

interacoes = pd.read_csv("dados/interacoes_limpas.csv", parse_dates=["data"])
produtos = pd.read_csv("dados/produtos.csv")

compras = interacoes[interacoes["evento"] == "compra"].merge(
    produtos, on="id_produto"
)
hoje = pd.Timestamp("2026-10-31")

rfm = compras.groupby("id_cliente").agg(
    recencia=(
        "data",
        lambda d: (hoje - d.max()).days,
    ),  # dias desde a última compra
    frequencia=("id_produto", "count"),  # quantas compras
    valor=("preco", "sum"),  # quanto gastou
)
print(rfm.sort_values("valor", ascending=False))


pesos = {"visualizacao": 1, "carrinho": 3, "compra": 5}
base = interacoes.merge(produtos[["id_produto", "categoria"]], on="id_produto")
base["peso"] = base["evento"].map(pesos)

pontos = base.groupby(["id_cliente", "categoria"])["peso"].sum().reset_index()
preferida = pontos.sort_values("peso", ascending=False).drop_duplicates(
    "id_cliente"
)
preferida = preferida.set_index("id_cliente")["categoria"].sort_index()
print(preferida.to_string())


from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

X = StandardScaler().fit_transform(rfm[["recencia", "frequencia", "valor"]])
modelo = KMeans(n_clusters=3, n_init=10, random_state=42)
rfm["segmento"] = modelo.fit_predict(X)
rfm["categoria_preferida"] = preferida

resumo = (
    rfm.groupby("segmento")[["recencia", "frequencia", "valor"]]
    .mean()
    .round(1)
)
print(resumo)
print()
print(
    rfm.sort_values("segmento")[["segmento", "valor", "categoria_preferida"]]
)


segmento_alto_valor = resumo["valor"].idxmax()


def mensagem(id_cliente):
    if id_cliente not in rfm.index:
        return "Bem-vindo(a)! Veja os mais vendidos da semana."
    cliente = rfm.loc[id_cliente]
    if cliente["segmento"] == segmento_alto_valor:
        categoria = cliente["categoria_preferida"]
        return f"Atendimento prioritário: novidades em {categoria} para você."
    return f"Ofertas selecionadas em {cliente['categoria_preferida']}."


for c in ["C08", "C05", "C12"]:
    print(c, "->", mensagem(c))
