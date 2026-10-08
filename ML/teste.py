# O código a seguir para criar um dataframe e remover as linhas duplicadas sempre é executado e age como um preâmbulo para o script: 

# dataset = pandas.DataFrame(pedido_id, valor_total)
# dataset = dataset.drop_duplicates()

# Cole ou digite aqui seu código de script:


import pandas as pd
import matplotlib.pyplot as plt


df = dataset.copy()



plt.figure(figsize=(8, 4))

plt.bar(
    df["pedido_id"].astype(str),
    df["valor_total"]
)

plt.title("Valor dos pedidos - LojaTech")
plt.xlabel("Pedido")
plt.ylabel("Valor Total")

plt.xticks(rotation=90)

plt.tight_layout()
plt.show()