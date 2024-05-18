import itertools
import logging
import os

import pandas as pd
import sqlalchemy as sa
from prometheus_client import samples

from database.database import connect
from database.models import Exsiccata, DatasetSamples, Level, Identifier, Local, TrustedIdentifier
from database.sql import insert, is_query_empty


def load_datasetv1(session, dir='./csv/datasetv1', version=1):
    query = session.query(DatasetSamples)\
        .filter(sa.and_(DatasetSamples.name.__eq__('br_dataset'),
                        DatasetSamples.version.__eq__(1)))\
        .count()

    if is_query_empty(query):
        for dataset in ['br_dataset', 'pr_dataset']:
            for minimum in ['5', '10', '20']:
                p = os.path.join(dir, dataset, minimum, 'info_samples.csv')
                df = pd.read_csv(p, header=0, index_col=False, sep=';', encoding='utf-8')

                for idx, row in df.iterrows():
                    d = DatasetSamples(seq=row['seq'], genus=row['genus_trusted'], specie=row['specific_epithet_trusted'],
                                       name=dataset, minimum=int(minimum), version=version)
                    insert(d, session)


def load_datasetv2(session, version=2):
    columns = [Level.genus, Level.specific_epithet, sa.func.array_agg(Exsiccata.seq).label('seqs')]
    query = session.query(*columns) \
        .join(Identifier, Exsiccata.identifier_id.__eq__(Identifier.id)) \
        .join(Level, Exsiccata.level_id.__eq__(Level.id)) \
        .join(Local, Exsiccata.local_id.__eq__(Local.id)) \
        .join(TrustedIdentifier, TrustedIdentifier.value_founded.__eq__(Identifier.identified_by)) \
        .filter(sa.and_(TrustedIdentifier.selected,
                        sa.or_(Local.country.__eq__('Brasil'),
                               sa.and_(Local.country.__eq__(None),
                                       Local.state_province.__ne__(None),
                                       Local.county.__ne__(None))),
                        Level.specific_epithet.__ne__(None),
                        Level.genus.__ne__(None)),
                        sa.or_(Level.infraspecific_epithet.__eq__(None),
                               Level.scientific_name_authorship.__eq__(None))) \
        .group_by(Level.genus, Level.specific_epithet) \
        .having(sa.func.count(Level.specific_epithet) >= 5) \
        .all()

    logging.info('count of samples %d', len(query))
    seqs = [q.seqs for q in query]
    seqs = list(itertools.chain(*seqs))

    query = session.query(Exsiccata) \
        .join(Level, Exsiccata.level_id.__eq__(Level.id)) \
        .filter(Exsiccata.seq.in_(seqs)) \
        .all()

    logging.info('count of samples %d', len(query))

    logging.info('count of samples %d', len(query))
    for q in query:
        d = DatasetSamples(seq=q.seq, genus=q.level.genus, specie=q.level.specific_epithet, name='br', minimum=5,
                           version=version)
        insert(d, session)