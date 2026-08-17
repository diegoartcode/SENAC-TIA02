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


LOAD DATA LOCAL INFILE 'C:/Users/diego.rjoaquim/Desktop/SENAC-TIA02/loja/dados/marcas.csv'
INTO TABLE marcas
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(marca_id, nome, site, ativo);
select * from categorias;


LOAD DATA LOCAL INFILE 'C:/Users/diego.rjoaquim/Desktop/SENAC-TIA02/loja/dados/centros_distribuicao.csv'
INTO TABLE centros_distribuicao
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(centro_id, nome, cidade, uf, ativo);


LOAD DATA LOCAL INFILE 'C:/Users/diego.rjoaquim/Desktop/SENAC-TIA02/loja/dados/produtos.csv'
INTO TABLE produtos
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(produto_id, sku, nome, slug, categoria_id, marca_id, fornecedor_id, preco_custo, preco_venda, peso_kg, garantia_meses, ativo, criado_em);


LOAD DATA LOCAL INFILE 'C:/Users/diego.rjoaquim/Desktop/SENAC-TIA02/loja/dados/estoques.csv'
INTO TABLE estoques
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(estoque_id, produto_id, centro_id, quantidade, reservado, ponto_reposicao, atualizado_em);


LOAD DATA LOCAL INFILE 'C:/Users/diego.rjoaquim/Desktop/SENAC-TIA02/loja/dados/clientes.csv'
INTO TABLE clientes
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(cliente_id, nome_completo, email, cpf, telefone, data_nascimento, criado_em, ativo);


LOAD DATA LOCAL INFILE 'C:/Users/diego.rjoaquim/Desktop/SENAC-TIA02/loja/dados/enderecos.csv'
INTO TABLE enderecos
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(endereco_id, cliente_id, tipo, logradouro, numero, @complemento, bairro, cidade, uf, cep, principal)
SET complemento = NULLIF(@complemento, '');


LOAD DATA LOCAL INFILE 'C:/Users/diego.rjoaquim/Desktop/SENAC-TIA02/loja/dados/cupons.csv'
INTO TABLE cupons
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(cupom_id, codigo, tipo_desconto, valor_desconto, valor_minimo, inicio_em, fim_em, limite_usos, usos_realizados, ativo);


LOAD DATA LOCAL INFILE 'C:/Users/diego.rjoaquim/Desktop/SENAC-TIA02/loja/dados/pedidos.csv'
INTO TABLE pedidos
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(pedido_id, cliente_id, endereco_entrega_id, status, subtotal, valor_desconto, valor_frete, valor_total, criado_em, atualizado_em);


LOAD DATA LOCAL INFILE 'C:/Users/diego.rjoaquim/Desktop/SENAC-TIA02/loja/dados/pedidos_cupons.csv'
INTO TABLE pedidos_cupons
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(pedido_id, cupom_id, valor_aplicado);


LOAD DATA LOCAL INFILE 'C:/Users/diego.rjoaquim/Desktop/SENAC-TIA02/loja/dados/itens_pedido.csv'
INTO TABLE itens_pedido
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(item_id, pedido_id, produto_id, centro_id, quantidade, preco_unitario, percentual_desconto, subtotal);


LOAD DATA LOCAL INFILE 'C:/Users/diego.rjoaquim/Desktop/SENAC-TIA02/loja/dados/pagamentos.csv'
INTO TABLE pagamentos
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(pagamento_id, pedido_id, metodo, parcelas, valor, status, codigo_transacao, @processado_em)
SET processado_em = NULLIF(@processado_em, '');


LOAD DATA LOCAL INFILE 'C:/Users/diego.rjoaquim/Desktop/SENAC-TIA02/loja/dados/entregas.csv'
INTO TABLE entregas
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(entrega_id, pedido_id, transportadora, codigo_rastreio, status, previsao_entrega, @enviado_em, @entregue_em)
SET enviado_em = NULLIF(@enviado_em, ''),
    entregue_em = NULLIF(@entregue_em, '');


LOAD DATA LOCAL INFILE 'C:/Users/diego.rjoaquim/Desktop/SENAC-TIA02/loja/dados/avaliacoes.csv'
INTO TABLE avaliacoes
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(avaliacao_id, cliente_id, produto_id, pedido_id, nota, titulo, comentario, criado_em, aprovado);


LOAD DATA LOCAL INFILE 'C:/Users/diego.rjoaquim/Desktop/SENAC-TIA02/loja/dados/movimentacoes_estoque.csv'
INTO TABLE movimentacoes_estoque
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(movimentacao_id, produto_id, centro_id, tipo, quantidade, referencia, criado_em);


LOAD DATA LOCAL INFILE 'C:/Users/diego.rjoaquim/Desktop/SENAC-TIA02/loja/dados/historico_status_pedido.csv'
INTO TABLE historico_status_pedido
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(historico_id, pedido_id, @status_anterior, status_novo, @observacao, alterado_em)
SET status_anterior = NULLIF(@status_anterior, ''),
    observacao = NULLIF(@observacao, '');

SET FOREIGN_KEY_CHECKS = 1;

SELECT 'categorias' AS tabela, COUNT(*) AS registros FROM categorias
UNION ALL SELECT 'produtos', COUNT(*) FROM produtos
UNION ALL SELECT 'clientes', COUNT(*) FROM clientes
UNION ALL SELECT 'pedidos', COUNT(*) FROM pedidos
UNION ALL SELECT 'itens_pedido', COUNT(*) FROM itens_pedido
UNION ALL SELECT 'pagamentos', COUNT(*) FROM pagamentos;


