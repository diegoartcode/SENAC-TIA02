# pip install mysql-connector-python

import mysql.connector 
conexao = mysql.connector.connect( 
    host="localhost", 
    user="root", 
    password="", 
    database="lojatech" 
    ) 
if conexao.is_connected(): 
    print( "Conexão realizada com sucesso!" )

cursor = conexao.cursor( dictionary=True )

cursor.execute( "SELECT * FROM produtos;" ) 
produtos = cursor.fetchall() 
print(produtos)

for produto in produtos:
    print(f'{produto['nome']} - {produto['preco_venda']}')