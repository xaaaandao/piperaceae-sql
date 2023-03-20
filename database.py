import os

import sqlalchemy
import sqlalchemy as sa
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import sqlalchemy.schema
from sqlalchemy import and_, or_

from tables import get_base, DataSP, create_datasp, create_county, create_identifier, DataTrustedIdentifier, \
    create_data_trusted_identifier
from unaccent import unaccent

cfg = {
    'host': '192.168.0.144',
    'user': os.environ['POSTGRE_USER'],
    'password': os.environ['POSTGRE_PASSWORD'],
    'port': '5432',
    'database': 'herbario'
}


def connect(echo=True):
    try:
        engine = sqlalchemy.create_engine(
            'postgresql+psycopg2://%s:%s@%s:%s/%s' % (
            cfg['user'], cfg['password'], cfg['host'], cfg['port'], cfg['database']), echo=echo,
            pool_pre_ping=True)
        Session = sqlalchemy.orm.sessionmaker(bind=engine)
        Session.configure(bind=engine)
        session = Session()
        if engine.connect():
            return engine, session
    except Exception as e:
        print('problems with host %s (%s)' % (cfg['host'], e))


def make_operation(session):
    try:
        session.commit()
        session.flush()
    except Exception as e:
        session.rollback()
        print(e)
        raise


# finally:
#     session.close()


def list_ilike(attribute, list_of_values):
    return [attribute.ilike(value) for value in list_of_values]


def create_table_if_not_exists(engine, table):
    table_name = table.__tablename__
    if not table_name in show_tables(engine):
        base = get_base()
        base.metadata.create_all(engine)
        print('create table: %s' % table.__tablename__)


def show_tables(engine):
    return sa.inspect(engine).get_table_names()


def table_is_empty(session, table):
    return session.query(table).count() == 0


def update_values_marked_by_george(df_george, session):
    for row in df_george.iterrows():
        if check_if_george_mark_true(row):
            seq = row[1]['seq']
            update_records_marked_by_george(seq, session)


def update_records_marked_by_george(seq, session):
    session.query(DataSP) \
        .filter(DataSP.seq == seq) \
        .update({'george': True}, synchronize_session=False)
    make_operation(session)


def check_if_george_mark_true(row):
    return row[1]['GEORGE'].lower() == 'sim'


def has_true_in_column_george(session):
    return session.query(DataSP).filter(DataSP.george).count() == 0


def insert_dataframe_in_database(dataframe, session):
    for row in dataframe.iterrows():
        session.add(create_datasp(row[1]))
        make_operation(session)


def insert_municipies_in_database(response, session):
    for i, county in enumerate(response.json()):
        session.add(create_county(county))
        make_operation(session)


def insert_new_identifier_trusted(identifier, query, searched_name, session):
    for q in query:
        new_record = create_identifier(identifier['full_name'], searched_name, q[0])
        session.add(new_record)
        make_operation(session)


def query_barcode(columns, list_values_founded, query_country, query_county, query_state_province, session):
    return session.query(*columns).filter(and_(
        or_(*list_values_founded),
        DataSP.specific_epithet.is_not(None),
        or_(or_(*query_country),
            or_(*query_state_province),
            or_(*query_county))
    )).distinct().all()


def find_and_replace_broken_characters(attribute, session, special_character):
    replace_func = sa.func.replace(attribute, special_character['find'], special_character['replace'])
    session.query(DataTrustedIdentifier) \
        .update(values={attribute: replace_func}, synchronize_session=False)
    make_operation(session)


def get_all_records_of_trusted_identifier(list_diff_identifier, session):
    return session.query(DataSP) \
        .filter(DataSP.identified_by.in_(list_diff_identifier))


def insert_new_data_trusted_identifier(session, query):
    for q in query:
        session.add(create_data_trusted_identifier(q))
        make_operation(session)


def get_all_identifiers_ilike(identifier, session):
    return


def get_all_records_with_diff_brasil(list_diff_br, session):
    return session.query(DataTrustedIdentifier) \
        .filter(DataTrustedIdentifier.country.in_(list_diff_br)) \
        .all()


def update_country_trusted_based_original_field(list_diff_br, session):
    session.query(DataTrustedIdentifier) \
        .filter(DataTrustedIdentifier.country.in_(list_diff_br)) \
        .update({'country_trusted': 'Brasil'}, synchronize_session=False)
    make_operation(session)


def has_brasil_in_country_trusted(session):
    return session.query(DataTrustedIdentifier) \
        .filter(DataTrustedIdentifier.country_trusted == 'Brasil') \
        .count() == 0


def get_all_records_with_brasil_in_country_trusted(session):
    return session.query(DataTrustedIdentifier) \
        .filter(DataTrustedIdentifier.country_trusted == 'Brasil') \
        .distinct() \
        .all()


def state_province_list_state(list_state):
    return unaccent(sa.func.lower(DataTrustedIdentifier.state_province)).in_(list_state)


def state_province_list_uf(list_uf):
    return unaccent(sa.func.lower(DataTrustedIdentifier.state_province)).in_(list_uf)


def state_province_in_list_uf_or_list_state(list_state, list_uf):
    return or_(state_province_list_uf(list_state),
               state_province_list_state(list_uf))


def county_in_list_county(list_county):
    return unaccent(sa.func.lower(DataTrustedIdentifier.county)).in_(list_county)


def update_country_trusted(list_county, list_state, list_uf, session):
    session.query(DataTrustedIdentifier) \
        .filter(and_(DataTrustedIdentifier.country_trusted.is_(None),
                     state_province_in_list_uf_or_list_state(list_state, list_uf),
                     county_in_list_county(list_county))) \
        .update({'country_trusted': 'Brasil'}, synchronize_session=False)
    make_operation(session)


def has_state_in_locality(list_state_like):
    return


def text_bold(string):
    return '\033[1m' + string + '\033[0m'


def execute_query(session, query):
    try:
        return session.execute(query).all()
    except:
        session.commit()
        session.flush()
