 # break (quebrar) - interrompe completamente o loop, permitindo que o programa continue a execução após o loop

while True:
   nomes = input('Digite um nome ou digite (sair) para sair: ')
   if nomes == 'sair':
       print('sair')
       break 
  

num = 1
while num != 0:
    print('Olá mundo')
    num = int(input('Digite um valor '))


# continue (continuar) 
# continue pula para a proxima iteração do loop, ignorando o codigo restante da quela iteração

for i in range(5):
    if i == 3:
        continue # pula o numero 3
    print(i)

# pass (passar)
# pass não faz nada, permite que o codigo continue normalmente

# for i in range(5):
#     if i == 3:
#         pass # nada acontece quando o i = 3
#     else:{
#         print(f'valor {i}')
#     }
#     print(i)

# exit() (saida)
# termina todo o programa, encerrando a execução completamente 

for i in range(5):
    if i == 3:
        exit()
    print(i)
print('fim')
print('fim')
print('fim')
print('fim')
print('fim')
print('fim')
print('fim')