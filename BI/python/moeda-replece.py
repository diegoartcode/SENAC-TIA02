moeda = float(input('Digite um valor: '))

print(moeda)

print(f'{moeda:,.2f}')

moeda_formatada = f'{moeda:,.2f}'.replace('.','x').replace(',','.').replace('x',',')
print(moeda_formatada)