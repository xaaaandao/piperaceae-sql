import requests


def get_municipies():
    try:
        return requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/municipios")
    except Exception as e:
        raise print(f"error: {e}")


def get_key(json, key):
    if key in json:
        return json[key]
    raise KeyError('key %s not found' % key)


def get_id(json):
    if 'id' in json:
        return json['id']
    raise KeyError('key id not found')


def get_county_name(json):
    if 'nome' in json:
        return json['nome']
    raise KeyError('key nome not found')


def get_uf(json):
    if 'microrregiao' in json:
        if 'mesorregiao' in json['microrregiao']:
            if 'UF' in json['microrregiao']['mesorregiao']:
                return return_sigla_estado(json), return_nome_estado(json)
            raise KeyError('key UF not found')
        raise KeyError('key mesorregiao not found')
    raise KeyError('key microrregiao not found')


def return_nome_estado(json):
    return json['microrregiao']['mesorregiao']['UF'][
        'nome']


def return_sigla_estado(json):
    return json['microrregiao']['mesorregiao']['UF']['sigla']
