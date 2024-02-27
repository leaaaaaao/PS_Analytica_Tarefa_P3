import requests

url_ibge = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'
ordena_ibge = '?orderBy=nome'

BAD_REQUEST = 400
NOT_FOUND = 404
SERVICE_UNAVAILABLE = 503

# Retorna uma tupla, (idMunicipio, err), onde err é uma string que descreve
# o erro que ocorreu na execução, ou None, caso não haja nenhum
# TODO passar isso pro README
def getMunicipioId(nomeMunicipio):
    try:
        municipios = requests.get(url_ibge)
        municipios = municipios.json()
    except:
        return None, ('Erro ao acessar a API do IBGE', SERVICE_UNAVAILABLE)

    municipioEncontrado = None

    for municipio in municipios:
        if municipio['nome'] == nomeMunicipio:
            municipioEncontrado = municipio
            break
    if not municipioEncontrado:
        return None, ('Erro: Município não encontrado', NOT_FOUND)
    
    return municipioEncontrado['id'], None

# Retorna uma tupla (nomesBairros, err), onde err é uma string que descreve
# o erro que ocorreu na execução, ou None, caso não tenha ocorrido nenhum
# TODO passar isso pro README
def getBairros(municipioId):
    bairros = []
    nomesBairros = []
    try:
        bairros = requests.get(url_ibge + f"/{municipioId}/subdistritos{ordena_ibge}")
        bairros = bairros.json()
    except:
        return None, ('Erro ao acessar a API do IBGE', SERVICE_UNAVAILABLE)
    
    for bairro in bairros:
        nomesBairros.append(bairro['nome'])
    
    return nomesBairros, None