meses = {
    1:'Janeiro',
    2:'Fevereiro',
    3:'Março',
    4:'Abril',
    5:'Maio',
    6:'Junho'
}
print(meses)
print(type(meses))
print(meses[4])

meses = {
    'Jan':'Janeiro',
    'Fev':'Fevereiro',
    'Mar':'Março',
    'Abr':'Abril',
    'Mai':'Maio',
    'Jun':'Junho'
}
print(meses['Abr'])
meses['Jun'] = 'JUNHO'
print(meses['Jun'])

frutas = {
    'fruta1':{
        'nome':'Maça',
        'preco':5.60
    },
    'fruta2':{
        'nome':'Banana',
        'preco':10.25
    },
}

print(frutas['fruta1']['nome'])
print(frutas['fruta1']['preco'])


chaves = ['nome','idade','curso']
valores = ['Jhenny','28','Python']


pessoa = dict(zip(chaves,valores))

print(pessoa)
print(type(pessoa))