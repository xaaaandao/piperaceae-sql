import logging

from ibge import api
from models import County
from sql import is_query_empty


def create_county(json):
    uf, state, regiao = api.get_uf(json)
    return County(id=api.get_id(json), county=api.get_county_name(json), uf=uf, state=state, regiao=regiao)


def insert_counties(session):
    response = api.get_data_api()

    count = session.query(County).count()
    if is_query_empty(count):
        for i, county in enumerate(response.json()):
            record = create_county(county)
            try:
                session.add(record)
                session.commit()
            except Exception:
                session.rollback()

    count = session.query(County).count()
    logging.info('count of counties is %d' % count)
