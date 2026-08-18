tenho_sede = True

if tenho_sede == True:
    print('Tenho sede!')

if tenho_sede:
    print('Tenho sede!')

print('fim')

num1 = 10 
num2 = 20

if num1 > num2:
    print('Tenho sede!')


if tenho_sede == True:
    print('Tenho sede!')
else:
    print('Não quero beber água!')

# nota maior ou igual a 90 #saida NOTA A
# nota maior ou igual a 80 #saida NOTA B
# nota maior ou igual a 70 #saida NOTA C
# nota menor que 70        #saida NOTA D
nota = 89

if nota >= 90:
    print("NOTA A")
elif nota >= 80:
    print("NOTA B")
elif nota>=70:
    print('NOTA C')
else:
    print("NOTA D")


#condicional aninhada

idade = 17
tem_cnh = True

if idade >= 18:
    if tem_cnh == True:
        print("Você pode dirigir!") 
    else:
        print("Você não pode dirigir!")
else:
    print('Voce é menor de idade!')