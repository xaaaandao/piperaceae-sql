import requests


def get_municipies():
    try:
        return requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/municipios")
    except Exception as e:
        raise print(f"error: {e}")
