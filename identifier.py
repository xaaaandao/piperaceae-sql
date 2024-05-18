import logging

import pandas as pd
import sqlalchemy as sa

from database.models import TrustedIdentifier, Identifier, Exsiccata
from database.sql import insert, is_query_empty


def insert_trusted_identifier(session):
    count = session.query(TrustedIdentifier).count()
    count_differents = session.query(TrustedIdentifier.value_founded) \
        .filter(TrustedIdentifier.selected) \
        .distinct() \
        .count()
    count_selected = session.query(TrustedIdentifier) \
        .filter(TrustedIdentifier.selected) \
        .count()

    trusted_identifiers = session.query(TrustedIdentifier).filter(TrustedIdentifier.selected).all()
    trusted_identifiers = [t.value_founded for t in trusted_identifiers]
    count_samples = session.query(Exsiccata) \
        .join(Identifier, Exsiccata.identifier_id.__eq__(Identifier.id)) \
        .filter(Identifier.identified_by.in_(trusted_identifiers)) \
        .count()
    if not is_query_empty(count):
        logging.info('count of trusted identifier is %d' % count)
        logging.info('count of differents trusted identifier selected %d' % count_differents)
        logging.info('count of trusted identifier selected is %d' % count_selected)
        logging.info('count of samples trusted identifier %d' % count_samples)
        assert count == 340 and count_selected == 212 and count_differents == 187 and count_samples == 13182
        return

    df = pd.read_csv('csv/trusted_identifiers.csv', sep=';', index_col=False, header=0, encoding='utf-8')
    for idx, row in df.iterrows():
        t = TrustedIdentifier(fullname=row['fullname'], search=row['search'], value_founded=row['value_founded'],
                              selected=row['selected'])
        insert(t, session)


def exists_identifier(row, session):
    return session.query(Identifier) \
        .filter(sa.and_(Identifier.identified_by.__eq__(row['identified_by']),
                        Identifier.year_identified.__eq__(row['year_identified']),
                        Identifier.month_identified.__eq__(row['month_identified']),
                        Identifier.day_identified.__eq__(row['day_identified']))) \
        .first()


def create_identifier(row):
    return Identifier(identified_by=row['identified_by'],
                      year_identified=row['year_identified'],
                      month_identified=row['month_identified'],
                      day_identified=row['day_identified'])
