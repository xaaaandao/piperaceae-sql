import logging

import sqlalchemy as sa

from api import get_data_api, get_uf, get_id, get_county_name
from database.models import Local, County, State
from database.sql import is_query_empty, insert
from database.unaccent import unaccent
from local.state import exists_state


def update_county_unencoded_character(session, unencoded_characters):
    for sc in zip(unencoded_characters['invalid'], unencoded_characters['valid']):
        sc_invalid = sc[0]
        sc_valid = sc[1]
        value = sa.func.replace(Local.county_old, sc_invalid, sc_valid)
        try:
            session.query(Local) \
                .update(values={Local.county_old: value}, synchronize_session=False)
            session.commit()
        except Exception as e:
            print(e)
            session.flush()


def update_county_encoded_character(session):
    counties = session.query(County).all()
    for c in counties:
        query = session.query(Local) \
            .filter(sa.or_(Local.county_old.__eq__(c.name),
                           Local.county_old.__eq__(sa.func.lower(c.name)),
                           Local.county_old.__eq__(sa.func.upper(c.name)),
                           Local.county_old.__eq__(unaccent(c.name)),
                           Local.county_old.__eq__(unaccent(sa.func.upper(c.name))),
                           Local.county_old.__eq__(unaccent(sa.func.lower(c.name))))) \
            .all()

        locals_id = [q.id for q in query]
        session.query(Local) \
            .filter(Local.id.in_(locals_id)) \
            .update({Local.county: c.name}, synchronize_session=False)
        session.commit()


def remove_words_county(session):
    invalid_characteres = ['Mun.']
    for char in invalid_characteres:
        value = sa.func.replace(Local.county_old, char, '')
        session.query(Local) \
            .update({Local.county_old: value}, synchronize_session=False)
        session.commit()


def update_county(session, unencoded_characters):
    """
    Essa função é dividida em três partes:
    1- Remoção da substring Mun. da coluna county_old;
    2- Atualiza os caracteres não codificados da coluna county_old;
    3- Procura na tabela api se existe aquela cidade.
    :param session:
    :param unencoded_characters:
    """
    remove_words_county(session)
    update_county_unencoded_character(session, unencoded_characters)
    update_county_encoded_character(session)


def update_county_old_to_county(session):
    """
    Atualiza a coluna api (condado) com o valor que está na coluna antiga (county_old).
    :param session:
    :return:
    """
    query = session.query(County).all()
    counties = [q.name for q in query]
    session.query(Local) \
        .filter(sa.and_(Local.county.__eq__(None),
                        Local.county_old.__ne__(None),
                        Local.county_old.in_(counties))) \
        .update({Local.county: Local.county_old}, synchronize_session=False)
    session.commit()


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

    response = get_data_api()
    counties = [data for i, data in enumerate(response.json())]
    for c in counties:
        uf, state_name, regiao = get_uf(c)
        state = exists_state(session, state_name)

        if not state:
            state = create_state(c)
            insert(state, session)

        county = create_county(c, state)
        insert(county, session)


def create_state(data):
    uf, state, regiao = get_uf(data)
    return State(uf=uf, name=state, region=regiao)


def create_county(json, state):
    return County(id=get_id(json), name=get_county_name(json), state_id=state.id)