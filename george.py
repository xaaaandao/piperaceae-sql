import logging

import pandas as pd

from models import GeorgeData
from sql import is_query_empty


def data_selected_george(session, filename="./csv/george_data.csv"):
    # pass
    df = pd.read_csv(filename, sep=';', low_memory=False, skipinitialspace=True, header=0, index_col=False)
    df["GEORGE"] = df["GEORGE"].apply(str.upper)
    df = df.drop_duplicates()
    df = df.loc[df["GEORGE"] == "SIM"]

    count = session.query(GeorgeData).count()
    if is_query_empty(count):
        for idx, row in df.iterrows():
            try:
                session.add(GeorgeData(seq=row[0]))
                session.commit()
            except Exception:
                session.rollback()

    count = session.query(GeorgeData).count()
    assert count == 1419
