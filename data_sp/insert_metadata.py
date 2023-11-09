import numpy as np
import pandas as pd
import re

import database as db
from database import get_columns_table
from models import DataSP


def check_if_type_column_is_int_or_float(columns_table):
    return str(columns_table.type).lower() in ('int', 'float')


def replace_nan_to_null(dataframe):
    return dataframe.replace({np.nan: None})


def replace_values_not_numeric(dataframe):
    for column in [*get_columns_numeric(dataframe, DataSP)]:
        dataframe[column] = pd.to_numeric(getattr(dataframe, column), errors='coerce').fillna(-1)
    return dataframe


def count_in_data_sp(session):
    return session.query(DataSP).count()


def column_is_numeric(columns_dataframe, columns_table):
    return str(columns_dataframe) in str(columns_table.type) and check_if_type_column_is_int_or_float(columns_table)


def preprocess(dataframe):
    rename_header_dataframe(dataframe)
    return replace_nan_to_null(replace_values_not_numeric(dataframe))


def rename_header_dataframe(df):
    df.rename(columns=convert_header_snake_case_to_lower_case(df), inplace=True)


def get_columns_numeric(dataframe, table):
    list_columns_dataframe = [column.lower() for column in get_columns_dataframe(dataframe)]
    list_columns_table = [column for column in get_columns_table(table)]
    return [c_table.key for c_table in list_columns_table if
            exits_column_table_in_dataframe(c_table, list_columns_dataframe) and column_table_is_numeric(c_table)]


def column_table_is_numeric(c_table):
    return 'int' in str(c_table.type).lower() or 'float' in str(c_table.type).lower()


def convert_header_snake_case_to_lower_case(dataframe):
    return {column_name: re.sub(r'(?<!^)(?=[A-Z])', '_', column_name).lower() for column_name in
            get_columns_dataframe(dataframe)}


def exits_column_table_in_dataframe(column_table, list_columns_dataframe):
    return column_table.key in list_columns_dataframe


def get_columns_dataframe(dataframe):
    return [*dataframe.columns]


def parse_row(info):
    return DataSP(seq=info['seq'],
                  modified=info['modified'], institution_code=info['institution_code'],
                  collection_code=info['collection_code'], catalog_number=info['catalog_number'],
                  basis_of_record=info['basis_of_record'], kingdom=info['kingdom'], phylum=info['phylum'],
                  classe=info['class'], order=info['order'], family=info['family'],
                  genus=info['genus'],
                  specific_epithet=info['specific_epithet'],
                  infraspecific_epithet=info['infraspecific_epithet'],
                  scientific_name=info['scientific_name'],
                  scientific_name_authorship=info['scientific_name_authorship'],
                  identified_by=info['identified_by'], year_identified=info['year_identified'],
                  month_identified=info['month_identified'], day_identified=info['day_identified'],
                  type_status=info['type_status'],
                  recorded_by=info['recorded_by'], record_number=info['record_number'],
                  field_number=info['field_number'], year=info['year'], month=info['month'],
                  day=info['day'], event_time=info['event_time'],
                  continent_ocean=info['continent_ocean'], country=info['country'],
                  state_province=info['state_province'], county=info['county'], locality=info['locality'],
                  decimal_longitude=info['decimal_longitude'],
                  decimal_latitude=info['decimal_latitude'], verbatim_longitude=info['verbatim_longitude'],
                  verbatim_latitude=info['verbatim_latitude'],
                  coordinate_precision=info['coordinate_precision'],
                  bounding_box=info['bounding_box'],
                  minimum_elevation_in_meters=info['minimum_elevation_in_meters'],
                  maximum_elevation_in_meters=info['maximum_elevation_in_meters'],
                  minimum_depth_in_meters=info['minimum_depth_in_meters'],
                  maximum_depth_in_meters=info['maximum_depth_in_meters'], sex=info['sex'],
                  preparation_type=info['preparation_type'],
                  individual_count=info['individual_count'],
                  previous_catalog_number=info['previous_catalog_number'],
                  relationship_type=info['relationship_type'],
                  related_catalog_item=info['related_catalog_item'],
                  occurrence_remarks=info['occurrence_remarks'], barcode=info['barcode'],
                  imagecode=info['imagecode'], geo_flag=info['geo_flag'])


def insert_row(df, session):
    n_rows = len(list(df.iterrows()))
    for i, (idx, row) in enumerate(df.iterrows()):
        print('%d/%d' % (i, n_rows))
        data_sp = parse_row(row)
        try:
            session.add(data_sp)
            session.commit()
        except Exception as e:
            print(e)
            session.flush()


def main():
    engine, session = db.connect()

    filename = '../csv/original.csv'
    df = pd.read_csv(filename, sep=';', low_memory=False, skipinitialspace=True)

    if db.table_is_empty(count_in_data_sp(session)):
        df = preprocess(df)
        insert_row(df, session)


    session.close()
    engine.dispose()


if __name__ == '__main__':
    main()
