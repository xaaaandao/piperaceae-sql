import os

import sqlalchemy
import sqlalchemy as sa
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import sqlalchemy.schema
from sqlalchemy import and_, or_

from tables import get_base, DataTrustedIdentifier
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
                cfg['user'], cfg['password'], cfg['host'], cfg['port'], cfg['database']), echo=echo, pool_pre_ping=True)
        session = sqlalchemy.orm.sessionmaker(bind=engine)
        session.configure(bind=engine)
        db = session()
        if engine.connect():
            return engine, db
    except Exception as e:
        print('problems with host %s (%s)' % (cfg['host'], e))


def create_table_if_not_exists(engine, table):
    table_name = table.__tablename__
    if table_name != show_tables(engine):
        base = get_base()
        base.metadata.create_all(engine)
        print('create table: %s' % table.__tablename__)


def show_tables(engine):
    return sa.inspect(engine).get_table_names()


def check_if_george_mark_true(row):
    return row[1]['GEORGE'].lower() == 'sim'


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


def text_bold(string):
    return '\033[1m' + string + '\033[0m'
