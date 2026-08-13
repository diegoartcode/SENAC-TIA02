USE lojatech;

-- desativa temporariamente a verificação de chaves 
-- estrangeiras. Isso permite limpar tabelas que possuem 
-- relacionamentos entre si sem que o MySQL impeça os 
-- TRUNCATE por causa das referências.
SET FOREIGN_KEY_CHECKS = 0;
SELECT * FROM categorias;
SHOW VARIABLES LIKE 'local_infile';

SET GLOBAL local_infile = 1;

-- limpa o historico de alterações de status dos pedidos
TRUNCATE TABLE historico_status_pedido;
TRUNCATE TABLE movimentacoes_estoque;
TRUNCATE TABLE avaliacoes;
TRUNCATE TABLE entregas;
TRUNCATE TABLE pagamentos;
TRUNCATE TABLE itens_pedido;
TRUNCATE TABLE pedidos_cupons;
TRUNCATE TABLE pedidos;
TRUNCATE TABLE cupons;
TRUNCATE TABLE enderecos;
TRUNCATE TABLE clientes;
TRUNCATE TABLE estoques;
TRUNCATE TABLE produtos;
TRUNCATE TABLE centros_distribuicao;
TRUNCATE TABLE fornecedores;
TRUNCATE TABLE marcas;
TRUNCATE TABLE categorias;
SET FOREIGN_KEY_CHECKS = 1;
-- importa os dados do arquivo categoria.csv para a tabela
-- categoria 
LOAD DATA LOCAL INFILE
 'C:/Users/diego.rjoaquim/Desktop/SENAC-TIA02/loja/dados/categorias.csv'
-- define a tabela que receberá os dados importados
INTO TABLE categorias
-- informa que o arquivo CSV utiliza a codificação UTF-8,
-- para caracteres especiais com Ç, ã, é, etc...
CHARACTER SET utf8mb4
-- define a virgula como separador entre os campos do 
-- arquivo CSV
-- OPTIONALLY ENCLOSED BY '"': permite que os campos
-- possam estar entre aspas duplas
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'

-- define que a cada registro termina com uma 
-- quebra de linha
LINES TERMINATED BY '\n'

-- ignora a primeira linha 
IGNORE 1 LINES

-- define a ordem das colunas que serão importadas.
(categoria_id,nome,slug,@categoria_pai_id,ativo
)
-- atribua a categoria_pai_id o valor de @categoria_pai_id,
-- mas transforme um string vazia ('') em um null
SET categoria_pai_id = NULLIF(@categoria_pai_id, '');



-- fornecedores 

LOAD DATA LOCAL INFILE 'C:/Users/diego.rjoaquim/Desktop/SENAC-TIA02/loja/dados/fornecedores.csv'
INTO TABLE fornecedores
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(fornecedor_id, razao_social, nome_fantasia, cnpj, email, telefone, prazo_medio_dias, ativo);


