import json, math, os


def retorna_post_fields(uf, pag_inicial, pag_final):
    post_fields = {
        'UF': f'{uf}',
        'Localidade': '',
        'qtdrow': '50',
        'pagini': f'{pag_inicial}',
        'pagfim': f'{pag_final}'
    }
    return post_fields


def calcula_paginas(total_registros):
    return math.ceil(int(total_registros) / 50)


def encontra_texto_nova_consulta(lista_de_elementos):
    return lista_de_elementos.index('[ Nova Consulta ]')


def gera_lista_elementos(soup):
    i = 0
    lista_de_elementos = []
    for elemento in soup.find('body').findAll(text=True):
        elemento_string = str(elemento)
        lista_de_elementos.append(elemento_string)
        i += 1
    return lista_de_elementos


def calcula_total_paginas(soup):
    lista_de_elementos = gera_lista_elementos(soup)
    texto_nova_consulta = encontra_texto_nova_consulta(lista_de_elementos)
    posicao_texto_nova_consulta = lista_de_elementos[texto_nova_consulta + 2].split()
    total_paginas = calcula_paginas(posicao_texto_nova_consulta[4])
    return total_paginas


def verifica_cria_arquivo():
    if os.path.isfile('src/arquivo.jsonl'):
        os.remove('src/arquivo.jsonl')
    else:
        open('src/arquivo.jsonl', 'a')


def registros(id, uf, localidade, cep, situacao, tipo_de_faixa):
    return {
        'id': id,
        'uf': uf,
        'localidade': localidade,
        'faixa_de_cep': cep,
        'situacao': situacao,
        'tipo_de_faixa': tipo_de_faixa
    }


def escreve(registros, nome_arquivo):
    json_file = open(f'.\src\{nome_arquivo}', 'a', encoding='utf8')
    json.dump(registros, json_file, ensure_ascii=False)
    json_file.write('\n')
    json_file.close()


def escolhe_tabela_localidades(tabela_localidades):
    if len(tabela_localidades) == 2:
        tabela_localidades = tabela_localidades[1]
    elif len(tabela_localidades) == 1:
        tabela_localidades = tabela_localidades[0]

    return tabela_localidades
