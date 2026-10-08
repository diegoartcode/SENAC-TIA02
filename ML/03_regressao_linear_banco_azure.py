# pip list - para verificar bibliotecas instaladas 

# fazer instalação da biblioteca
# pip install mysql-connector-python 

# importa a biblioteca de conexão com mysql
import mysql.connector

# importa a biblioteca pandas
import pandas as pd

# pip install scikit-learn
#importa a biblioteca de ML
from sklearn.linear_model import LinearRegression

#importa a biblioteca de grafico
import matplotlib.pyplot as plt


# conexao com o banco
def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host='mysql-loja-tech-diego.mysql.database.azure.com',
            user='diegorodriguesdev',
            password='66613F@mili@13666',
            database='lojatech'
        )

        if conexao.is_connected():
            print('Conexão realizada com sucesso!')
            return conexao
    except mysql.connector.Error as erro:
        print(f'Erro ao conectar ao banco. {erro}')
        return None
    

 
conexao = conectar_banco()



cursor = conexao.cursor(
    dictionary=True
)


cursor.execute(
    '''
        SELECT 
        -- pega o ano da data de atualizado_em
        YEAR(atualizado_em) AS ano, 

        -- pega o mes da data de atualizado_em
        MONTH(atualizado_em) AS mes,

        -- pega o valor total
        ROUND(SUM(valor_total) ,2) AS faturamento

        from pedidos 

        where year(atualizado_em) = 2026 
        
        -- agrupa os resultados por ano e mes
        GROUP BY
            YEAR(atualizado_em),
            MONTH(atualizado_em)
        -- ordena o resultado primeiro pelo ano e depois pelo mes
        ORDER BY
            ano,
            mes        
        ;
    '''
)

pedidos = cursor.fetchall()

# criar DataFrame
df = pd.DataFrame(pedidos)

# imprimir o DataFrame
print(df)

# feature 
x = df[['mes']]

# target
y = df['faturamento']

modelo = LinearRegression()

modelo.fit(x,y)

previsoes_historicas = modelo.predict(x)

print(previsoes_historicas)


# conexao.close()


