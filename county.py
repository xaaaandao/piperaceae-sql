import logging

import api
from models import County, State
from sql import insert, is_query_empty


def insert_counties(session):
    response = api.get_data_api()

    count = session.query(County).count()
    if is_query_empty(count):
        counties = [data for i, data in enumerate(response.json())]
        for c in counties:
            uf, state, regiao = api.get_uf(c)
            s = session.query(State).filter(State.name.__eq__(state)).all()
            if s:
                county = create_county(c, s[0])
                insert(county, session)
            else:
                s = create_state(c)
                insert(s, session)
                county = create_county(c, s)
                insert(county, session)

    count_counties = session.query(County).count()
    logging.info('count of counties is %d' % count_counties)
    assert count_counties == 5570

    count_states = session.query(State).count()
    logging.info('count of states is %d' % count_states)
    assert count_states == 27


def create_state(data):
    uf, state, regiao = api.get_uf(data)
    return State(uf=uf, name=state, region=regiao)


def create_county(json, state):
    return County(id=api.get_id(json), name=api.get_county_name(json), state_id=state.id)
