import sqlalchemy as sa

from unittest import TestCase

import database as db
from models import County, DataTrustedIdentifier
from unaccent import unaccent


class Test(TestCase):
    color = 'rgb'
    engine = None
    image_size = (256, 256)
    level = None
    minimum_image = 5
    session = None

    def setUp(self) -> None:
        super().setUp()
        self.engine, self.session = db.connect()
        self.engine.echo=False
        self.level = DataTrustedIdentifier.specific_epithet_trusted

    def tearDown(self) -> None:
        super().tearDown()
        self.session.close()
        self.engine.dispose()


    def test_filter_records(self):
        records = [('emygdioi', [13300, 13301 ,13296, 13297, 13298],)]
        l, m = db.filter_records(self.color, self.image_size, self.minimum_image, records, self.session)
        print(l, m)