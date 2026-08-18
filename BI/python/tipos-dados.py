# string 

nome = "Romeu"
outronome = 'Julieta'

print(nome)
print(outronome)

nome = 'João'
outronome = "Maria"

print(nome)
print(outronome)

print('----------------------------------------')
# string - input

moto = input('Digite o nome da moto: ')
print(moto)

print(type(moto))

print('----------------------------------------')
# float

salario = 15000.50
print(salario)
print(type(salario))

largura = float(input('Digite a largura: '))
comprimento = float(input('Digite o comprimento: '))
print(type(largura))


calculo = largura * comprimento
print(calculo)

print('----------------------------------------')
#int
idade = int(input('Digite sua idade: '))
ANO_ATUAL = 2026

ano_nascimento = ANO_ATUAL - idade

print(ano_nascimento)
print("Sua idade é ", idade, ", e estamos em ", ANO_ATUAL, " então o ano de seu é nascimento ", ano_nascimento, ".")


print(f'Sua idade é {idade}, e estamos em {ANO_ATUAL} então o ano de seu é nascimento {ano_nascimento}.')

print('----------------------------------------')

#bool
verdadeiro = True
falso = False
