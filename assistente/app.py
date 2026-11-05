# API 

import re # trabalha com expressões regulares e identifica padrões em texto

import unicodedata # normaliza textos, permitindo remover acentos das palavras

import pandas as pd 

# utilizado para criar a aplicação web e a API
# jsonify dicionario python em respostas JSON
# render_template permite carregar paginas html
# request permite receber informações enviadas pelo usuario
from flask import Flask, jsonify, render_template, request 

# ele transforma textos em numeros para utilização em algoritmos de Machine Learning
from  sklearn.feature_extraction.text import TfidfVectorizer

# importa o algoritmo de regressão logistica
# neste projeto ele identifica a intenção de uma mensagem 
from sklearn.linear_model import LogisticRegression

# importa a função que calcula a similaridade de cosseno 
# ele identifica produtos semelhantes 
from sklearn.metrics.pairwise import cosine_similarity

# permite organizar etapas de processamento e treinamento em um unico modelo
from sklearn.pipeline import make_pipeline

# pip install flask

# cria uma instancia da apliacação Flask
# __name__ informa ao flask qual modulo esta executando 
app = Flask(__name__)


# 
produtos = pd.read_csv('dados/produtos.csv').set_index('id_produto')

interacoes = pd.read_csv('dados/interacoes.csv')

clientes = pd.read_csv('dados/clientes.csv').set_index('id_cliente')

pedidos = pd.read_csv('dados/pedidos.csv').set_index('id_pedido')

frases = pd.read_csv('dados/intencoes.csv')


# função para normalizar textos

# define uma função que recebe um texto como parametro

def normalizar(texto):
    # converte todas as letras para minusculas
    # depois, utiliza NFD para separar letras de acentos 
    # Exemplo: "Áudio" passa a ter "A" 
    texto = unicodedata.normalize("NFD", texto.lower())

    # percorre cada caractere do texto
    # unicodedata.category(c) identifica sua categoria
    # "Mn" representa marcas como acentos combinantes
    # os caracteres dessa categoria são ignorados
    # join reune os caracteres restantes em uma string
    return "".join(
        c for c in texto
        if unicodedata.category(c) != "Mn"
    )

# machine learning - identificação de intenções 

# cria um pipeline de machine learning
# o pipeline reune o processamento dos textos e o algoritimo utilizado para classificação
modelo = make_pipeline(
    # transforma frases em caracteristicas numericas 
    TfidfVectorizer(
        # aplica a função normalizar antes de analisar o texto, isso reduz diferenças entre palavras com e sem acentos 
        preprocessor=normalizar,
        # analisa sequancias de caracteres dentro de palavras
        # char_wb considera os limites das palavras
        analyzer="char_wb",
        # utiliza sequencia de 2 ate 5 caracteres 
        # exemplo: para 'mouse', podem surgir sequancias como 'mo', 'mou' e 'mous'
        ngram_range=(2,5)
    ),

    # Cria o classificador baseado em Regressão Logística. 

    LogisticRegression(
        # controla a intensidade da regularização
        # um C maior significa regularização mais fraca
        C=10,
        # define o maximo de 1000 iterações para o processo de otimização do modelo
        max_iter=1000
    )
) 


# treina o pipeline utilizando as frases do CSV

modelo.fit(frases['frase'],frases['intencao'])

# dicionario de sinonimos e categorias

# define categorias de produtos e palavras associadas
# o chatbot utiliza essas palavras para reconhecer categorias mencionadas nas mensagens
SINONIMOS = {
    "Periféricos": [
        "mouse",
        "teclado",
        "mousepad",
        "controle"
    ],

    "Áudio":[
        "headset",
        "fone",
        "microfone"
    ],
    "Armazenamento":[
        "ssd",
        "hd",
        "pen drive"
    ],
    "Acessórios":[
        "webcam",
        "suporte",
        "luminaria"
    ]
}

# função para entender a mensagem do usuario
def entender(texto):
    # proba é uma abreviação de probality (probabilidade)
    # predict_proba() é utilizado para calcular a probabilidade estimada de uma informação pertencer a cada uma das classes que o modelo aprendeu durante o treinamento.
    probs = modelo.predict_proba([texto])[0]

    # define qual intenção sera atribuida a mensagem 
    intencao = (
        # identifica a classe com a maior probabilidade
        # argmax() retorna a posição do maior valor
        # modelo.classes_ contem os nomes das intenções
        modelo.classes_[probs.argmax()]

        # so aceita a intenção quando sua probabilidade estimada é maior ou igual a 40%
        if probs.max() >= 0.40

        else "nao_entendi"
    )

    # normaliza a mensagem recebida
    t = normalizar(texto)

    # cria um dicionario vazio para armazenar informações identificadas na mensagem

    entidades = {}
    # procura um numero formado por exatamente 4 digitos consecutivos
    # \b identifica o limite de uma palavra
    # \d representa um digito de 0 ate 9
    # {4} indica exatamente quatro digitos
    # := permite atribuir e testar o resultado
    if m := re.search(r"\b(\d{4})\b", t):
        # captura o numero encontrado
        # group(1) recupera o primeiro grupo da expressão
        # int() converte o numero para inteiro
        entidades['pedido'] = int(m.group(1))

    # procura um valor maximo informado pelo cliente 
    # exemplo: 'mouse ate 150' ou 'ate R$ 200'.
    # \s* permite espaços opcionais
    # r? permite a letra 'r' opcional
    # \$? permite o simbolo de dinheiro opcional
    # (\d+) captura um ou mais digitos
    if m := re.search(r"ate\s*r?\$?\s*(\d+)", t):    
        entidades['preco_max'] = float(m.group(1))

    # percorre cada categoria e sua lista de palavras
    # items() permite acessar a chave e o valor
    # do dicionario simultaneamente
    for categoria, palavras in SINONIMOS.items():

        #  verifica se alguma palavra da categoria 
        # aparece dentro da mensagem
        # any() retorna True quando pelo menos uma condição é verdadeira
        # rf permite utilizar expressãoes regulares 
        # e inserir variaveis dentro da expressao
        # s? permite um 's' opcional no final

        if any(
            re.search(rf"\b{p}s?\b", t)
            for p in palavras
        ):
            
            entidades['categoria'] = categoria
    return intencao, entidades


# sistema de recomendação
pesos = {
    'visualizacao':1,
    'carrinho':3,
    'compra':5
}

# cria uma nova coluna chamada peso
# map() procura cada evento no dicionario pesos
# e atribui o valor correspondente
interacoes['peso'] = interacoes['evento'].map(pesos)

# matriz que relaciona cliente e produtos
# cada linha representa um cliente 
# cada coluna representa um produto
# cada celula contem a soma dos pesos das interações 
matriz = interacoes.pivot_table(
    # define os clientes como linha da matriz
    index="id_cliente",
    # define os produtos como colunas da matriz
    columns="id_produto",
    # utiliza os pesos como valores das celulas
    values="peso",
    # soma os pesos quando o mesmo cliente possui varias interações com um produto
    aggfunc ="sum",
    # preenche com zero os pares cliente-produto
    # que não possuem interações registradas
    fill_value=0
    # garante que todos os produtos cadastrados 
    # estejam representados nas colunas da matriz
    # produtos sem interações recebem valores zero
).reindex(columns=produtos.index, fill_value=0)

# calcala uma matriz de similaridade entre produtos
similaridade = pd.DataFrame(
    # transpõe a matriz cliente_produto
    # antes: linha = clientes, coluna = produtos
    # depois linha = produtos, coluna = clientes
    # values converte a tabela em uma matriz numerica
    # cosine_similarity calcula a semelhança entre os valores dos produtos
    cosine_similarity(matriz.T.values),

    index=produtos.index,
    columns=produtos.index
)

# calcula quantas compras cada produto recebeu
popularidade = (
    # seleciona apenas as interações do tipo "compra"
    interacoes[interacoes['evento'] == 'compra']['id_produto']
    # conta quantas vezes cada produto aparece
    .value_counts()
    # inclui todos os produtos cadastrados
    # produtos sem compras recebem contagem zero
    .reindex(produtos.index, fill_value=0)
)

# função para recomendar produtos

# id_cliente = identifica o cliente
# categoria = premite filtrar uma categoria especifica
# preco_max = define o preço maximo aceito
# n = quantidade de produtos retornados (padrão = 3)
def recomendar(id_cliente=None,categoria=None,preco_max=None, n = 3):
    # selecinar somente produtos com estaque maior que zero
    # copy cria uma copia dos produtos selecionados, isso evita alterações indesejadas do DataFrame original

    candidatos = produtos[produtos['estoque'] > 0].copy()
    # cria a coluna nota para prontuar cada produto
    # a popularidade é dividida pela maior popularidade
    # assim a pontuação é normalizada entre 0 e 1, quando existem compras registradas
    # o peso 0.2 limita a contribuição da popularidade 
    candidatos['nota'] = ( 0.2 * popularidade / popularidade.max() )

    # verifica se o cliente pode receber recomendações personaliadas com base no historico
    personalizado = (
        #  confirma que o cliente existe na matriz
        id_cliente in matriz.index

        # confirma que o cadastro permite personalização
        # segunda condição so é avaliada quando a primeira é verdadeira
        and clientes.loc[
            id_cliente, "aceita_personalizacao"
        ] == 'sim'
    )
    # executa a personalização somente quando autorizada
    if personalizado:
        # recupera o historico de interações do cliente
        # a linha contem os pesos de cada produto
        historico = matriz.loc[id_cliente]

        # calcula a afinidade do cliente com os produtos
        # similaridade contem a relação entre os produtos.
        # mul() multiplica as similaridades pelos pesos das interações do cliente
        # axis=0 indica alinhamento pelas linhas
        # sum() soma os resultados para cada produto
        # a divisão pelo total dos pesos gera uma media ponderada das similaridades
        afinidade = (
            similaridade.mul(historico, axis=0).sum() / historico.sum()
        )

        # adiciona a afinidade personalizada a nota 
        # reindex alinha as notas aos produtos candidatos
        candidatos['nota'] += afinidade.reindex(
            candidatos.index
        )

        # localiza os produtos ja comprados pelo cliente
        ja_comprou = interacoes[
            (interacoes['id_cliente'] == id_cliente)
            & (interacoes['evento'] == 'compra')
        ]['id_produto']

        # remove os produtos já comprados da lista
        # errors='ignore' evita erros caso algum produto comprado não esteja na lista de candidatos
        candidatos = candidatos.drop(
            index=ja_comprou,
            errors='ignore'
        )
    # verifica se foi informada uma categoria
    if categoria:
        # mantem somente produtos da categoria escolhida
        candidatos = candidatos[
            candidatos['categoria'] == categoria
        ]
    # verifica se foi informado um preço maximo
    if preco_max:
        # mantem somente produtos com preço menor ou igual ao valor definido pelo cliente 
        candidatos=candidatos[
            candidatos['preco'] <= preco_max
         ]
    # ordena os produtos pela nota, da maior para menor 
    # ascending=False define a ordem decrescente
    # head(n) seleciona os primeiros n produtos
    top = candidatos.sort_values(
        'nota',
        ascending=False
    ).head(n)

    return[
        {
            'id':int(i),
            'nome':r['nome'],
            'preco':float(r['preco'])
        }
        # iterrows() percorre as linha do DataFrame
        # i representa o indice do produto
        # r representa os dados da linha
        for i, r in top.iterrows()
    ]

RESPOSTAS = {
    'saudacao':(
        "Olá! Sou o assistente virtual da Lojatech"
        "Posso ajudar com pedidos, trocas e sugestões"
    ),
    'troca_devolucao':(
        "Você tem 7 dias para trocar (30 se tiver defeito)"
        "Quer que eu abra a solicitação?"
    ),
    'horario':(
        "Atendimento humano: seg. a sex., 9h às 18h;"
        "sáb., 9h às 13h."    
    ),
    'falar_humano':(
        "Certo! Vou transferir você para um atendente."
    ),
    'despedida':(
        "Obrigado pelo contato! Até logo."
    ),
    'nao_entendi':(
        "Não entendi! Posso ajudar com pedidos, trocas e sugestões de produtos."
    )
}

# rota da API 
# post  /api/chat


# cria uma rota que aceita requisições HTTP POST
# o endereço será http://127.0.0.1/5000/api/chat
@app.post("/api/chat")

# define a função executada quando uma requisição POST é enviada para a rota /api/chat
def chat():
    # silent=True evita lançar uma exceção caso o corpo 
    # JSON esteja ausente ou seja invalidado 
    # or {} utiliza um dicionario vazio nesses casos
    dados = request.get_json(silent=True) or {} 

    # recupera a propriedade 'mensagem' do json
    # get() retorna uma string vazia se ela não existir
    # str() converte o conteudo para texto
    # strip() remove espaços no começo e no final
    mensagem = str(
        dados.get('mensagem','')
    ).strip()

    # verifica se a mensagem esta vazia
    if not mensagem:
        # retorna uma mensagem de erro em JSON
        # o codigo HTTP 400 indica requisição invalida
        return jsonify({
            'erro':"Envie o campo 'mensagem'"           
        }),400
    
    # analisa a mensagem utilizando o modelo treinado
    # recebe a intenção e as entidades identificadas
    intencao, entidades = entender(mensagem)

    # cria o dicionario que sera utilizado como resposta
    # guarda a intenção identificada, as entidades extraidas e uma lista vazia de sugestões
    resposta = {
        'intencao':intencao,
        'entidades':entidades,
        'sugestoes':[]
    }
    # verifica se o usuario deseja consultar um pedido
    if intencao == "status_pedido":
        # recupera o numero do pedido encontrado na mensagem
        numero = entidades.get('pedido')
        # verifica se o numero existe na tabela de pedidos
        if numero in pedidos.index:
            # consulta o status do pedido pelo identificador.
            # loc localiza a linha correspondente ao pedido
            resposta['texto'] = (
                f"O pedido {numero} está: "
                f"{pedidos.loc[numero, 'status']}."
            )
        else:
            resposta['texto'] = (
                "Qual é o número do pedido? "
                "Ele está no e-mail de confirmação"
            )
    elif intencao == 'recomendar':
        resposta['sugestoes'] = recomendar(
            dados.get('id_cliente'),
            entidades.get('categoria'),
            entidades.get('preco_max')
        )
        resposta['texto'] = (
            'Separei estas sugestões para você:'

            if resposta['sugestoes']
            else 'Não encontrei produtos com esses filtros'
        )
    
    else:
        resposta['texto'] = RESPOSTAS[intencao]

    return jsonify(resposta)

# rota da api - recomendações por cliente 
# get /api/recomendacoes/<id_cliente>
# exemplo /api/recomendacoes/1
@app.get("/api/recomendacoes/<id_cliente>")

def recomendacoes(id_cliente):
    return jsonify({
        'cliente': id_cliente,
        'itens':recomendar(id_cliente,n=5)
    })

@app.get('/')

def pagina_inicial():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)