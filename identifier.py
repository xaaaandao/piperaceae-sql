import sqlalchemy as sa

from models import Identifier
from sql import insert


def exists_identifier(data, session):
    return session.query(Identifier) \
        .filter(sa.and_(Identifier.identified_by.__eq__(data['identified_by']),
                        Identifier.year_identified.__eq__(data['year_identified']),
                        Identifier.month_identified.__eq__(data['month_identified']),
                        Identifier.day_identified.__eq__(data['day_identified']))).first()


def create_identifier(data):
    return Identifier(identified_by=data['identified_by'],
                      year_identified=data['year_identified'], month_identified=data['month_identified'],
                      day_identified=data['day_identified'])


def insert_identifier(data, session):
    i = exists_identifier(data, session)
    if not i:
        identifier = create_identifier(data)
        insert(identifier, session)
        return identifier

    return i
