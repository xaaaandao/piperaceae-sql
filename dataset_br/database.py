import itertools
import numpy as np
import os
import pandas as pd
import sqlalchemy as sa

from sqlalchemy.orm import sessionmaker
from tables import DataTrustedIdentifier, InfoImage
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
        engine = sa.create_engine(
            'postgresql+psycopg2://%s:%s@%s:%s/%s' % (
                cfg['user'], cfg['password'], cfg['host'], cfg['port'], cfg['database']), echo=echo, pool_pre_ping=True)
        session = sessionmaker(bind=engine)
        session.configure(bind=engine)
        db = session()
        if engine.connect():
            return engine, db
    except Exception as e:
        print('problems with host %s (%s)' % (cfg['host'], e))


def get_list_uf_state_county(query):
    list_uf = [unaccent(sa.func.lower(q.uf)) for q in query]
    list_state = [unaccent(sa.func.lower(q.state)) for q in query]
    list_county = [unaccent(sa.func.lower(q.county)) for q in query]

    uf_unaccented_lower = unaccent(sa.func.lower(DataTrustedIdentifier.state_province)).in_(list_uf)
    state_unaccented_lower = unaccent(sa.func.lower(DataTrustedIdentifier.state_province)).in_(list_state)
    county_unaccented_lower = unaccent(sa.func.lower(DataTrustedIdentifier.county)).in_(list_county)

    return uf_unaccented_lower, state_unaccented_lower, county_unaccented_lower


def get_records_group_by_level(columns, condition, level, minimum_image, session):
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
        query = session.query(sa.func.array_agg(sa.distinct(InfoImage.path_image))) \
            .filter(sa.and_(InfoImage.seq_id.in_(list_seq),
                            InfoImage.image_size == image_size,
                            InfoImage.color_mode == color)) \
            .group_by(InfoImage.seq_id) \
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
    list_path_images =  list(itertools.chain(*list_path_images))
    columns = [DataTrustedIdentifier.seq, DataTrustedIdentifier.genus, DataTrustedIdentifier.specific_epithet, DataTrustedIdentifier.catalog_number, DataTrustedIdentifier.barcode, InfoImage.path_image, DataTrustedIdentifier.institution_code, DataTrustedIdentifier.collection_code]
    condition = sa.and_(InfoImage.path_image.in_(list_path_images),
                        DataTrustedIdentifier.seq==InfoImage.seq_id)
    query = session.query(*columns)\
            .filter(condition)\
            .all()


    data = [(q.seq, q.genus, q.specific_epithet, q.catalog_number, q.barcode, q.path_image, q.institution_code, q.collection_code, get_url_image(q.barcode, q.collection_code)) for q in query]
    columns = ['seq', 'genus', 'specific_epithet', 'catalog_number', 'barcode', 'path_image', 'institution_code', 'collection_code', 'url']
    df = pd.DataFrame(data, columns=columns)
    return df


def get_url_image(barcode, herbarium, height=5000, width=5000):
    return 'https://specieslink.net/search/util/osd-dezoomify?imagecode=%s&path=herbaria/%s/%s&width=%s&height=%s' % (barcode, herbarium, barcode, str(width), str(height))