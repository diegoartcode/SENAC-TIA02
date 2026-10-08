# importa a biblioteca de conexão com mysql
import mysql.connector

# importa a biblioteca pandas
import pandas as pd

# conexao com o banco
def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='lojatech'
        )

        if conexao.is_connected():
            print('Conexão realizada com sucesso!')
            return conexao
    except mysql.connector.Error as erro:
        print(f'Erro ao conectar ao banco. {erro}')
        return None
    
conexao = conectar_banco()


sql = '''
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

# executa a consulta com pandas
if conexao is not None:
    # executa a consulta SQL 
    # o pandas transforma automaticamente o resultado em um DataFrame
    df = pd.read_sql(sql,conexao) 
    print('----- FATURAMENTO MENSAL -----')

    # mostrar o DataFrame
    print(df)

# fecha a conexão
if conexao is not None and conexao.is_connected():
    conexao.close()
    print('Conexão encerrada.')
