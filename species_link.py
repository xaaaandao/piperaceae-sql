import logging

import pandas as pd

from dataframe import rename_header_dataframe, preprocess
from identifier import insert_identifier
from level import insert_level, has_level_valid, update_level_valid
from local.local import insert_local
from models import Exsiccata
from sql import is_query_empty, insert


def create_exsiccata(row):
    return Exsiccata(seq=row['seq'],
                     institution_code=row['institution_code'],
                     collection_code=row['collection_code'], catalog_number=row['catalog_number'],
                     basis_of_record=row['basis_of_record'],
                     type_status=row['type_status'],
                     recorded_by=row['recorded_by'], record_number=row['record_number'],
                     field_number=row['field_number'], year=row['year'], month=row['month'],
                     day=row['day'], sex=row['sex'],
                     preparation_type=row['preparation_type'],
                     individual_count=row['individual_count'],
                     previous_catalog_number=row['previous_catalog_number'],
                     relationship_type=row['relationship_type'],
                     related_catalog_item=row['related_catalog_item'],
                     occurrence_remarks=row['occurrence_remarks'], barcode=row['barcode'],
                     imagecode=row['imagecode'], geo_flag=row['geo_flag'])


def insert_data_specieslink(session, filename='./csv/original.csv'):
    count = session.query(Exsiccata).count()
    if not is_query_empty(count):
        logging.info('count of specieslink data is %d' % count)
        assert count == 55453
        return

    df = pd.read_csv(filename, sep=';', low_memory=False, skipinitialspace=True, encoding='utf-8')
    rename_header_dataframe(df)
    df = preprocess(df)
    for idx, row in df.iterrows():
        exsiccata = create_exsiccata(row)
        level = insert_level(row, session)
        update_level_valid(session)
        level_valid = has_level_valid(row, session)
        identifier = insert_identifier(row, session)
        exsiccata.levels.append(level)
        exsiccata.levels_valid.append(level_valid)
        exsiccata.identifiers.append(identifier)
        insert(exsiccata, session)
        insert_local(row, exsiccata, session)
