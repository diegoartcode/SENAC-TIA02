for contador in range(0,10+1,1):
    print(contador)

print('------------')

contador = 0
while contador <= 10:
    print(contador)
    contador += 1



while True:
   nomes = input('Digite um nome ou digite (sair) para sair: ')
   if nomes == 'sair':
       print('sair')
       break 
   # break (quebrar) - interrompe completamente o loop, permitindo que o programa continue a execução após o loop

num = 1
while num != 0:
    print('Olá mundo')
    num = int(input('Digite um valor '))