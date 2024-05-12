import pandas as pd

from old import database as db
from old.models import DataSP


def update_record_data_sp(row, session):
    try:
        session.query(DataSP) \
            .filter(DataSP.seq == row['seq']) \
            .update({'george': True}, synchronize_session=False)
        session.commit()
    except Exception as e:
        print(e)
        session.flush()


def get_value_column_george(row):
    return row['GEORGE'].lower()


def george_selected_data(row):
     return get_value_column_george(row) == 'sim'


def count_records_selected_by_george(session):
    return session.query(DataSP).filter(DataSP.george).count()


def main():
    engine, session = db.connect()

    filename = '../../csv/george_data.csv'
    df = pd.read_csv(filename, sep=';', low_memory=False, skipinitialspace=True)

    if count_records_selected_by_george(session) == 0:
        n_rows = len(list(df.iterrows()))
        for i, (idx, row) in enumerate(df.iterrows()):
            print('%d/%d' % (i, n_rows))
            if george_selected_data(row):
                update_record_data_sp(row, session)

    # this query should return 1419 rows
    print('George selected %d rows' % count_records_selected_by_george(session))
    session.close()
    engine.dispose()


if __name__ == '__main__':
    main()
