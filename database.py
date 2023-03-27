import itertools
import os

import numpy as np
import pandas as pd
import sqlalchemy
import sqlalchemy as sa
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import sqlalchemy.schema

from images import get_url_image
from models import get_base, DataTrustedIdentifier, Image
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


def get_records_group_by_level(condition, level, minimum_image, session):
    columns = [level, sa.func.array_agg(DataTrustedIdentifier.seq)]
    records = session.query(*columns) \
        .filter(condition) \
        .distinct() \
        .group_by(level) \
        .order_by(level) \
        .having(sa.func.count(level) >= minimum_image) \
        .all()

    return records


def filter_records(color, image_size, minimum_image, records, session):
    list_level_name = []
    list_path_images = []
    for i, q in enumerate(records):
        level = q[0]
        list_seq = q[1]
        query = session.query(sa.func.array_agg(sa.distinct(Image.path))) \
            .filter(sa.and_(Image.seq_id.in_(list_seq),
                            Image.height.__eq__(image_size[0]),
                            Image.width.__eq__(image_size[1]),
                            Image.color_mode == color)) \
            .group_by(Image.seq_id) \
            .all()

        l = list(itertools.chain(*query))  # "remove of tuples"

        if len(l) >= minimum_image:

            # remove images duplicates
            list_only_one_path = []
            for barcode in l:
                list_only_one_path.append(sorted(barcode)[0])  # sorted and catch first value of list

            if len(np.unique(list_only_one_path)) >= minimum_image:
                list_level_name.append(level)
                list_path_images.append(np.unique(list_only_one_path).tolist())

    return list_level_name, list_path_images


def get_informations_images(list_path_images, session):
    list_path_images = list(itertools.chain(*list_path_images))
    columns = [DataTrustedIdentifier.seq, DataTrustedIdentifier.genus, DataTrustedIdentifier.specific_epithet,
               DataTrustedIdentifier.catalog_number, DataTrustedIdentifier.barcode, Image.path,
               DataTrustedIdentifier.institution_code, DataTrustedIdentifier.collection_code]
    condition = sa.and_(Image.path.in_(list_path_images),
                        DataTrustedIdentifier.seq == Image.seq_id)
    query = session.query(*columns) \
        .filter(condition) \
        .all()

    data = [(q.seq, q.genus, q.specific_epithet, q.catalog_number, q.barcode, q.path, q.institution_code,
             q.collection_code, get_url_image(q.barcode, q.collection_code)) for q in query]
    columns = ['seq', 'genus', 'specific_epithet', 'catalog_number', 'barcode', 'path_image', 'institution_code',
               'collection_code', 'url']
    df = pd.DataFrame(data, columns=columns)
    return df


def get_columns_table(table):
    return table.__table__.columns
