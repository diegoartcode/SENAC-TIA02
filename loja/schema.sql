-- Cria o banco de dados "lojatech" apenas se ele ainda não existir
-- (evita erro caso o banco já tenha sido criado anteriormente)
CREATE DATABASE IF NOT EXISTS lojatech
  -- Define o conjunto de caracteres como utf8mb4, que suporta
  -- todos os caracteres Unicode, incluindo emojis e acentuação completa
  CHARACTER SET utf8mb4
  -- Define a collation (regras de comparação/ordenação de strings)
  -- utf8mb4_unicode_ci: comparação baseada em regras Unicode,
  -- "ci" = case insensitive (não diferencia maiúsculas de minúsculas)
  COLLATE utf8mb4_unicode_ci;
 

-- Seleciona o banco "lojatech" como o banco de dados ativo
-- (todos os comandos seguintes serão executados dentro dele)
USE lojatech;

-- Define a codificação de caracteres usada na conexão atual (cliente <-> servidor)
-- Garante que os dados enviados e recebidos usem utf8mb4,
-- evitando problemas com acentuação, emojis, etc.
SET NAMES utf8mb4;


-- Cria a tabela "categorias" (versão com sintaxe mais compacta)
CREATE TABLE categorias (
  -- Identificador único da categoria
  -- PRIMARY KEY já declarada aqui mesmo (inline), sem precisar de
  -- uma linha separada como "PRIMARY KEY (categoria_id)"
  categoria_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  -- Nome da categoria, com UNIQUE aplicado diretamente na coluna
  -- (equivale a CONSTRAINT uq_categorias_nome UNIQUE (nome) da versão anterior,
  -- mas o MySQL vai gerar um nome automático para essa constraint)
  nome VARCHAR(100) NOT NULL UNIQUE,
  -- Slug (versão amigável do nome para URLs), também único
  slug VARCHAR(120) NOT NULL UNIQUE,
  -- Referência à categoria "pai" (auto-relacionamento, permite subcategorias)
  -- NULL = categoria de nível raiz (sem "pai")
  categoria_pai_id INT UNSIGNED NULL,
  -- Indica se a categoria está ativa; TRUE por padrão
  ativo BOOLEAN NOT NULL DEFAULT TRUE,
  -- Chave estrangeira nomeada explicitamente (fk_categorias_pai)
  -- ligando categoria_pai_id ao próprio categoria_id da tabela
  CONSTRAINT fk_categorias_pai
    FOREIGN KEY (categoria_pai_id) REFERENCES categorias (categoria_id)
    ON UPDATE CASCADE   -- se o id do pai mudar, atualiza os filhos automaticamente
    ON DELETE SET NULL  -- se o pai for excluído, os filhos viram categoria raiz (não são apagados)

) ENGINE=InnoDB;

-- Cria a tabela "marcas", que armazena os fabricantes/marcas dos produtos
-- (ex: Samsung, Apple, Dell...)
CREATE TABLE marcas (
  -- Identificador único da marca (chave primária)
  -- AUTO_INCREMENT: gerado automaticamente a cada novo registro
  marca_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  -- Nome da marca (ex: "Samsung")
  -- UNIQUE: não permite duas marcas com o mesmo nome
  nome VARCHAR(100) NOT NULL UNIQUE,
  -- Site oficial da marca (opcional, por isso é NULL)
  -- VARCHAR(255): tamanho comum para armazenar URLs
  site VARCHAR(255) NULL,
  -- Indica se a marca está ativa (visível/disponível no sistema)
  -- DEFAULT TRUE: toda marca nova é criada como ativa por padrão
  ativo BOOLEAN NOT NULL DEFAULT TRUE
-- InnoDB: mecanismo de armazenamento com suporte a chaves estrangeiras
-- e transações (importante, já que "produtos" provavelmente vai
-- referenciar marca_id como FK)
) ENGINE=InnoDB;



-- Cria a tabela "fornecedores", que armazena as empresas que
-- fornecem/vendem produtos para a loja
CREATE TABLE fornecedores (
  -- Identificador único do fornecedor (chave primária)
  fornecedor_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  -- Razão social: nome oficial/jurídico da empresa (registrado na Receita)
  -- Ex: "Tech Distribuidora de Eletrônicos LTDA"
  razao_social VARCHAR(150) NOT NULL,
  -- Nome fantasia: nome comercial, mais curto e conhecido no dia a dia
  -- Ex: "TechDist"
  nome_fantasia VARCHAR(120) NOT NULL,
  -- CNPJ do fornecedor (Cadastro Nacional da Pessoa Jurídica)
  -- CHAR(14): tamanho fixo, pois o CNPJ sempre tem 14 dígitos
  -- (armazenado apenas com números, sem pontos/barra/traço)
  -- UNIQUE: não permite dois fornecedores com o mesmo CNPJ
  cnpj CHAR(14) NOT NULL UNIQUE,
  -- E-mail de contato do fornecedor (obrigatório)
  email VARCHAR(150) NOT NULL,
  -- Telefone de contato (opcional, por isso NULL)
  telefone VARCHAR(20) NULL,
  -- Prazo médio de entrega/reposição, em dias
  -- SMALLINT UNSIGNED: número inteiro pequeno e positivo (suficiente aqui)
  -- DEFAULT 7: se não for informado, assume 7 dias
  -- CHECK: garante que o valor esteja sempre entre 1 e 180 dias,
  -- evitando dados inconsistentes (ex: 0 dias ou 9999 dias)
  prazo_medio_dias SMALLINT UNSIGNED NOT NULL DEFAULT 7
    CHECK (prazo_medio_dias BETWEEN 1 AND 180),
  -- Indica se o fornecedor está ativo (disponível para novas compras)
  ativo BOOLEAN NOT NULL DEFAULT TRUE
) ENGINE=InnoDB;

-- Cria a tabela "centros_distribuicao", que armazena os locais físicos
-- (armazéns/depósitos) de onde os produtos são estocados e distribuídos
CREATE TABLE centros_distribuicao (
  -- Identificador único do centro de distribuição (chave primária)
  centro_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  -- Nome do centro de distribuição (ex: "CD São Paulo", "CD Sul")
  -- UNIQUE: não permite dois centros com o mesmo nome
  nome VARCHAR(120) NOT NULL UNIQUE,
  -- Cidade onde o centro está localizado
  cidade VARCHAR(100) NOT NULL,
  -- UF (unidade federativa/estado) onde o centro está localizado
  -- CHAR(2): tamanho fixo, pois a sigla de estado sempre tem 2 letras (ex: "SP", "RJ")
  uf CHAR(2) NOT NULL,
  -- Indica se o centro de distribuição está ativo (em operação)
  ativo BOOLEAN NOT NULL DEFAULT TRUE
) ENGINE=InnoDB;

-- Cria a tabela "produtos", tabela central do sistema, relacionando
-- categoria, marca e fornecedor de cada item vendido
CREATE TABLE produtos (
  -- Identificador único interno do produto (chave primária)
  produto_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  -- SKU (Stock Keeping Unit): código único de controle do produto,
  -- geralmente usado internamente/no estoque (ex: "NB-DELL-I5-001")
  sku VARCHAR(30) NOT NULL UNIQUE,
  -- Nome comercial do produto, exibido ao cliente
  nome VARCHAR(160) NOT NULL,
  -- Slug: versão do nome amigável para URL (ex: "notebook-dell-i5-8gb")
  slug VARCHAR(180) NOT NULL UNIQUE,

  -- Chaves estrangeiras (relacionamentos obrigatórios) ------------------

  -- Categoria à qual o produto pertence (obrigatório: NOT NULL)
  categoria_id INT UNSIGNED NOT NULL,
  -- Marca/fabricante do produto (obrigatório)
  marca_id INT UNSIGNED NOT NULL,
  -- Fornecedor de onde o produto é adquirido (obrigatório)
  fornecedor_id INT UNSIGNED NOT NULL,

  -- Valores monetários -----------------------------------------------

  -- Preço de custo (quanto a loja pagou pelo produto)
  -- DECIMAL(10,2): até 10 dígitos no total, 2 casas decimais (ideal para dinheiro,
  -- evita erros de arredondamento que ocorreriam com FLOAT/DOUBLE)
  -- UNSIGNED: não permite valores negativos
  preco_custo DECIMAL(10,2) UNSIGNED NOT NULL,
  -- Preço de venda (quanto o cliente paga)
  preco_venda DECIMAL(10,2) UNSIGNED NOT NULL,
  -- Peso do produto em quilogramas (usado para cálculo de frete)
  -- DECIMAL(8,3): permite até 3 casas decimais (ex: 1.250 kg)
  -- DEFAULT 0: assume peso zero se não informado
  peso_kg DECIMAL(8,3) UNSIGNED NOT NULL DEFAULT 0,
  -- Garantia do produto, em meses (DEFAULT 3 meses)
  garantia_meses SMALLINT UNSIGNED NOT NULL DEFAULT 3,
  -- Indica se o produto está ativo (disponível para venda/exibição)
  ativo BOOLEAN NOT NULL DEFAULT TRUE,
  -- Data/hora de criação do registro, preenchida automaticamente
  -- pelo próprio MySQL no momento do INSERT
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  -- Restrições de integridade referencial (chaves estrangeiras) -------

  -- Relaciona o produto à categoria; impede excluir uma categoria
  -- que ainda tenha produtos vinculados (ON DELETE RESTRICT)
  CONSTRAINT fk_produtos_categoria FOREIGN KEY (categoria_id)
    REFERENCES categorias (categoria_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  -- Relaciona o produto à marca; mesma lógica de proteção contra exclusão
  CONSTRAINT fk_produtos_marca FOREIGN KEY (marca_id)
    REFERENCES marcas (marca_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  -- Relaciona o produto ao fornecedor; mesma lógica de proteção
  CONSTRAINT fk_produtos_fornecedor FOREIGN KEY (fornecedor_id)
    REFERENCES fornecedores (fornecedor_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  -- Regra de negócio: preço de venda deve ser sempre maior que zero,
  -- e o preço de custo nunca pode ser negativo
  CONSTRAINT chk_produtos_precos CHECK (preco_venda > 0 AND preco_custo >= 0),

  -- Índices para otimizar buscas e filtros mais comuns ----------------

  -- Acelera buscas/pesquisas por nome do produto (ex: barra de busca)
  INDEX idx_produtos_nome (nome),
  -- Índice composto: otimiza consultas que filtram produtos ativos
  -- de uma determinada categoria ao mesmo tempo
  -- (ex: "listar produtos ativos da categoria X")
  INDEX idx_produtos_categoria_ativo (categoria_id, ativo),
  -- Acelera buscas/filtros por marca
  INDEX idx_produtos_marca (marca_id)
) ENGINE=InnoDB;

-- Cria a tabela "estoques", que controla a quantidade de cada produto
-- disponível em cada centro de distribuição (tabela associativa
-- entre "produtos" e "centros_distribuicao", com dados adicionais)
CREATE TABLE estoques (
  -- Identificador único do registro de estoque (chave primária própria,
  -- em vez de usar chave composta produto_id + centro_id diretamente)
  estoque_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  -- Produto ao qual esse registro de estoque se refere
  produto_id INT UNSIGNED NOT NULL,
  -- Centro de distribuição onde esse estoque está localizado
  centro_id INT UNSIGNED NOT NULL,
  -- Quantidade total do produto disponível nesse centro
  -- DEFAULT 0: novo registro de estoque começa zerado
  quantidade INT UNSIGNED NOT NULL DEFAULT 0,
  -- Quantidade já reservada (ex: em pedidos ainda não finalizados/enviados)
  -- Serve para não vender/comprometer duas vezes o mesmo item
  reservado INT UNSIGNED NOT NULL DEFAULT 0,
  -- Ponto de reposição: quantidade mínima que, ao ser atingida,
  -- indica que é hora de repor o estoque desse produto nesse centro
  ponto_reposicao INT UNSIGNED NOT NULL DEFAULT 10,
  -- Data/hora da última atualização deste registro
  -- DEFAULT CURRENT_TIMESTAMP: preenchido automaticamente na criação
  -- ON UPDATE CURRENT_TIMESTAMP: atualizado automaticamente sempre que
  -- a linha for modificada (ex: quando a quantidade mudar)
  atualizado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  -- Garante que só exista UM registro de estoque por combinação
  -- de produto + centro (evita duplicidade, ex: dois registros de
  -- estoque do mesmo produto no mesmo centro)
  CONSTRAINT uq_estoques_produto_centro UNIQUE (produto_id, centro_id),
  -- Relaciona o estoque ao produto
  -- ON DELETE CASCADE: se o produto for excluído, os registros de
  -- estoque relacionados a ele são excluídos automaticamente
  CONSTRAINT fk_estoques_produto FOREIGN KEY (produto_id)
    REFERENCES produtos (produto_id)
    ON UPDATE CASCADE ON DELETE CASCADE,
  -- Relaciona o estoque ao centro de distribuição
  -- ON DELETE RESTRICT: impede excluir um centro de distribuição
  -- que ainda possua estoque registrado (protege contra perda de dados)
  CONSTRAINT fk_estoques_centro FOREIGN KEY (centro_id)
    REFERENCES centros_distribuicao (centro_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  -- Regra de negócio: a quantidade reservada nunca pode ser maior
  -- que a quantidade total em estoque (evita reservar mais do que existe)
  CONSTRAINT chk_estoques_reserva CHECK (reservado <= quantidade),
  -- Índice composto para acelerar consultas que cruzam quantidade
  -- e ponto de reposição — útil para relatórios/alertas do tipo
  -- "produtos que precisam de reposição" (quantidade <= ponto_reposicao)
  INDEX idx_estoques_nivel (quantidade, ponto_reposicao)
) ENGINE=InnoDB;

-- Cria a tabela "clientes", que armazena os dados cadastrais
-- das pessoas que compram na loja
CREATE TABLE clientes (

  -- Identificador único do cliente (chave primária)
  cliente_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,

  -- Nome completo do cliente
  nome_completo VARCHAR(150) NOT NULL,

  -- E-mail do cliente
  -- UNIQUE: não permite dois cadastros com o mesmo e-mail
  -- (geralmente também usado como login no sistema)
  email VARCHAR(150) NOT NULL UNIQUE,
  -- CPF do cliente (documento de identificação pessoal)
  -- CHAR(11): tamanho fixo, pois o CPF sempre tem 11 dígitos
  -- (armazenado apenas com números, sem pontos/traço)
  -- UNIQUE: impede duplicidade de cadastro para a mesma pessoa
  cpf CHAR(11) NOT NULL UNIQUE,
  -- Telefone de contato (opcional)
  telefone VARCHAR(20) NULL,
  -- Data de nascimento (opcional)
  -- Pode ser usada, por ex., para validar maioridade ou promoções
  data_nascimento DATE NULL,
  -- Data/hora de criação do cadastro, preenchida automaticamente
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  -- Indica se o cliente está ativo (cadastro válido/habilitado)
  ativo BOOLEAN NOT NULL DEFAULT TRUE,
  -- Índice para acelerar buscas/filtros por nome
  -- (ex: pesquisa de cliente no painel administrativo)
  INDEX idx_clientes_nome (nome_completo),
  -- Índice para acelerar consultas que filtram/ordenam por data de cadastro
  -- (ex: "novos clientes no último mês", relatórios de crescimento)
  INDEX idx_clientes_criado_em (criado_em)
) ENGINE=InnoDB;

CREATE TABLE enderecos (
  endereco_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  cliente_id INT UNSIGNED NOT NULL,
  tipo VARCHAR(20) NOT NULL DEFAULT 'ENTREGA',
  logradouro VARCHAR(160) NOT NULL,
  numero VARCHAR(20) NOT NULL,
  complemento VARCHAR(80) NULL,
  bairro VARCHAR(100) NOT NULL,
  cidade VARCHAR(100) NOT NULL,
  uf CHAR(2) NOT NULL,
  cep CHAR(8) NOT NULL,
  principal BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY (endereco_id),
  CONSTRAINT fk_enderecos_cliente FOREIGN KEY (cliente_id)
    REFERENCES clientes (cliente_id) ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT chk_enderecos_tipo CHECK (tipo IN ('ENTREGA', 'COBRANCA')),
  INDEX idx_enderecos_cliente (cliente_id),
  INDEX idx_enderecos_cep (cep)
) ENGINE=InnoDB;

CREATE TABLE cupons (
  cupom_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  codigo VARCHAR(30) NOT NULL,
  tipo_desconto VARCHAR(20) NOT NULL,
  valor_desconto DECIMAL(10,2) UNSIGNED NOT NULL,
  valor_minimo DECIMAL(10,2) UNSIGNED NOT NULL DEFAULT 0,
  inicio_em DATETIME NOT NULL,
  fim_em DATETIME NOT NULL,
  limite_usos INT UNSIGNED NOT NULL,
  usos_realizados INT UNSIGNED NOT NULL DEFAULT 0,
  ativo BOOLEAN NOT NULL DEFAULT TRUE,
  PRIMARY KEY (cupom_id),
  CONSTRAINT uq_cupons_codigo UNIQUE (codigo),
  CONSTRAINT chk_cupons_tipo CHECK (tipo_desconto IN ('PERCENTUAL', 'VALOR_FIXO')),
  CONSTRAINT chk_cupons_datas CHECK (fim_em > inicio_em),
  CONSTRAINT chk_cupons_usos CHECK (usos_realizados <= limite_usos),
  CONSTRAINT chk_cupons_percentual CHECK (
    tipo_desconto <> 'PERCENTUAL' OR valor_desconto BETWEEN 0 AND 100
  )
) ENGINE=InnoDB;

-- Cria a tabela "pedidos", que representa cada compra/pedido
-- realizado por um cliente
CREATE TABLE pedidos (
  -- Identificador único do pedido (chave primária)
  pedido_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  -- Cliente que realizou o pedido
  cliente_id INT UNSIGNED NOT NULL,
  -- Endereço de entrega escolhido para este pedido
  -- (referencia uma tabela "enderecos", que armazena os endereços
  -- cadastrados pelo cliente)
  endereco_entrega_id INT UNSIGNED NOT NULL,
  -- Status atual do pedido, controlando o fluxo/ciclo de vida dele
  -- DEFAULT 'PENDENTE_PAGAMENTO': todo pedido novo começa nesse status
  -- CHECK ... IN (...): restringe os valores possíveis a uma lista fixa,
  -- funcionando como um "ENUM" mais flexível/legível
  status VARCHAR(30) NOT NULL DEFAULT 'PENDENTE_PAGAMENTO' CHECK (status IN (
    'PENDENTE_PAGAMENTO',   -- aguardando confirmação do pagamento
    'PAGAMENTO_APROVADO',   -- pagamento confirmado
    'EM_SEPARACAO',         -- pedido sendo preparado/embalado no CD
    'ENVIADO',              -- pedido despachado para entrega
    'ENTREGUE',             -- pedido entregue ao cliente
    'CANCELADO'             -- pedido cancelado (por cliente ou loja)
  )),
  -- Valores financeiros do pedido -------------------------------------
  -- Subtotal: soma dos itens do pedido, antes de descontos/frete
  -- DECIMAL(12,2): mais dígitos que em "produtos", pois aqui é a soma
  -- de vários itens (pode chegar a valores bem maiores)
  subtotal DECIMAL(12,2) UNSIGNED NOT NULL DEFAULT 0,
  -- Valor de desconto aplicado ao pedido (cupom, promoção, etc.)
  valor_desconto DECIMAL(12,2) UNSIGNED NOT NULL DEFAULT 0,
  -- Valor do frete cobrado
  valor_frete DECIMAL(10,2) UNSIGNED NOT NULL DEFAULT 0,
  -- Valor total final do pedido (subtotal - desconto + frete)
  valor_total DECIMAL(12,2) UNSIGNED NOT NULL DEFAULT 0,
  -- Datas de criação e última atualização do pedido
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  atualizado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  -- Relaciona o pedido ao cliente
  -- ON DELETE RESTRICT: impede excluir um cliente que já tenha pedidos
  -- (preserva o histórico de vendas)
  CONSTRAINT fk_pedidos_cliente FOREIGN KEY (cliente_id)
    REFERENCES clientes (cliente_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  -- Relaciona o pedido ao endereço de entrega usado
  -- ON DELETE RESTRICT: impede excluir um endereço já usado em pedidos
  CONSTRAINT fk_pedidos_endereco FOREIGN KEY (endereco_entrega_id)
    REFERENCES enderecos (endereco_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  -- Regra de negócio: garante que o valor_total sempre seja calculado
  -- corretamente a partir dos outros campos:
  -- total = (subtotal - desconto, nunca menor que 0) + frete
  -- GREATEST(..., 0): evita total negativo caso o desconto seja maior
  -- que o subtotal
  -- ROUND(..., 2): arredonda para 2 casas decimais, evitando erro de
  -- comparação por causa de arredondamento
  CONSTRAINT chk_pedidos_total CHECK (
    valor_total = ROUND(GREATEST(subtotal - valor_desconto, 0) + valor_frete, 2)
  ),
  -- Índice composto: otimiza consultas do tipo "pedidos de um cliente
  -- ordenados/filtrados por data" (ex: histórico de compras do cliente)
  INDEX idx_pedidos_cliente_data (cliente_id, criado_em),
  -- Índice composto: otimiza consultas do tipo "pedidos com status X
  -- filtrados por data" (ex: painel administrativo, relatórios)
  INDEX idx_pedidos_status_data (status, criado_em)
) ENGINE=InnoDB;




-- Cria a tabela "pedidos_cupons", que registra qual cupom de desconto
-- foi aplicado em cada pedido
CREATE TABLE pedidos_cupons (
  -- Pedido ao qual o cupom foi aplicado
  -- Aqui, pedido_id é a PRÓPRIA chave primária da tabela (não um id
  -- próprio auto-incrementado) — isso implica um relacionamento
  -- "1 para 1": cada pedido pode ter, no máximo, UM cupom aplicado
  pedido_id INT UNSIGNED NOT NULL PRIMARY KEY,
  -- Cupom de desconto utilizado nesse pedido
  cupom_id INT UNSIGNED NOT NULL,
  -- Valor efetivamente aplicado/descontado por esse cupom no pedido
  -- (armazenado separadamente, pois o valor do cupom pode mudar
  -- no futuro, mas o histórico do pedido deve manter o valor
  -- que foi realmente concedido naquele momento)
  valor_aplicado DECIMAL(10,2) UNSIGNED NOT NULL,
  -- Relaciona o registro ao pedido
  -- ON DELETE CASCADE: se o pedido for excluído, o vínculo com o
  -- cupom também é excluído automaticamente (não faz sentido manter
  -- órfão, já que essa tabela só existe "em função" do pedido)
  CONSTRAINT fk_pedidos_cupons_pedido FOREIGN KEY (pedido_id)
    REFERENCES pedidos (pedido_id)
    ON UPDATE CASCADE ON DELETE CASCADE,
  -- Relaciona o registro ao cupom utilizado
  -- ON DELETE RESTRICT: impede excluir um cupom que já tenha sido
  -- usado em algum pedido (preserva o histórico/auditoria de uso)
  CONSTRAINT fk_pedidos_cupons_cupom FOREIGN KEY (cupom_id)
    REFERENCES cupons (cupom_id)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- Cria a tabela "itens_pedido", que armazena cada produto individual
-- dentro de um pedido (relacionamento N:N entre pedidos e produtos,
-- com dados adicionais como quantidade, preço e desconto)
CREATE TABLE itens_pedido (
  -- Identificador único do item (chave primária própria)
  item_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  -- Pedido ao qual esse item pertence
  pedido_id INT UNSIGNED NOT NULL,
  -- Produto correspondente a esse item
  produto_id INT UNSIGNED NOT NULL,
  -- Centro de distribuição de onde esse item específico será
  -- separado/enviado (permite que itens de um mesmo pedido saiam
  -- de centros diferentes, se necessário)
  centro_id INT UNSIGNED NOT NULL,
  -- Quantidade comprada desse produto nesse pedido
  quantidade INT UNSIGNED NOT NULL,
  -- Preço unitário do produto NO MOMENTO da compra
  -- (guardado aqui e não buscado de "produtos", pois o preço do
  -- produto pode mudar depois, mas o pedido deve manter o preço
  -- histórico praticado na venda)
  preco_unitario DECIMAL(10,2) UNSIGNED NOT NULL,
  -- Percentual de desconto aplicado a este item específico (0 a 100%)
  -- DECIMAL(5,2): permite valores como "100.00" (3 dígitos antes + 2 depois)
  -- CHECK: garante que o percentual esteja sempre entre 0 e 100
  percentual_desconto DECIMAL(5,2) UNSIGNED NOT NULL DEFAULT 0
    CHECK (percentual_desconto BETWEEN 0 AND 100),
  -- Subtotal do item (quantidade x preço unitário, já com desconto aplicado)
  subtotal DECIMAL(12,2) UNSIGNED NOT NULL,
  -- Garante que não existam dois itens repetidos para o mesmo produto
  -- vindo do mesmo centro dentro do mesmo pedido (evita duplicidade;
  -- se o cliente comprar 2 unidades, isso deve ser refletido no campo
  -- "quantidade", não em duas linhas separadas)
  CONSTRAINT uq_itens_pedido_produto_centro UNIQUE (pedido_id, produto_id, centro_id),
  -- Relaciona o item ao pedido
  -- ON DELETE CASCADE: se o pedido for excluído, seus itens também são
  -- (não faz sentido manter itens "órfãos" sem o pedido "pai")
  CONSTRAINT fk_itens_pedido_pedido FOREIGN KEY (pedido_id)
    REFERENCES pedidos (pedido_id)
    ON UPDATE CASCADE ON DELETE CASCADE,
  -- Relaciona o item ao produto
  -- ON DELETE RESTRICT: impede excluir um produto que já tenha sido
  -- vendido em algum pedido (preserva o histórico de vendas)
  CONSTRAINT fk_itens_pedido_produto FOREIGN KEY (produto_id)
    REFERENCES produtos (produto_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  -- Relaciona o item ao centro de distribuição de origem
  -- ON DELETE RESTRICT: impede excluir um centro que já tenha itens
  -- de pedidos vinculados a ele
  CONSTRAINT fk_itens_pedido_centro FOREIGN KEY (centro_id)
    REFERENCES centros_distribuicao (centro_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  -- Regra de negócio: quantidade deve ser sempre maior que zero
  -- (não faz sentido um item de pedido com quantidade 0)
  CONSTRAINT chk_itens_quantidade CHECK (quantidade > 0),
  -- Regra de negócio: garante que o subtotal esteja sempre coerente
  -- com quantidade, preço unitário e desconto aplicado
  -- Fórmula: subtotal = quantidade x preço x (1 - desconto%)
  -- ROUND(..., 2): evita divergência por arredondamento de casas decimais
  CONSTRAINT chk_itens_subtotal CHECK (
    subtotal = ROUND(quantidade * preco_unitario * (1 - percentual_desconto / 100), 2)
  ),
  -- Índice para acelerar buscas/relatórios por produto
  -- (ex: "quantas vezes esse produto foi vendido")
  INDEX idx_itens_produto (produto_id),
  -- Índice para acelerar a busca de todos os itens de um pedido
  -- (consulta muito comum: montar a "nota" de um pedido específico)
  INDEX idx_itens_pedido (pedido_id)
) ENGINE=InnoDB;

-- Cria a tabela "pagamentos", que registra as transações de pagamento
-- realizadas para cada pedido (um pedido pode ter mais de um pagamento,
-- ex: tentativa recusada + nova tentativa aprovada)
CREATE TABLE pagamentos (
  -- Identificador único do pagamento (chave primária)
  pagamento_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  -- Pedido ao qual esse pagamento se refere
  pedido_id INT UNSIGNED NOT NULL,
  -- Método de pagamento utilizado
  -- CHECK ... IN (...): restringe os valores a uma lista fixa,
  -- funcionando como um "ENUM" mais legível/portável
  metodo VARCHAR(30) NOT NULL CHECK (metodo IN (
    'PIX',
    'CARTAO_CREDITO',
    'CARTAO_DEBITO',
    'BOLETO'
  )),
  -- Número de parcelas do pagamento
  -- DEFAULT 1: a maioria dos métodos (PIX, débito, boleto) é à vista
  -- CHECK: limita entre 1 e 24 parcelas (evita valores absurdos/errados)
  parcelas SMALLINT UNSIGNED NOT NULL DEFAULT 1 CHECK (parcelas BETWEEN 1 AND 24),
  -- Valor total pago nessa transação
  valor DECIMAL(12,2) UNSIGNED NOT NULL,
  -- Status atual do pagamento
  -- DEFAULT 'PENDENTE': toda tentativa de pagamento começa pendente
  status VARCHAR(20) NOT NULL DEFAULT 'PENDENTE' CHECK (status IN (
    'PENDENTE',    -- aguardando confirmação da operadora/gateway
    'APROVADO',    -- pagamento confirmado
    'RECUSADO',    -- pagamento negado (ex: cartão sem limite)
    'ESTORNADO'    -- pagamento devolvido/cancelado após aprovação
  )),
  -- Código/identificador único da transação, geralmente retornado
  -- pelo gateway de pagamento (ex: Stripe, PagSeguro, Mercado Pago)
  -- Útil para conciliação financeira e para evitar processar a
  -- mesma transação duas vezes
  codigo_transacao VARCHAR(80) NOT NULL,
  -- Data/hora em que o pagamento foi efetivamente processado
  -- (aprovado, recusado ou estornado)
  -- NULL enquanto o pagamento ainda está PENDENTE
  processado_em DATETIME NULL,
  -- Garante que não existam dois pagamentos com o mesmo código de
  -- transação (evita duplicidade/processamento repetido)
  CONSTRAINT uq_pagamentos_transacao UNIQUE (codigo_transacao),
  -- Relaciona o pagamento ao pedido
  -- ON DELETE RESTRICT: impede excluir um pedido que já tenha
  -- pagamentos registrados (preserva histórico financeiro)
  CONSTRAINT fk_pagamentos_pedido FOREIGN KEY (pedido_id)
    REFERENCES pedidos (pedido_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  -- Índice composto: otimiza consultas do tipo "pagamentos de um
  -- pedido filtrados por status" (ex: verificar se algum pagamento
  -- do pedido já foi aprovado)
  INDEX idx_pagamentos_pedido_status (pedido_id, status)
) ENGINE=InnoDB;

-- Cria a tabela "entregas", que controla o transporte/logística
-- de cada pedido até o cliente
CREATE TABLE entregas (
  -- Identificador único da entrega (chave primária)
  entrega_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  -- Pedido ao qual essa entrega se refere
  -- UNIQUE: garante relação 1:1 (cada pedido tem, no máximo,
  -- UMA entrega associada — não há reenvio parcial nesse modelo)
  pedido_id INT UNSIGNED NOT NULL UNIQUE,
  -- Nome da transportadora responsável pelo envio (ex: "Correios", "Jadlog")
  transportadora VARCHAR(100) NOT NULL,
  -- Código de rastreio fornecido pela transportadora
  -- UNIQUE: não permite dois registros com o mesmo código de rastreio
  codigo_rastreio VARCHAR(60) NOT NULL UNIQUE,
  -- Status atual da entrega, controlando o fluxo logístico
  -- CHECK ... IN (...): restringe os valores a uma lista fixa
  status VARCHAR(30) NOT NULL CHECK (status IN (
    'AGUARDANDO_COLETA',  -- pedido pronto, aguardando a transportadora coletar
    'EM_TRANSITO',        -- pacote a caminho, ainda no trajeto
    'SAIU_PARA_ENTREGA',  -- saiu para entrega final ao cliente
    'ENTREGUE',           -- entrega concluída
    'EXTRAVIADO'          -- pacote perdido/extraviado no percurso
  )),
  -- Data prevista para a entrega (estimativa, sem hora definida)
  previsao_entrega DATE NOT NULL,
  -- Data/hora em que o pedido foi de fato enviado (despachado)
  -- NULL enquanto ainda está "AGUARDANDO_COLETA"
  enviado_em DATETIME NULL,
  -- Data/hora em que o pedido foi efetivamente entregue ao cliente
  -- NULL até que o status chegue a "ENTREGUE"
  entregue_em DATETIME NULL,
  -- Relaciona a entrega ao pedido
  -- ON DELETE RESTRICT: impede excluir um pedido que já tenha uma
  -- entrega registrada (preserva o histórico logístico)
  CONSTRAINT fk_entregas_pedido FOREIGN KEY (pedido_id)
    REFERENCES pedidos (pedido_id)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- Cria a tabela "avaliacoes", que armazena as avaliações/reviews que
-- os clientes fazem sobre os produtos comprados
CREATE TABLE avaliacoes (

  -- Identificador único da avaliação
  avaliacao_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  -- Cliente que fez a avaliação
  cliente_id INT UNSIGNED NOT NULL,
  -- Produto avaliado
  produto_id INT UNSIGNED NOT NULL,
  -- Pedido que "comprova" a compra do produto avaliado
  -- (geralmente usado para exibir o selo "compra verificada")
  pedido_id INT UNSIGNED NOT NULL,
  -- Nota dada ao produto (ex: de 1 a 5 estrelas)
  -- TINYINT UNSIGNED: número inteiro pequeno e positivo, suficiente
  -- para esse tipo de valor (economiza espaço comparado a INT)
  nota TINYINT UNSIGNED NOT NULL,
  -- Título curto da avaliação (ex: "Ótimo custo-benefício")
  titulo VARCHAR(120) NOT NULL,
  -- Texto completo do comentário/avaliação
  -- TEXT: usado por não ter um limite curto e fixo de caracteres,
  -- diferente de VARCHAR
  comentario TEXT NOT NULL,
  -- Data/hora de criação da avaliação, preenchida automaticamente
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  -- Indica se a avaliação foi aprovada para exibição pública
  -- DEFAULT FALSE: toda avaliação nova precisa de moderação antes
  -- de aparecer no site (evita spam, ofensas, etc.)
  aprovado BOOLEAN NOT NULL DEFAULT FALSE,
  -- Garante que um mesmo cliente não avalie o mesmo produto mais
  -- de uma vez (evita avaliações duplicadas/repetidas)
  CONSTRAINT uq_avaliacoes_cliente_produto UNIQUE (cliente_id, produto_id),
  -- Relaciona a avaliação ao cliente
  -- ON DELETE CASCADE: se o cliente for excluído, suas avaliações
  -- também são removidas automaticamente
  CONSTRAINT fk_avaliacoes_cliente FOREIGN KEY (cliente_id)
    REFERENCES clientes (cliente_id)
    ON UPDATE CASCADE ON DELETE CASCADE,
  -- Relaciona a avaliação ao produto
  -- ON DELETE CASCADE: se o produto for excluído, as avaliações
  -- dele também são removidas
  CONSTRAINT fk_avaliacoes_produto FOREIGN KEY (produto_id)
    REFERENCES produtos (produto_id)
    ON UPDATE CASCADE ON DELETE CASCADE,
  -- Relaciona a avaliação ao pedido que comprova a compra
  -- ON DELETE RESTRICT: impede excluir um pedido que já tenha
  -- gerado uma avaliação (preserva a rastreabilidade da "compra verificada")
  CONSTRAINT fk_avaliacoes_pedido FOREIGN KEY (pedido_id)
    REFERENCES pedidos (pedido_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  -- Regra de negócio: a nota deve estar sempre entre 1 e 5
  CONSTRAINT chk_avaliacoes_nota CHECK (nota BETWEEN 1 AND 5),
  -- Índice composto: otimiza a consulta mais comum da página de produto
  -- ("buscar avaliações aprovadas de um produto específico")
  INDEX idx_avaliacoes_produto_aprovado (produto_id, aprovado)
) ENGINE=InnoDB;

-- Cria a tabela "movimentacoes_estoque", que funciona como um LOG/histórico
-- de todas as entradas e saídas de estoque de cada produto
-- (essencial para auditoria e para reconstruir o saldo de estoque ao longo do tempo)
CREATE TABLE movimentacoes_estoque (

  -- Identificador único da movimentação
  -- BIGINT UNSIGNED (em vez de INT): usado aqui porque essa tabela tende
  -- a crescer MUITO mais rápido que as outras (toda entrada/saída de
  -- estoque gera uma linha nova), então o limite maior do BIGINT evita
  -- estourar o AUTO_INCREMENT no longo prazo
  movimentacao_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,

  -- Produto que teve estoque movimentado
  produto_id INT UNSIGNED NOT NULL,

  -- Centro de distribuição onde a movimentação ocorreu
  centro_id INT UNSIGNED NOT NULL,

  -- Tipo da movimentação (ex: "ENTRADA_COMPRA", "SAIDA_VENDA",
  -- "AJUSTE_INVENTARIO", "DEVOLUCAO", etc.)
  -- Aqui está como VARCHAR livre, sem CHECK restringindo valores
  -- (diferente de "status" em outras tabelas)
  tipo VARCHAR(30) NOT NULL,

  -- Quantidade movimentada
  -- IMPORTANTE: aqui é INT (COM sinal), não UNSIGNED como nas outras
  -- tabelas — isso é proposital, pois permite valores negativos
  -- para representar SAÍDAS de estoque (ex: -5) e positivos para
  -- ENTRADAS (ex: +10), facilitando somar tudo para obter o saldo
  quantidade INT NOT NULL,

  -- Referência externa opcional, ligando essa movimentação a outro
  -- registro do sistema (ex: número do pedido, código da nota fiscal
  -- de compra, id de um ajuste manual)
  -- É um campo "livre" (não é uma FK de verdade), então não garante
  -- integridade referencial automática
  referencia VARCHAR(80) NULL,

  -- Data/hora em que a movimentação ocorreu, preenchida automaticamente
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  -- Relaciona a movimentação ao produto
  -- ON DELETE RESTRICT: impede excluir um produto que já tenha
  -- histórico de movimentações (preserva a auditoria/rastreabilidade)
  CONSTRAINT fk_movimentacoes_produto FOREIGN KEY (produto_id)
    REFERENCES produtos (produto_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,

  -- Relaciona a movimentação ao centro de distribuição
  -- ON DELETE RESTRICT: mesma lógica, protege o histórico
  CONSTRAINT fk_movimentacoes_centro FOREIGN KEY (centro_id)
    REFERENCES centros_distribuicao (centro_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,

  -- Regra de negócio: a quantidade nunca pode ser zero
  -- (uma movimentação sem efeito nenhum não faz sentido existir)
  CONSTRAINT chk_movimentacoes_quantidade CHECK (quantidade <> 0),

  -- Índice composto: otimiza consultas do tipo "histórico de
  -- movimentações de um produto, ordenado por data"
  -- (ex: extrato de estoque de um item específico)
  INDEX idx_movimentacoes_produto_data (produto_id, criado_em),

  -- Índice composto: otimiza consultas do tipo "movimentações de
  -- um centro de distribuição, ordenadas por data"
  -- (ex: relatório operacional de um CD específico)
  INDEX idx_movimentacoes_centro_data (centro_id, criado_em)

) ENGINE=InnoDB;

-- Cria a tabela "historico_status_pedido", que funciona como um LOG
-- registrando cada mudança de status pela qual um pedido passou
-- (ex: PENDENTE_PAGAMENTO -> PAGAMENTO_APROVADO -> ENVIADO -> ENTREGUE)
CREATE TABLE historico_status_pedido (

  -- Identificador único do registro de histórico
  -- BIGINT UNSIGNED: assim como em "movimentacoes_estoque", essa tabela
  -- tende a crescer rapidamente (cada mudança de status de cada pedido
  -- gera uma linha), então o limite maior do BIGINT evita estourar o
  -- AUTO_INCREMENT no longo prazo
  historico_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,

  -- Pedido ao qual esse registro de histórico pertence
  pedido_id INT UNSIGNED NOT NULL,

  -- Status em que o pedido estava ANTES da mudança
  -- NULL: usado para representar a criação do pedido, quando ainda
  -- não havia um "status anterior" (primeira linha do histórico)
  status_anterior VARCHAR(30) NULL,

  -- Status para o qual o pedido mudou
  -- NOT NULL: toda mudança de status precisa ter um novo status definido
  status_novo VARCHAR(30) NOT NULL,

  -- Observação/comentário livre sobre a mudança
  -- (ex: "Pagamento aprovado via PIX", "Cliente solicitou cancelamento")
  observacao VARCHAR(255) NULL,

  -- Data/hora em que a mudança de status ocorreu, preenchida automaticamente
  alterado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  -- Define historico_id como chave primária
  PRIMARY KEY (historico_id),

  -- Relaciona o histórico ao pedido
  -- ON DELETE CASCADE: se o pedido for excluído, todo o histórico
  -- de status dele também é removido automaticamente
  CONSTRAINT fk_historico_pedido FOREIGN KEY (pedido_id)
    REFERENCES pedidos (pedido_id)
    ON UPDATE CASCADE ON DELETE CASCADE,

  -- Índice composto: otimiza a consulta mais comum dessa tabela —
  -- "buscar todo o histórico de um pedido, ordenado por data"
  -- (ex: exibir a linha do tempo do pedido para o cliente/atendimento)
  INDEX idx_historico_pedido_data (pedido_id, alterado_em)

) ENGINE=InnoDB;

-- Cria a tabela "auditoria_precos", que registra o HISTÓRICO de
-- alterações de preço dos produtos (quem mudou, de quanto para quanto,
-- e quando) — importante para rastreabilidade e prestação de contas
CREATE TABLE auditoria_precos (

  -- Identificador único do registro de auditoria
  -- BIGINT UNSIGNED: mesmo padrão das outras tabelas de log
  -- (movimentacoes_estoque, historico_status_pedido), pois tende a
  -- crescer bastante ao longo do tempo
  auditoria_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT  PRIMARY KEY ,

  -- Produto que teve o preço alterado
  produto_id INT UNSIGNED NOT NULL,

  -- Preço praticado ANTES da alteração
  -- Observação: sem UNSIGNED aqui (diferente de produtos.preco_custo/venda)
  preco_anterior DECIMAL(10,2) NOT NULL,

  -- Preço definido DEPOIS da alteração
  preco_novo DECIMAL(10,2) NOT NULL,

  -- Identificação de quem (ou o quê) fez a alteração
  -- VARCHAR livre: pode ser um nome de usuário, e-mail, ID de sistema
  -- externo, ou algo como "sistema_automatico" (ex: reajuste em lote)
  alterado_por VARCHAR(128) NOT NULL,

  -- Data/hora em que a alteração ocorreu, preenchida automaticamente
  alterado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

 

  -- Relaciona o registro de auditoria ao produto
  -- ON DELETE RESTRICT: impede excluir um produto que já tenha
  -- histórico de alteração de preço (preserva a auditoria)
  CONSTRAINT fk_auditoria_produto FOREIGN KEY (produto_id)
    REFERENCES produtos (produto_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,

  -- Índice composto: otimiza a consulta mais comum dessa tabela —
  -- "histórico de preços de um produto, ordenado por data"
  -- (ex: gráfico de variação de preço de um item ao longo do tempo)
  INDEX idx_auditoria_produto_data (produto_id, alterado_em)

) ENGINE=InnoDB;

-- Cria a tabela "alertas_estoque", que registra ocorrências de produtos
-- que atingiram (ou ficaram abaixo d)o ponto de reposição em um centro
-- de distribuição — usada para disparar reposição/compra
CREATE TABLE alertas_estoque (

  -- Identificador único do alerta
  -- BIGINT UNSIGNED: segue o mesmo padrão das outras tabelas de
  -- log/evento (movimentacoes_estoque, historico_status_pedido, etc.)
  alerta_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,

  -- Produto que gerou o alerta
  produto_id INT UNSIGNED NOT NULL,

  -- Centro de distribuição onde o estoque baixo foi detectado
  centro_id INT UNSIGNED NOT NULL,

  -- Quantidade em estoque NO MOMENTO em que o alerta foi gerado
  -- (um "retrato"/snapshot do valor, independente do que "estoques"
  -- tiver depois — importante para saber a situação exata que
  -- disparou o alerta)
  quantidade_atual INT UNSIGNED NOT NULL,

  -- Ponto de reposição vigente no momento do alerta
  -- (também um snapshot, já que esse valor em "estoques" pode
  -- ser alterado depois)
  ponto_reposicao INT UNSIGNED NOT NULL,

  -- Indica se o alerta já foi resolvido (ex: estoque reabastecido)
  -- DEFAULT FALSE: todo alerta nasce como pendente/aberto
  resolvido BOOLEAN NOT NULL DEFAULT FALSE,

  -- Data/hora em que o alerta foi gerado, preenchida automaticamente
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  -- Data/hora em que o alerta foi marcado como resolvido
  -- NULL enquanto o alerta ainda estiver em aberto
  resolvido_em DATETIME NULL,

  -- Relaciona o alerta ao produto
  -- ON DELETE CASCADE: se o produto for excluído, os alertas
  -- relacionados a ele também são removidos (não faz sentido manter
  -- alerta de um produto que não existe mais)
  CONSTRAINT fk_alertas_produto FOREIGN KEY (produto_id)
    REFERENCES produtos (produto_id)
    ON UPDATE CASCADE ON DELETE CASCADE,

  -- Relaciona o alerta ao centro de distribuição
  -- ON DELETE CASCADE: mesma lógica — sem centro, o alerta perde sentido
  CONSTRAINT fk_alertas_centro FOREIGN KEY (centro_id)
    REFERENCES centros_distribuicao (centro_id)
    ON UPDATE CASCADE ON DELETE CASCADE,

  -- Índice composto: otimiza a consulta mais importante dessa tabela —
  -- "listar alertas ainda não resolvidos, ordenados por data de criação"
  -- (ex: painel/fila de reposição de estoque para o time de compras)
  INDEX idx_alertas_abertos (resolvido, criado_em)

) ENGINE=InnoDB;