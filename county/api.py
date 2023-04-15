import requests


def get_data_api():
    try:
        url = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'
        return requests.get(url)
    except Exception:
        raise requests.exceptions.RequestException('error in request')


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


def get_name_region(json):
    return json['microrregiao']['mesorregiao']['UF'][
        'regiao']['nome']


def get_uf(json):
    if 'microrregiao' in json:
        if 'mesorregiao' in json['microrregiao']:
            if 'UF' in json['microrregiao']['mesorregiao']:
                return get_acronym_state(json), get_name_state(json), get_name_region(json)
            raise KeyError('key UF not found')
        raise KeyError('key mesorregiao not found')
    raise KeyError('key microrregiao not found')


def get_name_state(json):
    return json['microrregiao']['mesorregiao']['UF']['nome']


def get_acronym_state(json):
    return json['microrregiao']['mesorregiao']['UF']['sigla']
