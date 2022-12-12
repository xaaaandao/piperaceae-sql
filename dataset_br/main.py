import os
import pathlib
import sys

import sqlalchemy as sa

from database import connect, state_province_in_list_uf_or_list_state
from images import copy_all_images, separate_images_per_threshold

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath('main.py'))))

from tables import County, DataTrustedIdentifier
from sqlalchemy import and_
from sqlalchemy.orm import Session

from unaccent import unaccent


def main():
    session: Session
    engine, session = connect()

    columns = [DataTrustedIdentifier.specific_epithet, DataTrustedIdentifier.barcode, DataTrustedIdentifier.country,
               DataTrustedIdentifier.state_province, DataTrustedIdentifier.county]
    dataset_br(columns, session)
    dataset_regioes(columns, session)


def dataset_regioes(columns, session):
    for regiao in ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']:
        county = session.query(County) \
            .filter(County.regiao == regiao) \
            .distinct() \
            .all()

        list_uf, list_state = get_list_uf_and_state(county)

        query = get_query_using_list_uf_and_state(columns, list_state, list_uf, session)

        dst = 'regioes'
        save_images(dst, query)


def get_query_using_list_uf_and_state(columns, list_state, list_uf, session):
    return session.query(*columns) \
        .filter(and_(DataTrustedIdentifier.country_trusted == 'Brasil',
                     DataTrustedIdentifier.specific_epithet.is_not(None),
                     state_province_in_list_uf_or_list_state(list_state, list_uf))) \
        .distinct() \
        .all()


def get_list_uf_and_state(county):
    list_uf = [unaccent(sa.func.lower(c.uf)) for c in county]
    list_state = [unaccent(sa.func.lower(c.state)) for c in county]

    return list_uf, list_state


def dataset_br(columns, session):
    county = session.query(County).distinct().all()
    list_uf, list_state = get_list_uf_and_state(county)

    query = get_query_using_list_uf_and_state(columns, list_state, list_uf, session)

    dst = 'brasil'
    save_images(dst, query)


def save_images(dst, query):
    for color in ['RGB', 'grayscale']:
        for image_size in ['256', '400', '512']:
            path_fotos = '/home/xandao/%s/%s/w_pred_mask' % (color, image_size)
            list_images = list([file for file in pathlib.Path(path_fotos).glob('*.jpeg')])
            dst = '%s/%s/%s' % (dst, color, image_size)
            copy_all_images(dst, list_images, query)
            separate_images_per_threshold(dst)


if __name__ == '__main__':
    main()