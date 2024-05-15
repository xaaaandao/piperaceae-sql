import sqlalchemy
import sqlalchemy as sa

from models import Local, County, State, LocalTrusted
from sql import insert
from unaccent import unaccent


def exists_local(data, session):
    return session.query(Local) \
        .filter(sqlalchemy.and_(Local.event_time.__eq__(data['event_time']),
                                Local.continent_ocean.__eq__(data['continent_ocean']),
                                Local.country.__eq__(data['country']),
                                Local.state_province.__eq__(data['state_province']),
                                Local.county.__eq__(data['county']),
                                Local.locality.__eq__(data['locality']),
                                Local.decimal_longitude.__eq__(data['decimal_longitude']),
                                Local.decimal_latitude.__eq__(data['decimal_latitude']),
                                Local.verbatim_longitude.__eq__(data['verbatim_longitude']),
                                Local.verbatim_latitude.__eq__(data['verbatim_latitude']),
                                Local.coordinate_precision.__eq__(data['coordinate_precision']),
                                Local.bounding_box.__eq__(data['bounding_box']),
                                Local.minimum_elevation_in_meters.__eq__(data['minimum_elevation_in_meters']),
                                Local.maximum_elevation_in_meters.__eq__(data['maximum_elevation_in_meters']),
                                Local.minimum_depth_in_meters.__eq__(data['minimum_depth_in_meters']),
                                Local.maximum_depth_in_meters.__eq__(data['maximum_depth_in_meters']))).first()


def create_local(data,exsiccata):
    return Local(event_time=data['event_time'], continent_ocean=data['continent_ocean'], country=data['country'],
                 state_province=data['state_province'], county=data['county'], locality=data['locality'],
                 decimal_longitude=data['decimal_longitude'], decimal_latitude=data['decimal_latitude'],
                 verbatim_longitude=data['verbatim_longitude'], verbatim_latitude=data['verbatim_latitude'],
                 coordinate_precision=data['coordinate_precision'], bounding_box=data['bounding_box'],
                 minimum_elevation_in_meters=data['minimum_elevation_in_meters'],
                 maximum_elevation_in_meters=data['maximum_elevation_in_meters'],
                 minimum_depth_in_meters=data['minimum_depth_in_meters'],
                 maximum_depth_in_meters=data['maximum_depth_in_meters'],
                 exsiccata_id=exsiccata.seq)


def create_local_trusted(local):
    return LocalTrusted(local_id=local)


def insert_local(data, exsiccata, session):
    local = create_local(data, exsiccata)
    insert(local, session)
    local_trusted = create_local_trusted(local)
    insert(local_trusted, session)


def update_county(session):
    counties = session.query(County) \
        .distinct() \
        .all()

    for c in counties:
        query = session.query(Local) \
            .filter(Local.county.__eq__(unaccent(c.name))) \
            .all()

        locals_id = [q.id for q in query]
        # session.query(exsiccata_local) \
        #     .filter(exsiccata_local.c.local_id.in_(locals_id)) \
        #     .update({exsiccata_local.c.county: c.name}, synchronize_session=False)
        # session.commit()


def update_local(session):
    update_country(session)
    # update_state(session)
    # update_county(session)


def update_state(session):
    states = session.query(State) \
        .distinct() \
        .all()

    for s in states:
        query = session.query(Local) \
            .filter(sa.or_(Local.state_province.__eq__(unaccent(s.name.lower())),
                           Local.state_province.__eq__(unaccent(s.uf.lower())))) \
            .all()

        locals_id = [q.id for q in query]
        # session.query(exsiccata_local) \
        #     .filter(exsiccata_local.c.local_id.in_(locals_id)) \
        #     .update({exsiccata_local.c.state_province: s.name}, synchronize_session=False)
        # session.commit()


def update_country(session):
    br_variations = ['Brasil', 'BRASIL', 'Brasil/Bolivia', 'Brasilia', 'brazil', 'Brazil', 'BRazil', 'BRAZIL',
                     '[Brésil]', 'Brésil']
    query = session.query(Local.id).filter(Local.country.in_(br_variations)).all()

    locals_id = [q[0] for q in query]

    session.query(LocalTrusted) \
        .filter(LocalTrusted.local_id.in_(locals_id)) \
        .update({LocalTrusted.country: 'Brasil'}, synchronize_session=False)
