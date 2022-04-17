from urllib.parse import urlencode
from urllib.request import Request
import urllib.request
from bs4 import BeautifulSoup

url_busca = 'https://www2.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm'
url_resultado = 'https://www2.correios.com.br/sistemas/buscacep/ResultadoBuscaFaixaCEP.cfm?'


def retorna_ufs():
    ufs_encontradas = []
    pagina_de_busca = urllib.request.urlopen(url_busca)
    soup = get_beatiful_soup(pagina_de_busca)
    ufs = soup.find('select', attrs={'class': 'f1col'}).text.strip()

    for uf in ufs.split():
        ufs_encontradas.append(uf)

    return ufs_encontradas


def retorna_soup_html(form_fields):
    request = Request(url_resultado, urlencode(form_fields).encode())
    result = urllib.request.urlopen(request)
    soup = get_beatiful_soup(result)

    return soup


def get_beatiful_soup(pagina_de_busca):
    soup = BeautifulSoup(pagina_de_busca, 'html.parser')

    return soup
