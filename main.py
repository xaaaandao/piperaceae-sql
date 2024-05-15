import datetime
import logging

import pandas as pd

import api
# from county import insert_counties
from database import connect, create_table
from george import insert_data_george
from local import update_local
from models import get_base, County, State, GeorgeData, Exsiccata, exsiccata_identifier, Identifier, TrustedIdentifier, \
    TrustedIdentifierSelected
from species_link import insert_data_specieslink
from sql import insert

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


def create_county(json, state):
    return County(id=api.get_id(json), name=api.get_county_name(json), state_id=state.id)


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
            # print(data)

            state = create_state(data)
            insert(state, session)
            county = create_county(data, state)
            insert(county, session)

    count = session.query(County).count()
    logging.info('count of counties is %d' % count)


def insert_trusted_identifier(session):
    # if session.query(TrustedIdentifier).count() == 0:
    df = pd.read_csv('./csv/trusted_identifiers.csv', sep=';', index_col=False, header=0)
    df_selected = pd.read_csv('./csv/a.csv', sep=';', index_col=False, header=0)
    for idx, row in df.iterrows():
        t = TrustedIdentifier(fullname=row['fullname'], search=row['search'])
        insert(t, session)

        df_value_founded = df_selected.loc[df_selected['fullname'].__eq__(row['fullname'])]
        for idx, row in df_value_founded.iterrows():
            tis = TrustedIdentifierSelected(value_founded=row['value_founded'],
                                            selected=row['selected'],
                                            trusted_identifier_id=t.id)
            insert(tis, session)


# def insert_trusted_identifier_selected(session):
#     if session.query(TrustedIdentifierSelected).count() == 0:
#         df = pd.read_csv('./csv/a.csv', sep=';', index_col=False, header=0)
#         for idx, row in df.iterrows():
#             t = TrustedIdentifierSelected(fullname=row['fullname'], search=row['search'])
#             insert(t, session)

# if session.query(TrustedIdentifier).count()==0:


def main():
    engine, session = connect()
    base = get_base()

    create_table(base, engine)
    insert_counties(session)
    insert_data_specieslink(session)
    insert_data_george(session)
    insert_trusted_identifier(session)
    update_local(session)
    # update_local(session)

    engine.dispose()
    session.close()


if __name__ == '__main__':
    main()
