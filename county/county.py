import logging

import api
from database.models import County, State
from database.sql import insert, is_query_empty


def exists_state(session, state):
    return session.query(State).filter(State.name.__eq__(state)).first()


def insert_counties(session):
    """
    Primeiramente, verifica-se o estado já está cadastrado.
    Caso positivo, pega o id do estado e adiciona a cidade.
    Caso negativo, adiciona o estado e logo após adiciona a cidade.
    :param session: conexão com banco de dados.
    :return:
    """
    count_counties = session.query(County).count()

    count_states = session.query(State).count()
    if not is_query_empty(count_counties) and not is_query_empty(count_states):
        logging.info('count of counties is %d and states is %d' % (count_counties, count_states))
        assert count_counties == 5570 and count_states == 27
        return

    response = api.get_data_api()
    counties = [data for i, data in enumerate(response.json())]
    for c in counties:
        uf, state_name, regiao = api.get_uf(c)
        state = exists_state(session, state_name)

        if not state:
            state = create_state(c)
            insert(state, session)

        county = create_county(c, state)
        insert(county, session)


def create_state(data):
    uf, state, regiao = api.get_uf(data)
    return State(uf=uf, name=state, region=regiao)


def create_county(json, state):
    return County(id=api.get_id(json), name=api.get_county_name(json), state_id=state.id)
