import pandas as pd

import database as db
from models import DataSP


def update_record_data_sp(dict_cols, row, session):
    try:
        session.query(DataSP) \
            .filter(DataSP.seq == row[dict_cols['seq']]) \
            .update({'george': True}, synchronize_session=False)
        session.commit()
    except Exception as e:
        print(e)
        session.flush()


def george_selected_data(dict_cols, row):
     return row[dict_cols['GEORGE']].lower() == 'sim'


def count_records_selected_by_george(session):
    return session.query(DataSP).filter(DataSP.george).count()


def set_george_data(session, filename='./csv/george_data.csv'):
    df = pd.read_csv(filename, sep=';', low_memory=False, skipinitialspace=True)

    if count_records_selected_by_george(session) == 1419:
        return

    dict_cols = {j: i for i, j in enumerate(df.columns)}
    for row in df.values:
        if george_selected_data(dict_cols, row):
            update_record_data_sp(dict_cols, row, session)

    # this query should return 1419 rows
    assert(count_records_selected_by_george(session) == 1419)


