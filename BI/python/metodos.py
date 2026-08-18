texto = input('Digite um texto: ')

print(f'1 - Quantidade de caracteres: {len(texto)}')

print(f'2 - Texto em maiúsculo: {texto.upper()}')

print(f'3 - Texto em minúsculo: {texto.lower()}')

print(f'4 - Texto sem espaços: {texto.replace(' ', '')}')

print(f'5 - Tem somente letras? (temos que tirar os espaços para verificar):  {texto.replace(' ', '').isalpha()}')

print(f'6 - É alfanumérico? Tem letras e números (temos que tirar os espaços para verificar): {texto.replace(' ', '').isalnum()}')

print(f'7 - Quebra o texto a cada espaço em branco: {texto.split()}')

print(f'8 - Centralizar o texto em * ')
print(texto.center(20, "*"))