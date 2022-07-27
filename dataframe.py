import numpy
import pandas
import re

from tables import DataSP


def convert_header_to_snake_case(dataframe):
    return {column_name: re.sub(r'(?<!^)(?=[A-Z])', '_', column_name).lower() for column_name in get_columns_dataframe(dataframe)}


def change_header(dataframe):
    dataframe.rename(columns=convert_header_to_snake_case(dataframe), inplace=True)


def get_columns_numeric(dataframe, table):
    list_of_columns_numeric = list([])
    for columns_dataframe in get_columns_dataframe(dataframe):
        for columns_table in get_columns_table(table):
            if check_if_column_is_numeric(columns_dataframe, columns_table):
                list_of_columns_numeric.append(columns_dataframe)
    return list_of_columns_numeric


def get_columns_table(table):
    return table.__table__.columns


def get_columns_dataframe(dataframe):
    return list([*dataframe.columns])


def check_if_column_is_numeric(columns_dataframe, columns_table):
    return str(columns_dataframe) in str(columns_table) and str(columns_table.type).lower() in ("int", "float")


def replace_nan_to_null(dataframe):
    return dataframe.replace({numpy.nan: None})


def replace_values_not_numeric(dataframe):
    for column in list([*get_columns_numeric(dataframe, DataSP)]):
        dataframe[column] = pandas.to_numeric(getattr(dataframe, column), errors='coerce').fillna(-1)
    return dataframe


def preprocess(dataframe):
    return replace_nan_to_null(replace_values_not_numeric(dataframe))