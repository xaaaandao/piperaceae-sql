import logging

import pandas as pd

from data_sp.insert_metadata import rename_header_dataframe, preprocess
from models import DataSP
from sql import is_query_empty


def create_datasp(row):
    return DataSP(seq=row['seq'],
                  modified=row['modified'], institution_code=row['institution_code'],
                  collection_code=row['collection_code'], catalog_number=row['catalog_number'],
                  basis_of_record=row['basis_of_record'], kingdom=row['kingdom'], phylum=row['phylum'],
                  classe=row['class'], order=row['order'], family=row['family'],
                  genus=row['genus'],
                  specific_epithet=row['specific_epithet'],
                  infraspecific_epithet=row['infraspecific_epithet'],
                  scientific_name=row['scientific_name'],
                  scientific_name_authorship=row['scientific_name_authorship'],
                  identified_by=row['identified_by'], year_identified=row['year_identified'],
                  month_identified=row['month_identified'], day_identified=row['day_identified'],
                  type_status=row['type_status'],
                  recorded_by=row['recorded_by'], record_number=row['record_number'],
                  field_number=row['field_number'], year=row['year'], month=row['month'],
                  day=row['day'], event_time=row['event_time'],
                  continent_ocean=row['continent_ocean'], country=row['country'],
                  state_province=row['state_province'], county=row['county'], locality=row['locality'],
                  decimal_longitude=row['decimal_longitude'],
                  decimal_latitude=row['decimal_latitude'], verbatim_longitude=row['verbatim_longitude'],
                  verbatim_latitude=row['verbatim_latitude'],
                  coordinate_precision=row['coordinate_precision'],
                  bounding_box=row['bounding_box'],
                  minimum_elevation_in_meters=row['minimum_elevation_in_meters'],
                  maximum_elevation_in_meters=row['maximum_elevation_in_meters'],
                  minimum_depth_in_meters=row['minimum_depth_in_meters'],
                  maximum_depth_in_meters=row['maximum_depth_in_meters'], sex=row['sex'],
                  preparation_type=row['preparation_type'],
                  individual_count=row['individual_count'],
                  previous_catalog_number=row['previous_catalog_number'],
                  relationship_type=row['relationship_type'],
                  related_catalog_item=row['related_catalog_item'],
                  occurrence_remarks=row['occurrence_remarks'], barcode=row['barcode'],
                  imagecode=row['imagecode'], geo_flag=row['geo_flag'])


def insert_data_specieslink(session, filename='./csv/original.csv'):
    df = pd.read_csv(filename, sep=';', low_memory=False, skipinitialspace=True)

    count = session.query(DataSP).count()
    if is_query_empty(count):
        rename_header_dataframe(df)
        df = preprocess(df)
        for row in df.iterrows():
            data_sp = create_datasp(row[1])
            try:
                session.add(data_sp)
                session.commit()
            except Exception:
                session.rollback()

    count = session.query(DataSP).count()
    logging.info('count of specieslink data is %d' % count)

    assert count == 55453
