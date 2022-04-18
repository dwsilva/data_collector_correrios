import uuid
import controller
import http_in

ufs = http_in.retorna_ufs()

criar_arquivo = controller.verifica_cria_arquivo()

for uf in ufs:
    pagini = 1
    pagfim = 50
    numero_da_pagina = 1
    ceps_nao_duplicados = []
    requisicao_html = http_in.retorna_soup_html(controller.retorna_post_fields(uf, pagini, pagfim))
    total_paginas = controller.calcula_total_paginas(requisicao_html)
    print('-------> Coletando dados da UF: ', uf)

    while numero_da_pagina <= total_paginas:
        requisicao_html = http_in.retorna_soup_html(controller.retorna_post_fields(uf, pagini, pagfim))
        total_paginas = controller.calcula_total_paginas(requisicao_html)
        tabela_localidades = controller.escolhe_tabela_localidades(requisicao_html.find_all('table'))

        for linha in tabela_localidades.findAll("tr"):
            id = str(uuid.uuid4())
            celulas = linha.findAll('td')
            if len(celulas) > 0:
                cep = str(celulas[1].find(text=True)).strip()
                localidade = celulas[0].find(text=True)
                situacao = celulas[2].find(text=True)
                tipo_de_faixa = celulas[3].find(text=True)

                if cep in ceps_nao_duplicados:
                    print(f'A localidade {celulas[0].find(text=True)} já existe no dicionário para a UF {uf}')

                else:
                    ceps_nao_duplicados.append(cep)
                    registros = controller.registros(id, uf, localidade, cep, situacao, tipo_de_faixa)
                    escreve_em_arquivo = controller.escreve(registros, 'arquivo.jsonl')

        pagini += 50
        pagfim += 50
        numero_da_pagina += 1

    total_paginas += 1
    print(f'----------------------------------------------------\n')
