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