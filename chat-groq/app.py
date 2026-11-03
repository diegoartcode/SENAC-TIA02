# python -m streamlit run app.py --server.fileWatcherType none

# biblioteca que calcula um identificador SHA-256 do arquivo para evitar indexação duplicada
import hashlib 
# permite converte dados python em json e imprementar respostas SJON da IA
import json 
# le configurações e segredos definidos nas variaveis de ambiente 
import os
# trabalha com expressões regulares usadas para bloquear padrões SQL inseguros
import re
# gerencia o SQLite local que armazena conversas e mensagens
import sqlite3
# cria identificadores unicos para cada conversa
import uuid
#  obtem a data e a hora atuais para registrar o historico
from datetime import datetime
# transforma bytes de arquivos em objetos que o pandas consegue ler 
from io import BytesIO
# manipula caminhos de arquivos de modo independete do sistema operacional
from pathlib import Path
# banco vetorial usado para salvar embeddings e recuperar trechos dos documentos
# embeddings é uma tecnica de inteligencia artificial que transforma dados do mundo real como palavras, frases, imagens ou audios em sequencia de numeros chamados vetores. Esses numeros capturam o significado (semantica) de conteudo em um mapa matematico, fazendo com que os itens parecidos fiquem proximos uns dos outros.
import chromadb
# organiza dados tabulares, importa planilhas e apresenta resultados de consultas
import pandas as pd
# extrai texto de arquivos PDF, pagina por pagina
import pymupdf
# cria a interface web interativa: botoes, campos, tabelas e chat
import streamlit as st
# carrega as variaveis de configurações do arquivo .env
from dotenv import load_dotenv
#  cliente da API Groq e classe de erro de limite de requisições/tokens 
from groq import Groq, RateLimitError
# carrega o modelo que transforma textos e perguntas em vetores numericos
from sentence_transformers import SentenceTransformer
# interpreta SQL como um arvore sintatica antes de permitir sua execução
import sqlglot
# disponibiliza os tipos de comandos SQL reconhecidos pelo sqlglot
from sqlglot import exp


# instalação das bibliotecas
# python -m pip install streamlit groq python-dotenv pandas pymupdf openpyxl chromadb sentence-transformers mysql-connector-python sqlglot

# carrega o .env
load_dotenv()

# pasta onde este script esta salvo, serve de base para os caminhos locais
ROOT = Path(__file__).resolve().parent
#  diretorio onde ficam o banco SQLite e o banco vetorial Chroma
DATA = ROOT/'dados_locais'
# cria a pasta de dados, caso ela ainda não exista
DATA.mkdir(exist_ok=True)
#  nome do modelo multiligue de embeddings empregado na busca semantica
MODEL_EMBED = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-V2'
#  modelo de linguagem 
MODEL_GROQ = os.getenv('GROQ_MODEL')
# arquivo que armazena as conversas e mensagens persistentes
DB_SQLITE = DATA / 'historico.sqlite3'
# limite para o total de fragmentos indexados no Chroma 
MAX_CHUNKS = 2000
# limites aproximados em caracteres para controlar o tamanho da requisições 
# limita o tamanho do esquema de tabelas enviado ao gerador de SQL
MAX_ESQUEMA_CHARS = 6000
# limita caracteres do contexto enviado na resposta da IA
MAX_CONTEXTO_CHARS = 6500
# constante reservada no codigo atual o corte do historico é feito por mensagem (600 caracteres)
MAX_HISTORICO_CHARS = 1200
# numero maximo do MySQL enviadas a ia; não limata o DataFrame da tela
MAX_LINHAS_IA = 20 # A tabela na interface continua com até 200 linhas

# configura titulo, icone e largura da pagina web do Streamlit
st.set_page_config(
    page_title='IA + RAG + MySQL',
    page_icon='🤖',
    layout='wide'
    )

# abre o SQlite e garante a existencia das tabelas de conversas e mensagens
def historico_db():
    # abre uma conexao com o arquivo SQLite local
    connection = sqlite3.connect(DB_SQLITE)
    # cria a tabela de identificação e data de criaçao de cada conversa
    connection.execute('''
                CREATE TABLE IF NOT EXISTS conversas(
                       id TEXT PRIMARY KEY,
                       titulo TEXT NOT NULL,
                       criado_em TEXT NOT NULL
                       )
''')
    connection.execute('''
                CREATE TABLE IF NOT EXISTS mensagens(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       conversa_id TEXT NOT NULL, 
                       papel TEXT NOT NULL,
                       conteudo TEXT NOT NULL,
                       criado_em TEXT NOT NULL,
                       FOREIGN KEY (conversa_id) REFERENCES conversas(id)
                       )    
''')
    # confirma as alterações de criação das tabelas no banco
    connection.commit()
    return connection


# cria um ID unico, insere uma conversa vazia e devolve o identificador
def nova_conversa():
    # gera um identificador aleatorio unico no padrao UUID
    cid = str(uuid.uuid4())
    # usa uma conexão SQLite em um bloco de contexto para confirmar transações
    with historico_db() as c:
        # registra uma nova conversa com titulo inicial e data/hora
        c.execute('INSERT INTO conversas VALUES (?,?,?)', (cid,'Nova conversa', datetime.now().isoformat(timespec='seconds')))
    return cid


#  lista as conversas existentes, mostrando primeiro as mais recentes
def listar_conversas():
    #  usa uma conexão SQLite em um bloco de contexto para confirmar transações 
    with historico_db() as c:
        #  executa um select no historico SQLite e retorna as linha
        return c.execute('SELECT id, titulo FROM conversas ORDER BY criado_em DESC').fetchall()

# recupera as mensagens de um a conversa em ordem cronologica
def mensagens_da_conversa(cid):
    # usa uma conexão SQLite em um bloco de contexto para confirmar transações 
    with historico_db() as c:
        # transforma cada linha do SQLite no formato role/context usado pelo chat
        return [{'role': p, 'content' : t } for p, t, in c.execute(
            'SELECT papel, conteudo FROM mensagens WHERE conversa_id = ? ORDER BY id', (cid,)
        ) ]
# salva uma mensagem e ajusta o titulo da conversa na primeira pergunta   
def guardar_mensagem(cid, papel, conteudo):
    with historico_db() as c:
        # salva papel (user/assistant), texto e data/hora da mensagem
        c.execute('''INSERT INTO mensagens
                   (conversa_id, papel, conteudo, criado_em) 
                  VALUES (?,?,?,?)''', 
                  (cid, papel, conteudo, datetime.now().isoformat(timespec='seconds')))
        # atualiza automaticamente o titulo somente quando a mensagem é do usuario
        if papel == 'user':
            # consulta o titulo atual da conversa
            atual = c.execute('SELECT titulo FROM conversas WHERE id=?'(cid)).fetchone()
            # não sobrescreve titulo que já foram definidos
            if atual and atual[0] == 'Nova conversa':
                # usa os 55 primeiros caracteres da primeira pergunta como titulo
                c.execute('UPDATE conversas SET titulo=? WHERE  id=?',
                          (conteudo[:55],cid))

# mantem recursos caros na memoria entre atualizações do Streamlit
@st.cache_resource
# carrega o modelo de embeddings uma vez e o reutiliza
def modelo_embedding():
    #  instancia o modelo multilingue definido na configuração
    return SentenceTransformer(MODEL_EMBED)

# mantem recursos caros na memoria entre atualizações do Streamlit
@st.cache_resource
# cria ou recupera o cliente persistente do ChomaDB
def chroma_cliente():
    # salva os vetores no disco para não perde-los ao encerrar o aplicativo
    return chromadb.PersistentClient(path=str(DATA / 'chroma'))

# retorna a coleção de documentos usada nas buscas por similaridade
def colecao():
    # embeddings são calculados por nosso modelo, não pela função-padrão Chroma
    # cria a coleção somente se ela ainda não existir, os vetores são calculados externamente 
    return chroma_cliente().get_or_create_collection(name="documentos",embedding_function=None)

def dividir_texto(texto, tamanho=950, sobreposicao=150):
    if not texto.strip():
        return [] 
   
    return [texto[i:i+tamanho].strip() for i in range(0, len(texto), tamanho-sobreposicao)]

def partes_arquivo(arquivo):
    # retem somente o nome, sem caminhos enviados pelo arquivo
    nome = Path(arquivo.name).name
    # obtem a extensao padronizada em letras minusculas
    ext = Path(nome).suffix.lower() 
    # le todo o conteudo do upload como bytes
    raw = arquivo.getvalue()
    # lista que acumula pares(origem do trecho, conteudo)
    partes = []
    # para PDF, extrai o texto separadamente de cada pagina
    if ext == '.pdf':
        # abre o PDF diretamente da memoria, sem salva-lo no disco
        with pymupdf.open(stream=raw,filetype='pdf') as pdf:
            # percorre paginas e inicia a numeração em 1
            for numero, pagina in enumerate(pdf, 1):
                # extrai o texto que esta presente na camada textual do pdf
                texto = pagina.get_text('text', sort=True)
                # ignora paginas sem texto extraivel
                if texto.strip():
                    partes.append((f'Página {numero}', texto))
    # para TXT, tenta primeiro a codificação UTF-8 e depois Windows-1252
    elif ext == '.txt':
        try:
            # decodifica UTF-8 
            texto = raw.decode('utf-8-sig')
        #  caso o arquivo não seja UTF-8
        except UnicodeDecodeError:
            # decodifica textos produzidos em algumas instalações windows
            texto = raw.decode('cp1252')
        partes.append(('Texto', texto))
    # para tabelas, converte grupos de linhas em texto que sera indexado
    elif ext in ('.csv','.xlsx'):
        #  trata arquivo CSV e planilhas Excel com leitores diferentes
        if ext == '.csv':
            # usado para descobrir se alguma tentativa de leitura foi bem-sucedida
            tabela = None
            # testa codificações comuns dos arquivos CSV
            for enc in ('utf-8-sig','cp1252'):
                try:
                    # pandas tenta identificar automaticamente o separedor do CSV
                    tabela = pd.read_csv(BytesIO(raw), sep = None, engine='python',encoding=enc)
                    break
                #  se a leitura falhar, tenta a proxima codificação
                except (UnicodeError, pd.errors.ParserError):
                    continue
            # rejeita CSVs que nunhuma tentativa conseguiu interpretar 
            if tabela is None:
                raise ValueError('CSV inválido ou ilegível')
            abas = {'CSV': tabela}

        else:
            # importa todas as abas do excel para um dicionario de DataFrame
            abas = pd.read_excel(BytesIO(raw), sheet_name=None,engine='openpyxl')
            # percorre cada aba e seu conjunto de linhas 
        for aba, df in abas.items():
            # divide tabelas em blocos de oito registros para indexação
            for inicio in range(0, len(df), 8):
                # evita ultrapassar o total de linhas na ultima parte
                fim = min(inicio + 8, len(df))
                partes.append((f'Aba {aba}, linhas {inicio+1}-{fim}',df.iloc[inicio:fim].to_csv(index=False)))
    else: 
        raise ValueError('Tipo de arquivo não permitido')
    return nome, raw, partes   
         
# gera trechos e embedding e persite o conteudo no banco vetorial
def indexar(arquivo):
    # extrai texto e metadados do arquivo enviado
    nome, raw, partes = partes_arquivo(arquivo)
    # calcula a impressão digital unica do conteudo do arquivo
    hash_arquivo = hashlib.sha256(raw).hexdigest()
    # obtem a coleção do Chroma onde o conteudo ficara armazanado
    conjunto = colecao()
    # evita reprocessar upload do mesmo conteudo
    # busca um arquivo com hash igual para não indexar novamente
    existente = conjunto.get(where={'arquivo_hash':hash_arquivo}, limit=1)
    

    