import pandas as pd

from models import TrustedIdentifier, TrustedIdentifierSelected
from sql import insert


def insert_trusted_identifier(session):
    # if session.query(TrustedIdentifier).count() == 0:
    df = pd.read_csv('./csv/trusted_identifiers.csv', sep=';', index_col=False, header=0)
    df_selected = pd.read_csv('./csv/a.csv', sep=';', index_col=False, header=0)
    for idx, row in df.iterrows():
        t = TrustedIdentifier(fullname=row['fullname'], search=row['search'])
        insert(t, session)

        df_value_founded = df_selected.loc[df_selected['fullname'].__eq__(row['fullname'])]
        for idx, row in df_value_founded.iterrows():
            tis = TrustedIdentifierSelected(value_founded=row['value_founded'],
                                            selected=row['selected'],
                                            trusted_identifier_id=t.id)
            insert(tis, session)
