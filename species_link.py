import logging
import pandas as pd

from dataframe import rename_header_dataframe, preprocess
from database.models import Exsiccata
from database.sql import is_query_empty, insert
from identifier import exists_identifier, create_identifier
from level import exists_level, create_level
from local.local import exists_local, create_local


def create_exsiccata(identifier, level, local, row):
    return Exsiccata(seq=row['seq'],
                     modified=row['modified'],
                     institution_code=row['institution_code'],
                     collection_code=row['collection_code'],
                     catalog_number=row['catalog_number'],
                     basis_of_record=row['basis_of_record'],
                     identified_by=row['identified_by'],
                     year_identified=row['year_identified'],
                     month_identified=row['month_identified'],
                     day_identified=row['day_identified'],
                     type_status=row['type_status'],
                     recorded_by=row['recorded_by'],
                     record_number=row['record_number'],
                     field_number=row['field_number'],
                     year=row['year'],
                     month=row['month'],
                     day=row['day'],
                     event_time=row['event_time'],
                     bounding_box=row['bounding_box'],
                     minimum_elevation_in_meters=row['minimum_elevation_in_meters'],
                     maximum_elevation_in_meters=row['maximum_elevation_in_meters'],
                     minimum_depth_in_meters=row['minimum_depth_in_meters'],
                     maximum_depth_in_meters=row['maximum_depth_in_meters'],
                     sex=row['sex'],
                     preparation_type=row['preparation_type'],
                     individual_count=row['individual_count'],
                     previous_catalog_number=row['previous_catalog_number'],
                     relationship_type=row['relationship_type'],
                     related_catalog_item=row['related_catalog_item'],
                     occurrence_remarks=row['occurrence_remarks'],
                     barcode=row['barcode'],
                     imagecode=row['imagecode'],
                     geo_flag=row['geo_flag'],
                     level_id=level.id,
                     local_id=local.id,
                     identifier_id=identifier.id)


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
        level = exists_level(row, session)
        if not level:
            level = create_level(row)
            insert(level, session)

        local = exists_local(row, session)
        if not local:
            local = create_local(row)
            insert(local, session)

        identifier = exists_identifier(row, session)
        if not identifier:
            identifier = create_identifier(row)
            insert(identifier, session)

        exsiccata = create_exsiccata(identifier, level, local, row)
        insert(exsiccata, session)


