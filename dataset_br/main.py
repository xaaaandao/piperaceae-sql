import os
import pathlib
import sys
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from dataframe import create_df
from images import copy_all_images, separate_images_per_threshold

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import connect, list_ilike
from tables import DataSP


def main():
    session: Session
    engine, session = connect()

    path_fotos = '/home/xandao/Documentos/dataset-52k-sp-2021/fotos'
    list_images = list([file for file in pathlib.Path(path_fotos).rglob('*') if file.is_file()])
    result = session.query(DataSP.identified_by).filter(DataSP.george).distinct().all()

    print(len(list_images), len(result))

    list_identified = list_ilike(DataSP.identified_by, ['%{}%'.format(r[0]) for r in result])
    list_br = list_ilike(DataSP.country, ['Bra_il'])

    query = session.query(DataSP.specific_epithet, DataSP.barcode).filter(and_(DataSP.specific_epithet.is_not(None),
                                                                               or_(*list_identified),
                                                                               or_(*list_br))).all()

    # dst = 'out/specific_epithet'
    # copy_all_images(dst, list_images, query)
    # separate_images_per_threshold(dst)
    # create_df(dst, query, 'specific_epithet')


if __name__ == '__main__':
    main()
