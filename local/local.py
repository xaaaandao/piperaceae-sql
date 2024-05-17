import sqlalchemy as sa

from database.models import Local
from local.country import update_country
from local.county import update_county
from local.state import update_state


def update_local(session):
    unencoded_characters = {
        'invalid': ['Ã¡', 'Ãº', 'Ã', 'Ã³', 'Ã±', 'Ã©'],
        'valid': ['á', 'ú', 'í', 'ó', 'ñ', 'é']
    }
    update_country(session)
    update_state(session, unencoded_characters)
    update_county(session, unencoded_characters)


def exists_local(row, session):
    return session.query(Local) \
        .filter(sa.and_(Local.continent_ocean.__eq__(row['continent_ocean']),
                        Local.country_old.__eq__(row['country']),
                        Local.state_province_old.__eq__(row['state_province']),
                        Local.county_old.__eq__(row['county']),
                        Local.locality.__eq__(row['locality']),
                        Local.decimal_longitude.__eq__(row['decimal_longitude']),
                        Local.decimal_latitude.__eq__(row['decimal_latitude']),
                        Local.verbatim_longitude.__eq__(row['verbatim_longitude']),
                        Local.verbatim_latitude.__eq__(row['verbatim_latitude']),
                        Local.coordinate_precision.__eq__(row['coordinate_precision']))) \
        .first()


def create_local(row):
    return Local(continent_ocean=row['continent_ocean'],
                 country_old=row['country'],
                 state_province_old=row['state_province'],
                 county_old=row['county'],
                 locality=row['locality'],
                 decimal_longitude=row['decimal_longitude'],
                 decimal_latitude=row['decimal_latitude'],
                 verbatim_longitude=row['verbatim_longitude'],
                 verbatim_latitude=row['verbatim_latitude'],
                 coordinate_precision=row['coordinate_precision'])
