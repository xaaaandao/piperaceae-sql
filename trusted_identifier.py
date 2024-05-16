import logging

import pandas as pd

from models import TrustedIdentifier
from sql import insert, is_query_empty


def insert_trusted_identifier(session):
    count = session.query(TrustedIdentifier).count()
    if not is_query_empty(count):
        logging.info('count of trusted identifier is %d' % count)
        assert count == 340
        return

    df = pd.read_csv('./csv/a.csv', sep=';', index_col=False, header=0, encoding='utf-8')
    for idx, row in df.iterrows():
        t = TrustedIdentifier(fullname=row['fullname'], search=row['search'], value_founded=row['value_founded'], selected=row['selected'])
        insert(t, session)
