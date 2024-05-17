import sqlalchemy as sa
from unittest import TestCase

from database.database import connect
from database.models import Local


class Test(TestCase):
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

    def test_update_county_old_to_county(self):
        """
        Testa se o registro seq=17127 não atualizou o campo county depois do update.
        """
        local = self.session.query(Local)\
            .filter(sa.and_(Local.id.__eq__(17127)))\
            .first()

        self.assertIsNotNone(local.county_old)
        self.assertIsNone(local.county)