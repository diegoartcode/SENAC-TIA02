opcao = int(input('Digite um numero de 1 a 3:'))

match opcao:
    case 1:
        print('Opção 1 selecionada ')
    case 2:
        print('Opção 2 selecionada ')
    case 3:
        print('Opção 3 selecionada ')
    case _:
        print('Opção inválida ')

dia = "quarta" 

match dia:
    case "segunda":
        print('Hoje é segunda-feira')
    case "terça":
        print('Hoje é terça-feira')
    case "quarta":
        print('Hoje é quarta-feira')
    case "quinta":
        print('Hoje é quinta-feira')
    case "sexta":
        print('Hoje é sexta-feira')
    case "sabado":
        print('Hoje é sabado')
    case "domingo":
        print('Hoje é domingo')
    case _:
        print('Dia inválido')

from datetime import datetime
pegarDataAtual = datetime.now()
print(pegarDataAtual)

print(f'Data atual: {pegarDataAtual.strftime('%d/%m/%y %H:%M:%S')}')
print(f'Data atual: {pegarDataAtual.strftime('%d/%m/%Y %H:%M:%S')}')
print(f'Dia da semana: {pegarDataAtual.strftime('%A')}')
print(f'Dia da semana (abreviado): {pegarDataAtual.strftime('%a')}')
print(f'Número do dia da semana: {pegarDataAtual.strftime('%w')}')
print(f'Número do dia do ano: {pegarDataAtual.strftime('%j')}')
print(f'Número do mês: {pegarDataAtual.strftime('%m')}')
print(f'Número do dia do mês: {pegarDataAtual.strftime('%d')}')



print('-------')

diaDaSemana = pegarDataAtual.strftime('%w')
print(diaDaSemana)

match diaDaSemana:
    case '1':
        print('Hoje é segunda-feira')
    case '2':
        print('Hoje é terça-feira')
    case '3':
        print('Hoje é quarta-feira')
    case '4':
        print('Hoje é quinta-feira')
    case '5':
        print('Hoje é sexta-feira')
    case '6':
        print('Hoje é sabado')
    case '0':
        print('Hoje é domingo')
    case _:
        print('Dia inválido')


import locale
from datetime import datetime

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

agora = datetime.now()
print(agora)

print(f'Data atual: {agora.strftime('%d/%m/%y %H:%M:%S')}')

print(f'Dia da semana: {agora.strftime('%A')}')
print(f'Dia da semana (abreviado): {agora.strftime('%a')}')

