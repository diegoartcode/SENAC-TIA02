# set = conjunto
# set funciona como uma lista desordenada 
# não aceita valores duplicados
# dados não podem ser alterado para outro dado
# podemos incluir e excluir dados

frutas = {'Maça', 'Laranja', 'Abacaxi'}
print(frutas)
print(type(frutas))


frutas.add('Uva')
print(frutas)
frutas.remove('Maça')
print(frutas)