import os

import sqlalchemy
import sqlalchemy as sa
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import sqlalchemy.schema

from models import get_base, DataTrustedIdentifier
from unaccent import unaccent

cfg = {
    'host': '192.168.0.144',
    'user': os.environ['POSTGRE_USER'],
    'password': os.environ['POSTGRE_PASSWORD']
}


def connect(echo=True):
    try:
        url = 'postgresql+psycopg2://%s:%s@%s:5432/herbario' % (cfg['user'], cfg['password'], cfg['host'])
        engine = sa.create_engine(url, echo=echo, pool_pre_ping=True)
        session = sqlalchemy.orm.sessionmaker(bind=engine)
        session.configure(bind=engine)
        db = session()
        if engine.connect():
            return engine, db
    except Exception as e:
        print('problems with host %s (%s)' % (cfg['host'], e))


def table_exists(engine, table_name):
    return True if table_name in show_tables(engine) else False


def create_table(engine, table):
    table_name = table.__tablename__

    if not table_exists(engine, table_name):
        base = get_base()
        base.metadata.tables[table_name].create(bind=engine)
        print('create table: %s' % table.__tablename__)


def show_tables(engine):
    return sa.inspect(engine).get_table_names()


def update_country_trusted(session, query):
    uf_unaccented_lower, state_unaccented_lower, county_unaccented_lower = get_list_uf_state_county(query)
    condition = sa.and_(DataTrustedIdentifier.country_trusted.is_(None),
                        sa.or_(uf_unaccented_lower, state_unaccented_lower))
    session.query(DataTrustedIdentifier) \
        .filter(condition) \
        .update({'country_trusted': 'Brasil'}, synchronize_session=False)


def get_list_uf_state_county(query):
    list_uf = [unaccent(sa.func.lower(q.uf)) for q in query]
    list_state = [unaccent(sa.func.lower(q.state)) for q in query]
    list_county = [unaccent(sa.func.lower(q.county)) for q in query]

    uf_unaccented_lower = unaccent(sa.func.lower(DataTrustedIdentifier.state_province)).in_(list_uf)
    state_unaccented_lower = unaccent(sa.func.lower(DataTrustedIdentifier.state_province)).in_(list_state)
    county_unaccented_lower = unaccent(sa.func.lower(DataTrustedIdentifier.county)).in_(list_county)

    return uf_unaccented_lower, state_unaccented_lower, county_unaccented_lower


def get_columns_table(table):
    return table.__table__.columns
