def mensagem():
    print('Olá mundo!')
    print('Olá mundo!')
    print('Olá mundo!')
    print('Olá mundo!')



mensagem()
print('----------')
mensagem()

def nome(nome,idade):
    print(nome)
    print(idade)

nome('Diego',35)
nome('Maria',66)


def soma():
    num1 = 5
    num2 = 60
    soma = num1 + num2
    print(soma)

soma()


def somar(n1,n2):
    soma = n1 + n2
    print(soma)

somar(10,6)

           
def calculo(n1,n2,n3=30):
    cal = n1 + n2 + n3
    print(cal)

calculo(10,6)

def funcao_retorno(num1, num2):
    cal = num1 + num2
    return cal

resultado = funcao_retorno(20,30)

print(resultado)
print(resultado * 2)