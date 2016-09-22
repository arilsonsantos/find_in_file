# -*- coding: UTF-8 -*-

import sys
from buscador import Buscador

def logarValor(nome, valor):
    print(nome.title() + ": [" + valor + "]")

if len(sys.argv) == 5:
    print("-" * 100)

    logarValor("diretorio", sys.argv[1])
    logarValor("palavra chave", sys.argv[2])
    logarValor("padrao", sys.argv[3])

    print("-" * 100)

    busca = Buscador(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

    busca.pesquisar()

    resultados = busca.getResultados()

    print('Encontrado ', len(resultados), ' files:')

    for arquivo, contador in resultados.items():
        print('Arquivo: ', arquivo, ' Ocorências:' , contador)
else:
    print("Usage:")
    print("py main.py [DIRECTORY] [KEYWORD] [PATTERN(JAVA, TXT, XML, PY, ...)] [SHOW_LINE(true | false)]")
    print("Example:")
    print("py main.py c:\\projet\\django\\ driver xml true")
