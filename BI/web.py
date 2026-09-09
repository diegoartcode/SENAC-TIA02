# pip install sweetviz
import sweetviz as sv
import pandas as pd

valores = [
    100,
    120,
    150,
    180,
    200
]

df = pd.DataFrame(valores)

analise = sv.analyze(df)

analise.show_html('analise_valores.html')