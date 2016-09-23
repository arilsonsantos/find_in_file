import os
import re
import util


class Buscador:

    def __init__(self, diretorio, palavra_chave, padrao, is_mostrar_linha, barra_diretorio):
        self.diretorio = diretorio
        self.barra_diretorio = barra_diretorio

        self.verificar_barras_do_diretorio_por_sistema_operacional()

        if self.diretorio[-1] != self.barra_diretorio:
            self.diretorio += self.barra_diretorio

        self.palavra_chave = palavra_chave
        self.padrao = padrao
        self.is_mostrar_linha = is_mostrar_linha
        self.encontrados = {}

    def pesquisar(self):
        for root, _, files in os.walk(self.diretorio):
            for file in files:

                if self.is_arquivo_do_padrao(file):
                    if self.is_fim_caminho_diretorio_sem_barra(root):
                        root += self.barra_diretorio

                    try:
                        arquivo = open(root + file, 'rt', encoding="utf8")

                        if self.is_mostrar_linha == 'false':
                            texto_arquivo = arquivo.read()
                            contador = self.get_ocorrencias_palavra_chave(
                                self.palavra_chave, texto_arquivo)

                            if contador > 0:
                                self.encontrados[root + file] = contador
                        else:
                            linhas = arquivo.readlines()

                            quantidade_ocorrencias_arquivo = 0
                            texto_linhas_encontradas = {}

                            for texto_linha in linhas:
                                contador = self.get_ocorrencias_palavra_chave(
                                    self.palavra_chave, texto_linha)

                                if contador > 0:
                                    quantidade_ocorrencias_arquivo += 1
                                    texto_linhas_encontradas[
                                        quantidade_ocorrencias_arquivo] = texto_linha
                            if quantidade_ocorrencias_arquivo > 0:
                                self.encontrados[
                                    root + file] = quantidade_ocorrencias_arquivo
                                util.logar_valor("arquivo", (root + file))

                                for numero_linha, texto_linha in texto_linhas_encontradas.items():
                                    util.logar_valor(
                                        "Ocorrencia " + str(numero_linha), texto_linha)
                                    print("")

                    except Exception as error:
                        util.logar_valor("erro", str(error))
                        util.logar_valor("Erro lendo o arquivo", root + file)
                        continue
                    finally:
                        arquivo.close()

    def get_ocorrencias_palavra_chave(self, palavra_chave, texto):
        return len(re.findall(palavra_chave, texto, re.IGNORECASE))

    def is_arquivo_do_padrao(self, arquivo):
        return re.match(r'.*?\.' + self.padrao + '$', arquivo) is not None

    def is_fim_caminho_diretorio_sem_barra(self, caminho):
        return (caminho[-1] != self.barra_diretorio)

    def get_resultados(self):
        return self.encontrados

    def verificar_barras_do_diretorio_por_sistema_operacional(self):
        if self.barra_diretorio == util.barra_linux:
            self.diretorio = self.diretorio.replace(
                util.barra_windows, util.barra_linux)
        else:
            self.diretorio = self.diretorio.replace(
                util.barra_linux, util.barra_windows)
