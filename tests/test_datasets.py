import numpy as np
import sqlalchemy as sa
from unittest import TestCase

from database.database import connect
from database.models import DatasetSamples, Exsiccata, Level, Local


class TestDatasets(TestCase):

    @classmethod
    def setUp(self):
        engine, session = connect()
        self.engine = engine
        self.session = session


    @classmethod
    def tearDown(self):
        self.engine.dispose()
        self.session.close()

    def test_compare_versions_br(self):
        v1 = self.session.query(DatasetSamples)\
                    .filter(sa.and_(DatasetSamples.name.__eq__('br_dataset'),
                                    DatasetSamples.minimum.__eq__(5),
                                    DatasetSamples.version.__eq__(1)))

        v2 = self.session.query(DatasetSamples) \
            .filter(sa.and_(DatasetSamples.name.__eq__('br'),
                            DatasetSamples.minimum.__eq__(5),
                            DatasetSamples.version.__eq__(2)))

        v1_seqs = [q.seq for q in v1]
        v2_seqs = [q.seq for q in v2]

        # print(np.setdiff1d(v1_seqs, v2_seqs))

        diff = set(v1_seqs) - set(v2_seqs)
        print(len(diff), diff)

        q = self.session.query(Exsiccata.seq, Level.genus, Level.specific_epithet)\
            .join(Level, Exsiccata.level_id == Level.id) \
            .filter(Exsiccata.seq.in_(diff))\
            .order_by(Level.specific_epithet)\
            .all()

        for q2 in q:
            print(q2.seq, q2.genus, q2.specific_epithet)

        diff = set(v2_seqs) - set(v1_seqs)
        print(len(diff))

        # q = self.session.query(Exsiccata.seq, Level.genus_old, Level.specific_epithet_old, Level.genus, Level.specific_epithet) \
        q = self.session.query(Exsiccata.seq, Local.country_old, Local.state_province_old, Local.county_old, Local.country, Local.state_province, Local.county) \
            .join(Level, Exsiccata.level_id == Level.id) \
            .join(Local, Exsiccata.local_id == Local.id) \
            .filter(Exsiccata.seq.in_(diff)) \
            .order_by(Level.specific_epithet) \
            .all()

        for q2 in q:
            # print(q2.seq, q2.genus_old, q2.specific_epithet_old, q2.genus, q2.specific_epithet)
            print(q2.seq, q2.country_old, q2.state_province_old, q2.county_old, q2.country, q2.state_province, q2.county)