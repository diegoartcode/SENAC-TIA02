-- cria o banco de dados apenas se ele ainda não existir
CREATE DATABASE IF NOT EXISTS lojatech
-- define o conjunto de caracteres com utf8mb4 
-- que suporta todos os caracteres Unicode, 
-- incluindo emojis e acentuação completa
CHARACTER SET utf8mb4
-- define a collation 
-- (regras de comparação/ ordenação de string)
-- utf8mb4_unicode_ci: comparação baseada em regras Unicode
-- "ci": case insensitive (não diferencia 
-- maiusculas de minusculas)
COLLATE utf8mb4_unicode_ci;

-- Seleciona o banco de dados 
-- todos os comandos seguinte serão execudados dentro dele
USE lojatech;

-- define a codificação de caracteres usada na conexão atual 
-- (cliente <-> servidor)
-- Garante que os dados enviados e recebidos usem utf8mb4
SET NAMES utf8mb4;


CREATE TABLE IF NOT EXISTS categorias(
categoria_id INT unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
nome VARCHAR(100) NOT NULL UNIQUE,
slug VARCHAR(120) NOT NULL UNIQUE,
categoria_pai_id INT UNSIGNED NULL,
ativo BOOLEAN NOT NULL DEFAULT TRUE,
-- PRIMARY KEY (categoria_id),
CONSTRAINT fk_categorias_pai 
foreign key(categoria_pai_id) REFERENCES categorias(categoria_id)
ON UPDATE CASCADE -- se o id do pai mudar, atualiza os 
-- filhos automaticamente
ON DELETE SET NULL -- se o pai for excluido, os 
-- filhos viram categoria raiz (e não são apagados)
);

CREATE TABLE IF NOT EXISTS marcas(
marca_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
nome VARCHAR(100) NOT NULL UNIQUE,
site VARCHAR(255) NULL,
ativo BOOLEAN NOT NULL DEFAULT TRUE
);


CREATE TABLE IF NOT EXISTS fornecedores(
fornecedor_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
razao_social VARCHAR(150) NOT NULL,
nome_fantasia VARCHAR(120) NOT NULL,
cnpj CHAR(14), 
email VARCHAR(150) NOT NULL,
telefone VARCHAR(20) NULL,
ativo BOOLEAN NOT NULL DEFAULT TRUE,
-- SMALLINT: numero inteiro pequeno 
-- UNSIGNED: numero positivo 
prazo_medio_dias SMALLINT UNSIGNED NOT NULL DEFAULT 7
CHECK (prazo_medio_dias BETWEEN 1 AND 180)
);


CREATE TABLE IF NOT EXISTS centros_distribuicao(
centro_id INT UNSIGNED NOT NULL  AUTO_INCREMENT PRIMARY KEY,
nome VARCHAR(120) NOT NULL UNIQUE,
cidade VARCHAR(100) NOT NULL,
uf CHAR(2) NOT NULL,
ativo BOOLEAN NOT NULL DEFAULT TRUE 
);

CREATE TABLE IF NOT EXISTS produtos(
produto_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
sku VARCHAR(30) NOT NULL UNIQUE,
nome VARCHAR(160) NOT NULL,
slug VARCHAR(180) NOT NULL UNIQUE,
categoria_id INT UNSIGNED NOT NULL,
marca_id INT UNSIGNED NOT NULL,
fornecedor_id INT UNSIGNED NOT NULL,
preco_custo DECIMAL(10,2) UNSIGNED NOT NULL,
preco_venda DECIMAL(10,2) UNSIGNED NOT NULL,
peso_kg DECIMAL(8,3) UNSIGNED NOT NULL,
garantia_meses SMALLINT UNSIGNED NOT NULL DEFAULT 3,
ativo BOOLEAN NOT NULL DEFAULT TRUE,
criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- NOW()
CONSTRAINT fk_produto_categoria FOREIGN KEY (categoria_id)
	REFERENCES categorias (categoria_id)
    -- impede excluir uma categoria que ainda tenha produtos
    -- vinculados a categoria (delete restrict)
    ON UPDATE CASCADE ON DELETE RESTRICT,
CONSTRAINT fk_produto_marca FOREIGN KEY (marca_id)
	REFERENCES marcas (marca_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
CONSTRAINT fk_produto_fornecedor FOREIGN KEY (fornecedor_id)
	REFERENCES fornecedores (fornecedor_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
    -- regra de negocio: preço de venda deve ser sempre maior que zero
    -- e o preço de custo nunca pode ser negativo
CONSTRAINT chk_produtos_precos 
	CHECK (preco_venda > 0 AND preco_custo >=0),   

INDEX idx_produtos_nome(nome),
INDEX idx_produtos_categoria_ativo(categoria_id,ativo),
INDEX idx_produtos_marca(marca_id)
);

CREATE TABLE estoque(
estoque_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
produto_id INT UNSIGNED NOT NULL,
centro_id INT UNSIGNED NOT NULL,
quantidade INT UNSIGNED NOT NULL DEFAULT 0,
reservado INT UNSIGNED NOT NULL DEFAULT 0,
ponto_reposicao INT UNSIGNED NOT NULL DEFAULT 10,
-- DEFAULT CURRENT_TIMESTAMP: preenchido automaticamnete na criação
-- pela data e hora atual
-- ON UPDATE CURRENT_TIMESTAMP: atualizado automaticamente sempre
-- que a linha for modificada 
atualizado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP 
ON UPDATE CURRENT_TIMESTAMP, 

CONSTRAINT  fk_estoque_produto FOREIGN KEY (produto_id)
REFERENCES produtos (produto_id)
ON UPDATE CASCADE ON DELETE CASCADE,

CONSTRAINT fk_estoque_centro FOREIGN KEY (centro_id)
REFERENCES centro_distribuicao (centro_id)
ON UPDATE CASCADE ON DELETE RESTRICT,

CONSTRAINT chk_estoque_reserva CHECK (reservado <= quantidade),

INDEX idx_estoque_nivel (quantidade, ponto_reposicao) 
);


CREATE TABLE IF NOT EXISTS clientes(
cliente_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
nome_completo VARCHAR(150) NOT NULL,
email VARCHAR(150) NOT NULL,
cpf CHAR(11) NOT NULL,
telefone VARCHAR(20) NOT NULL,
data_nascimento DATE NULL,
criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
ativo BOOLEAN NOT NULL DEFAULT TRUE,
INDEX idx_clientes_nome (nome_completo),
INDEX idx_clientes_criado_em(criado_em)
);

CREATE TABLE IF NOT EXISTS endereco(
endereco_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
cliente_id INT UNSIGNED NOT NULL,
tipo VARCHAR(20) NOT NULL DEFAULT 'ENTREGA' 
CHECK (tipo in ('ENTREGA', 'COBRANCA')),
logradouro VARCHAR(160) NOT NULL,
numero VARCHAR(20) NOT NULL,
complemento VARCHAR(80) NOT NULL,
bairro VARCHAR(100) NOT NULL,
cidade VARCHAR(100) NOT NULL,
uf CHAR(2) NOT NULL,
cep CHAR(8) NOT NULL,
principal BOOLEAN NOT NULL DEFAULT FALSE,
CONSTRAINT fk_enderecos_cliente FOREIGN KEY (cliente_id)
	REFERENCES clientes(cliente_id),
INDEX idx_enderecos_cliente (cliente_id),
INDEX idx_enderecos_cep (cep)
);

CREATE TABLE IF NOT EXISTS cupons(
cupom_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
codigo VARCHAR(30) NOT NULL UNIQUE,
tipo_desconto VARCHAR(20) NOT NULL 
CHECK (tipo_desconto IN ('PERCENTUAL','VALOR_FIXO')),
valor_desconto DECIMAL(10,2) UNSIGNED NOT NULL,
valor_minimo DECIMAL(10,2) UNSIGNED NOT NULL DEFAULT 0,
inicio_em DATETIME NOT NULL,
fim_em DATETIME NOT NULL,
limite_usos INT UNSIGNED NOT NULL,
usos_realizados INT UNSIGNED NOT NULL DEFAULT 0,
CONSTRAINT chk_cupons_datas 
CHECK (fim_em > inicio_em),
CONSTRAINT chk_cupons_uso 
CHECK (usos_realizados <= limite_usos),
CONSTRAINT chk_cupons_percentual CHECK (
	tipo_desconto <> 'PERCENTUAL' 
    OR valor_desconto BETWEEN 0 AND 100
)
);

CREATE TABLE pedidos(
	pedido_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT UNSIGNED NOT NULL,
    endereco_entrega_id INT UNSIGNED NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'PENDENTE_PAGAMENTO' 
		CHECK (status IN (
			'PENDENTE_PAGAMENTO',
            'PAGAMENTO_APROVADO',
            'EM_SEPARACAO',
            'ENVIADO',
            'ENTREGUE',
            'CANCELADO'
        )),
	subtotal DECIMAL(12,2) UNSIGNED NOT NULL DEFAULT 0,
    valor_desconto DECIMAL(12,2) UNSIGNED NOT NULL DEFAULT 0,
	valor_frete DECIMAL(10,2) UNSIGNED NOT NULL DEFAULT 0,
    valor_total DECIMAL(12,2) UNSIGNED NOT NULL DEFAULT 0,   
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP 
		ON UPDATE CURRENT_TIMESTAMP,
	
    CONSTRAINT fk_pedidos_cliente FOREIGN KEY (cliente_id)
		REFERENCES clientes (cliente_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
        
	CONSTRAINT fk_pedidos_endereco FOREIGN KEY (endereco_entrega_id)
		REFERENCES enderecos(endereco_id)
		ON UPDATE CASCADE ON DELETE RESTRICT,
        
	INDEX idx_pedidos_cliente_data (cliente_id,criado_em),
    INDEX idx_pedidos_status_data (status, criado_em)	
);







