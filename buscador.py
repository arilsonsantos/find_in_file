import os
import re


class Buscador:

    def __init__(self, diretorio, palavraChave, padrao, is_mostrar_linha):
        self.diretorio = diretorio

        if self.diretorio[-1] != '/':
            self.diretorio += '/'

        self.diretorio = self.diretorio.replace('/', '\\')
        self.palavraChave = palavraChave
        self.padrao = padrao
        self.is_mostrar_linha = is_mostrar_linha
        self.encontrados = {}

    def pesquisar(self):
        for root, _, files in os.walk(self.diretorio):
            for file in files:

                if self.is_arquivo_do_padrao(file):
                    if root[-1] != '\\':
                        root += '\\'

                    try:
                        arquivoAberto = open(
                            root + file, 'rt', encoding="utf8")

                        if self.is_mostrar_linha != 'true':
                            textoArquivo = arquivoAberto.read()
                            contador = self.get_ocorrencias_palavra_chave(
                                self.palavraChave, textoArquivo)

                            if contador > 0:
                                self.encontrados[root + file] = contador

                        else:
                            linhas = arquivoAberto.readlines()

                            quantidadeOcorrenciasArquivo = 0
                            textoLinhasEncontradas = {}

                            for textoLinha in linhas:
                                contador = self.get_ocorrencias_palavra_chave(
                                    self.palavraChave, textoLinha)

                                if contador > 0:
                                    quantidadeOcorrenciasArquivo += 1
                                    textoLinhasEncontradas[quantidadeOcorrenciasArquivo] = textoLinha

                            if quantidadeOcorrenciasArquivo > 0:
                                self.encontrados[root + file] = quantidadeOcorrenciasArquivo
                                self.logar_valor("arquivo", (root + file))

                                for numeroLinha, textoLinha in textoLinhasEncontradas.items():
                                    self.logar_valor("Ocorrencia " + str(numeroLinha), textoLinha)
                                    print("")

                    except Exception as error:
                        self.logar_valor("erro", str(error))
                        self.logar_valor(
                            "Erro lendo o arquivo", root + file)
                        continue
                    finally:
                        arquivoAberto.close()

    def get_ocorrencias_palavra_chave(self, palavraChave, texto):
        return len(re.findall(palavraChave, texto, re.IGNORECASE))

    def is_arquivo_do_padrao(self, arquivo):
        return re.match(r'.*?\.' + self.padrao + '$', arquivo) is not None

    def logar_valor(self, nome, valor):
        print(nome.title() + ": [" + valor + "]")

    def getResultados(self):
        return self.encontrados
