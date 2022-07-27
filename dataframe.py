import numpy
import pandas
import re

from tables import DataSP


def convert_header_to_snake_case(dataframe):
    return {column_name: re.sub(r'(?<!^)(?=[A-Z])', '_', column_name).lower() for column_name in
            get_columns_dataframe(dataframe)}


def change_header(dataframe):
    dataframe.rename(columns=convert_header_to_snake_case(dataframe), inplace=True)


def get_columns_numeric(dataframe, table):
    list_columns_dataframe = list([column.lower() for column in get_columns_dataframe(dataframe)])
    list_columns_table = list([column for column in get_columns_table(table)])
    return list([c_table.key for c_table in list_columns_table if
                 exits_column_table_in_dataframe(c_table, list_columns_dataframe) and column_table_is_numeric(c_table)])


def column_table_is_numeric(c_table):
    return "int" in str(c_table.type).lower() or "float" in str(c_table.type).lower()


def exits_column_table_in_dataframe(c_table, list_columns_dataframe):
    return c_table.key in list_columns_dataframe


def get_columns_table(table):
    return table.__table__.columns


def get_columns_dataframe(dataframe):
    return list([*dataframe.columns])


def check_if_column_is_numeric(columns_dataframe, columns_table):
    return str(columns_dataframe) in str(columns_table.type) and str(columns_table.type).lower() in ("int", "float")


def replace_nan_to_null(dataframe):
    return dataframe.replace({numpy.nan: None})


def replace_values_not_numeric(dataframe):
    for column in list([*get_columns_numeric(dataframe, DataSP)]):
        dataframe[column] = pandas.to_numeric(getattr(dataframe, column), errors='coerce').fillna(-1)
    return dataframe


def preprocess(dataframe):
    return replace_nan_to_null(replace_values_not_numeric(dataframe))
