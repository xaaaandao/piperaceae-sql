import datetime
import logging

import sqlalchemy

import api
# from county import insert_counties
from database import connect, create_table
from george import insert_data_george
from models import get_base, Local, County, State
from species_link import insert_data_specieslink
from sql import insert, inserts

datefmt = '%d-%m-%Y+%H-%M-%S'
dateandtime = datetime.datetime.now().strftime(datefmt)
bold_red = "\x1b[31;1m"
green = "\x1b[32m"
reset = "\x1b[0m"
format = '%(asctime)s [%(module)s - L:%(lineno)d - %(levelname)s] %(message)s'
format_info = green + format + reset
format_error = bold_red + format + reset
logging.basicConfig(format=format_info, datefmt='[%d/%m/%Y %H:%M:%S]', level=logging.INFO)
logging.basicConfig(format=format_error, datefmt='[%d/%m/%Y %H:%M:%S]', level=logging.ERROR)


def update_local(session):
    br_variations = ['Brasil', 'BRASIL', 'Brasil/Bolivia', 'Brasilia', 'brazil', 'Brazil', 'BRazil', 'BRAZIL',
                     '[Brésil]', 'Brésil']

    pass


def create_county(json):
    return County(id=api.get_id(json), name=api.get_county_name(json))


def is_query_empty(query):
    return query == 0


def create_state(data):
    uf, state, regiao = api.get_uf(data)
    return State(uf=uf, name=state, region=regiao)


def insert_counties(session):
    response = api.get_data_api()

    count = session.query(County).count()
    if is_query_empty(count):
        for i, data in enumerate(response.json()):
            state = create_state(data)
            county = create_county(data)
            state.counties.append(county)
            insert(state, session)

    count = session.query(County).count()
    logging.info('count of counties is %d' % count)



def main():
    engine, session = connect()
    base = get_base()

    create_table(base, engine)
    # insert_counties(session)
    insert_data_specieslink(session)
    insert_data_george(session)
    # update_local(session)
    # update_local(session)

    engine.dispose()
    session.close()


if __name__ == '__main__':
    main()
