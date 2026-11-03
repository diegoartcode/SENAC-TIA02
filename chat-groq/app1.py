# intalar bibliotecas
# pip install dotenv 
# pip install groq

# python -m pip install groq==1.7.0

# permite acessar recursos do sistema operacional, criando e incluido variaveis de ambiente.
import os

# importa a classe Groq da biblioteca groq
from groq import Groq

# import a função load_dotenv da biblioteca python-dotenv
# essa função permite carregar variaveis armazanadas em um arquivo chamado .env
from dotenv import load_dotenv

# carragar as variaveis de ambimente
load_dotenv()

# recuperar a chave da API
# a função os.getenv procura o valor de uma variavel de ambiente pelo seu nome
# se a varialvel não existir, o resultado sera None.
api_key = os.getenv('GROQ_API_KEY')


# verificar se a chave existe
if not api_key:
    print('Chave GROQ_API_KEY não encontrada!')
    # raise é utilizado para provocar uma exceção

    # ValueError indica que existe um problema relacionado ao valor esperado

    # neste caso, interrompemos o programa porque não foi encontrada uma chave de api
    raise ValueError('Chave GROQ_API_KEY não encontrada!')


# criar o cliente Groq

client = Groq(api_key=api_key)


# criar a função de conversa com a ia


def chat_groq(prompt):
    # enviar uma requisição para a api
    # a variavel completion armazenara o resultado retornado pela API 
    # client representa o cliente criado anteriormente
    # chat representa os recursos de conversa
    # completions representa as respostas geradas
    # create() envia uma solicitação a api, infomando o modelo e as configurações da conversa
    completion = client.chat.completions.create(
        # definindo o modelo
        model="openai/gpt-oss-20b",
        # definir as mensagens da conversa
        messages=[
            {
                # a chave role identifica que esta enviando uma mensagem
                # "user" representa o usuario
                # "system" instruções para o modelo
                # "assistant" mensagens anteriores da IA
                "role":"user",
                # a chave content armazena o conteudo da mensagem enviada
                # para a ia
                # prompt contem o texto recebido como argumento da função
                "content":prompt
            }
        ],

        # configurar a temperatura
        # o parametro temperature controla o nivel de aleatoriedade na geração das respostas
        # valores menores tendem a produzir respostas mais previsiveis 
        # valores maiores tendem a preduzir resposta mais variadas

        # a temperatura não representa porcentagem de acerto ou inteligencia do modelo
        temperature=0.7,

        # definir o limite de tokens

        max_tokens=1024
        
    )

    # recuperar a resposta gerada 
    return completion.choices[0].message.content

# __name__ é uma variavel especial do python, criada automanticemente quando um modulo é executado ou importado 
# "__main__" é um nome especial ultilizado pelo python para identificar o modulo que esta sendo executado como program principal
# se este arquivo estiver sendo executado diretamente, execute o codigo abaixo
if __name__ == "__main__":
    while True:
        # pega o texto 
        user_input = input("Digite sua pergunta (ou 'sair' para encerrar): ")

        # verifica se o texto e igual a sair e finaliza o programa
        if user_input.lower().strip() == "sair":
            print("Chat encerrado!")
            break

        # verifica se o texto esta vazio e volta no inicio do while e retorna a preguntar    
        if not user_input.strip():
            continue
        
        # tentar consultar a IA
        try:
            response = chat_groq(user_input)

            print('Resposta do Groq')
            print(response)
        except Exception as erro:
            print(f'Erro: {erro}')
