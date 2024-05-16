import sqlalchemy as sa

from models import Local, County, LocalTrusted
from unaccent import unaccent


def update_county_unencoded_character(session, unencoded_characters):
    for sc in zip(unencoded_characters['invalid'], unencoded_characters['valid']):
        sc_invalid = sc[0]
        sc_valid = sc[1]
        value = sa.func.replace(Local.county, sc_invalid, sc_valid)
        try:
            session.query(Local) \
                .update(values={Local.county: value}, synchronize_session=False)
            session.commit()
        except Exception as e:
            print(e)
            session.flush()


def update_county_encoded_character(counties, session):
    for c in counties:
        query = session.query(Local) \
            .filter(sa.or_(Local.county.__eq__(c.name),
                           Local.county.__eq__(c.name.lower()),
                           Local.county.__eq__(c.name.upper()),
                           Local.county.__eq__(unaccent(c.name)),
                           Local.county.__eq__(unaccent(c.name.upper())),
                           Local.county.__eq__(unaccent(c.name.lower())))) \
            .all()

        locals_id = [q.id for q in query]
        session.query(LocalTrusted) \
            .filter(LocalTrusted.local_id.in_(locals_id)) \
            .update({LocalTrusted.county: c.name}, synchronize_session=False)
        session.commit()


def update_county(session, unencoded_characters):
    counties = session.query(County) \
        .distinct() \
        .all()

    update_county_unencoded_character(session, unencoded_characters)
    update_county_encoded_character(counties, session)
