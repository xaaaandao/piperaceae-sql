import sqlalchemy as sa

from unittest import TestCase

from database.database import connect
from database.models import County, State


class TestCounty(TestCase):
    session = None
    engine = None

    @classmethod
    def setUp(self):
        engine, session = connect()
        self.engine = engine
        self.session = session

    @classmethod
    def tearDown(self):
        self.engine.dispose()
        self.session.close()

    def test_insert_counties(self):
        count_counties = self.session.query(County).count()
        count_states = self.session.query(State).count()
        self.assertEqual(count_counties, 5570)
        self.assertEqual(count_states, 27)

    def test_counties_must_be_completed(self):
        count_counties = self.session.query(County) \
            .filter(sa.and_(County.name.__ne__(None),
                            County.state_id.__ne__(None))) \
            .count()

        count_states = self.session.query(State) \
            .filter(sa.and_(State.name.__ne__(None),
                            State.uf.__ne__(None),
                            State.region.__ne__(None))) \
            .count()
        self.assertEqual(count_counties, 5570)
        self.assertEqual(count_states, 27)
