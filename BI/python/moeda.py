import locale
#brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

#estados unidos 
# locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

#reino unido
# locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')

#frança
# locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

#alemanha
# locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

#italia
# locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')

#portugal
# locale.setlocale(locale.LC_ALL, 'pt_PT.UTF-8')

#japão
# locale.setlocale(locale.LC_ALL, 'ja_JP.UTF-8')

#china
# locale.setlocale(locale.LC_ALL, 'zh-CN.UTF-8')

valor = 10000.20

valor_formatado = locale.currency(valor,grouping=True)

print(valor)
print(valor_formatado)