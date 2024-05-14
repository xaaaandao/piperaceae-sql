import sqlalchemy

from models import Local
from sql import insert


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


def create_local(data):
    return Local(event_time=data['event_time'], continent_ocean=data['continent_ocean'], country=data['country'],
                 state_province=data['state_province'], county=data['county'], locality=data['locality'],
                 decimal_longitude=data['decimal_longitude'], decimal_latitude=data['decimal_latitude'],
                 verbatim_longitude=data['verbatim_longitude'], verbatim_latitude=data['verbatim_latitude'],
                 coordinate_precision=data['coordinate_precision'], bounding_box=data['bounding_box'],
                 minimum_elevation_in_meters=data['minimum_elevation_in_meters'],
                 maximum_elevation_in_meters=data['maximum_elevation_in_meters'],
                 minimum_depth_in_meters=data['minimum_depth_in_meters'],
                 maximum_depth_in_meters=data['maximum_depth_in_meters'])


def insert_local(data, session):
    l = exists_local(data, session)
    if not l:
        local = create_local(data)
        insert(local, session)
        return local

    return l
