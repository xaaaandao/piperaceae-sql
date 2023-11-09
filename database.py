import os

import sqlalchemy
import sqlalchemy as sa
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import sqlalchemy.schema

from models import DataIdentifiersSelectedGeorge
from unaccent import unaccent


def connect(echo=True, host='localhost', user=os.environ['myuser_pg'], password=os.environ['mypwd_pg'], port='5432', database='herbario'):
    try:
        url = 'postgresql+psycopg2://%s:%s@%s:%s/%s' % (user, password, host, port, database)
        engine = sa.create_engine(url, echo=echo, pool_pre_ping=True)
        session = sqlalchemy.orm.sessionmaker(bind=engine)
        session.configure(bind=engine)
        if engine.connect():
            return engine, session()
    except Exception as e:
        print(e)





def update_country_trusted(session, query):
    uf_unaccented_lower, state_unaccented_lower, county_unaccented_lower = get_list_uf_state_county(query)
    condition = sa.and_(DataIdentifiersSelectedGeorge.country_trusted.is_(None),
                        sa.or_(uf_unaccented_lower, state_unaccented_lower))
    session.query(DataIdentifiersSelectedGeorge) \
        .filter(condition) \
        .update({'country_trusted': 'Brasil'}, synchronize_session=False)


def get_list_uf_state_county(query):
    list_uf = [unaccent(sa.func.lower(q.uf)) for q in query]
    list_state = [unaccent(sa.func.lower(q.state)) for q in query]
    list_county = [unaccent(sa.func.lower(q.county)) for q in query]

    uf_unaccented_lower = unaccent(sa.func.lower(DataIdentifiersSelectedGeorge.state_province)).in_(list_uf)
    state_unaccented_lower = unaccent(sa.func.lower(DataIdentifiersSelectedGeorge.state_province)).in_(list_state)
    county_unaccented_lower = unaccent(sa.func.lower(DataIdentifiersSelectedGeorge.county)).in_(list_county)

    return uf_unaccented_lower, state_unaccented_lower, county_unaccented_lower


def get_columns_table(table):
    return table.__table__.columns


def get_records_group_by_level(condition, level, minimum_image, session):
    columns = [level,
               sa.func.array_agg(DataIdentifiersSelectedGeorge.seq).label('list_seq')]
    query = session.query(*columns) \
        .filter(condition) \
        .distinct() \
        .group_by(level) \
        .order_by(level) \
        .having(sa.func.count(level) >= minimum_image) \
        .all()
    return query


def get_state_uf_county(query):
    list_uf = [unaccent(sa.func.lower(q.uf)) for q in query]
    list_state = [unaccent(sa.func.lower(q.state)) for q in query]
    list_county = [unaccent(sa.func.lower(q.county)) for q in query]
    uf_unaccented_lower = unaccent(sa.func.lower(DataIdentifiersSelectedGeorge.state_province)).in_(list_uf)
    state_unaccented_lower = unaccent(sa.func.lower(DataIdentifiersSelectedGeorge.state_province)).in_(list_state)
    county_unaccented_lower = unaccent(sa.func.lower(DataIdentifiersSelectedGeorge.county)).in_(list_county)

    return state_unaccented_lower, uf_unaccented_lower, county_unaccented_lower


def table_is_empty(query):
    return True if query == 0 else False
