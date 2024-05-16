import logging

import pandas as pd

from models import GeorgeData
from sql import is_query_empty, insert


def insert_data_george(session, filename="./csv/george_data.csv"):
    count = session.query(GeorgeData).count()
    if not is_query_empty(count):
        logging.info('count of george_data is %d' % count)
        assert count == 1419
        return

    df = pd.read_csv(filename, sep=';', low_memory=False, skipinitialspace=True, header=0, index_col=False,
                     encoding='utf-8')
    df["GEORGE"] = df["GEORGE"].apply(str.upper)
    df = df.drop_duplicates()
    df = df.loc[df["GEORGE"] == "SIM"]

    for idx, row in df.iterrows():
        insert(GeorgeData(exsiccata_id=row[0]), session)



