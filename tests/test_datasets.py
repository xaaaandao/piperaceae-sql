import numpy as np
import sqlalchemy as sa
from unittest import TestCase

from database.database import connect
from database.models import DatasetSamples


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

        print(len(v1_seqs), len(v2_seqs))
        print(v1_seqs in v2_seqs)
        diff = set(v1_seqs) - set(v2_seqs)
        print(diff)
        diff2 = np.setdiff1d(v1_seqs, v2_seqs)
        print(diff2)

