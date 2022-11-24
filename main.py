import os
import pathlib
import sys

import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from api import get_municipies
from dataframe import create_df, change_header, preprocess
from images import copy_all_images, separate_images_per_threshold

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import connect, list_ilike, make_operation, create_table_if_not_exists
from tables import DataSP, get_base, create_datasp, create_county, County


def has_data_in_table(session, table):
    return session.query(table).count() == 0


def main():
    user = os.environ['POSTGRE_USER']
    password = os.environ['POSTGRE_PASSWORD']
    cfg = {
        'host': '192.168.0.144',
        'user': user,
        'password': password,
        'port': '5432',
        'database': 'herbario'
    }

    session: Session
    engine, session = connect()

    filename_sp = 'csv/original.csv'
    filename_george = 'csv/dados-george.csv'

    df_sp = pd.read_csv(filename_sp, sep=';', low_memory=False, skipinitialspace=True)
    df_george = pd.read_csv(filename_george, sep=';', low_memory=False, skipinitialspace=True)

    create_table_if_not_exists(cfg, engine, 'county')
    create_table_if_not_exists(cfg, engine, 'data')

    if has_data_in_table(session, County):
        response = get_municipies()
        insert_municipies_in_database(response, session)

    if has_data_in_table(session, DataSP):
        dataframe = preprocess(df_sp)
        insert_dataframe_in_database(dataframe, session)

    if has_true_in_column_george(session):
        update_values_marked_by_george(df_george, session)

    session.close()
    engine.dispose()


def update_values_marked_by_george(df_george, session):
    for row in df_george.iterrows():
        if check_if_george_mark_true(row):
            seq = row[1]['seq']
            session.query(DataSP).filter(DataSP.seq == seq).update({'george': True}, synchronize_session=False)
            make_operation(session)


def check_if_george_mark_true(row):
    return row[1]['GEORGE'].lower() == 'sim'


def has_true_in_column_george(session):
    return session.query(DataSP).filter(DataSP.george).count() == 0


def insert_dataframe_in_database(dataframe, session):
    for row in dataframe.iterrows():
        session.add(create_datasp(row[1]))
        make_operation(session)


def insert_municipies_in_database(response, session):
    for i, county in enumerate(response.json()):
        session.add(create_county(county))
        make_operation(session)


if __name__ == '__main__':
    main()
