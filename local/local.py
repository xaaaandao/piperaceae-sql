from local.country import update_country
from local.county import update_county
from local.state import update_state
from models import Local, LocalTrusted
from sql import insert


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
    return LocalTrusted(local_id=local.id)


def insert_local(data, exsiccata, session):
    local = create_local(data, exsiccata)
    insert(local, session)
    local_trusted = create_local_trusted(local)
    insert(local_trusted, session)


def update_local(session):
    unencoded_characters = {
        'invalid': ['Ã¡', 'Ãº', 'Ã', 'Ã³', 'Ã±', 'Ã©'],
        'valid': ['á', 'ú', 'í', 'ó', 'ñ', 'é']
    }
    update_country(session)
    update_state(session, unencoded_characters)
    update_county(session, unencoded_characters)


