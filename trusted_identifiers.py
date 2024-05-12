import dataclasses
import logging

import pandas as pd
import sqlalchemy

from models import TrustedIdentifier, DataSP
from sql import is_query_empty


def insert_trusted_identifiers(session, filename="./csv/trusted_identifiers_name.csv"):
    df = pd.read_csv(filename, sep=';', low_memory=False, skipinitialspace=True, header=0, index_col=False)

    count = session.query(TrustedIdentifier).count()
    # #
    if is_query_empty(count):
        full_names = df['full_name'].tolist()
        target_names = df['searched_name'].tolist()
        for item in zip(full_names, target_names):
            full_name_identifier = item[0]
            target = item[1]

            query = session.query(DataSP.identified_by) \
                .filter(DataSP.identified_by.ilike("%{}%".format(target))) \
                .distinct(DataSP.identified_by) \
                .all()
            #
            for q in query:
                logging.info('full name identifier: %s variation founded: %s' % (full_name_identifier, q.identified_by))
                new_identifier_trusted = TrustedIdentifier(name=full_name_identifier, searched_name=target,
                                                           value_founded=q.identified_by, trusted=False)
                try:
                    session.add(new_identifier_trusted)
                    session.commit()
                except Exception:
                    session.rollback()
    #
    count = session.query(TrustedIdentifier).count()
    logging.info('count identifiers inserted: %d' % count)

    assert count == 340


def update_trusted_identifiers(session, filename="./csv/trusted_identifiers.csv"):
    count = session.query(TrustedIdentifier.value_founded) \
        .filter(TrustedIdentifier.trusted) \
        .distinct() \
        .count()

    logging.info('count of variations: %d' % count)

    # aqui eh 187 ou 184?
    assert count == 187

