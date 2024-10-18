import numpy as np
import pandas as pd
import re

import database as db
from database import get_columns_table, insert
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


def create_datasp(dict_cols:dict, row):
    return DataSP(seq=row[dict_cols['seq']],
                  modified=row[dict_cols['modified']], institution_code=row[dict_cols['institution_code']],
                  collection_code=row[dict_cols['collection_code']], catalog_number=row[dict_cols['catalog_number']],
                  basis_of_record=row[dict_cols['basis_of_record']], kingdom=row[dict_cols['kingdom']], phylum=row[dict_cols['phylum']],
                  classe=row[dict_cols['class']], order=row[dict_cols['order']], family=row[dict_cols['family']],
                  genus=row[dict_cols['genus']],
                  specific_epithet=row[dict_cols['specific_epithet']],
                  infraspecific_epithet=row[dict_cols['infraspecific_epithet']],
                  scientific_name=row[dict_cols['scientific_name']],
                  scientific_name_authorship=row[dict_cols['scientific_name_authorship']],
                  identified_by=row[dict_cols['identified_by']], year_identified=row[dict_cols['year_identified']],
                  month_identified=row[dict_cols['month_identified']], day_identified=row[dict_cols['day_identified']],
                  type_status=row[dict_cols['type_status']],
                  recorded_by=row[dict_cols['recorded_by']], record_number=row[dict_cols['record_number']],
                  field_number=row[dict_cols['field_number']], year=row[dict_cols['year']], month=row[dict_cols['month']],
                  day=row[dict_cols['day']], event_time=row[dict_cols['event_time']],
                  continent_ocean=row[dict_cols['continent_ocean']], country=row[dict_cols['country']],
                  state_province=row[dict_cols['state_province']], county=row[dict_cols['county']], locality=row[dict_cols['locality']],
                  decimal_longitude=row[dict_cols['decimal_longitude']],
                  decimal_latitude=row[dict_cols['decimal_latitude']], verbatim_longitude=row[dict_cols['verbatim_longitude']],
                  verbatim_latitude=row[dict_cols['verbatim_latitude']],
                  coordinate_precision=row[dict_cols['coordinate_precision']],
                  bounding_box=row[dict_cols['bounding_box']],
                  minimum_elevation_in_meters=row[dict_cols['minimum_elevation_in_meters']],
                  maximum_elevation_in_meters=row[dict_cols['maximum_elevation_in_meters']],
                  minimum_depth_in_meters=row[dict_cols['minimum_depth_in_meters']],
                  maximum_depth_in_meters=row[dict_cols['maximum_depth_in_meters']], sex=row[dict_cols['sex']],
                  preparation_type=row[dict_cols['preparation_type']],
                  individual_count=row[dict_cols['individual_count']],
                  previous_catalog_number=row[dict_cols['previous_catalog_number']],
                  relationship_type=row[dict_cols['relationship_type']],
                  related_catalog_item=row[dict_cols['related_catalog_item']],
                  occurrence_remarks=row[dict_cols['occurrence_remarks']], barcode=row[dict_cols['barcode']],
                  imagecode=row[dict_cols['imagecode']], geo_flag=row[dict_cols['geo_flag']])


def insert_row(df, session):
    dict_cols = {j: i for i, j in enumerate(df.columns)}

    if db.count_of_table(session, DataSP) == 55453:
        return

    for row in df.values:
        data = create_datasp(dict_cols, row)
        insert(data, session)

    assert(db.count_of_table(session, DataSP) == 55453)


def insert_csv_sp(session, filename='./csv/original.csv'):
    # engine, session = db.connect()

    # filename = '../csv/original.csv'
    df = pd.read_csv(filename, sep=';', low_memory=False, skipinitialspace=True)

    if db.table_is_empty(count_in_data_sp(session)):
        df = preprocess(df)
        insert_row(df, session)


    # session.close()
    # engine.dispose()


