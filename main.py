import oslike
import sys

import pandas as pd
from sqlalchemy.orm import Session

from api import get_municipies
from dataframe import preprocess

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import connect, create_table_if_not_exists, table_is_empty, \
    update_values_marked_by_george, has_true_in_column_george, insert_dataframe_in_database, \
    insert_municipies_in_database
from tables import DataSP, County


def main():
    session: Session
    engine, session = connect()

    filename_sp = 'csv/original.csv'
    filename_george = 'csv/george_data.csv'

    df_sp = pd.read_csv(filename_sp, sep=';', low_memory=False, skipinitialspace=True, encoding='utf-8-sig')
    df_george = pd.read_csv(filename_george, sep=';', low_memory=False, skipinitialspace=True)

    create_table_if_not_exists(engine, 'county')
    create_table_if_not_exists(engine, 'data')

    if table_is_empty(session, County):
        response = get_municipies()
        insert_municipies_in_database(response, session)

    if table_is_empty(session, DataSP):
        dataframe = preprocess(df_sp)
        insert_dataframe_in_database(dataframe, session)

    if has_true_in_column_george(session):
        update_values_marked_by_george(df_george, session)

    session.close()
    engine.dispose()


if __name__ == '__main__':
    main()
