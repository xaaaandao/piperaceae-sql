import sqlalchemy as sa

from database.models import Local, State
from database.unaccent import unaccent


def find_state(session, state):
    return session.query(Local) \
        .filter(sa.or_(Local.state_province.__eq__(state.uf),
                       sa.func.lower(Local.state_province).__eq__(sa.func.lower(state.uf)),
                       Local.state_province.__eq__(state.name),
                       sa.func.upper(Local.state_province).__eq__(sa.func.upper(state.name)),
                       sa.func.lower(Local.state_province).__eq__(sa.func.lower(state.name)),
                       unaccent(Local.state_province).__eq__(unaccent(state.name)),
                       unaccent(sa.func.upper(Local.state_province)).__eq__(unaccent(sa.func.upper(state.name))),
                       unaccent(sa.func.lower(Local.state_province)).__eq__(unaccent(sa.func.lower(state.name))))) \
        .all()


def update_state(session, unencoded_characters):
    """
    A função atualiza os valores que contêm caracteres não codificados. Logo após,
    retorna todos os registros que contêm em state_province_old o nome completo do estado ou abreviação.
    No final, atualiza a coluna state_province com o valor correto.
    :param session:
    :param unencoded_characters:
    """
    states = session.query(State) \
        .distinct() \
        .all()

    update_state_unencoded(session, unencoded_characters)
    for state in states:
        query = find_state(session, state)
        locals_id = [q.id for q in query]

        session.query(Local) \
            .filter(Local.id.in_(locals_id)) \
            .update({Local.state_province: state.name}, synchronize_session=False)

        session.commit()


def update_state_unencoded(session, unencoded_characters):
    for sc in zip(unencoded_characters['invalid'], unencoded_characters['valid']):
        sc_invalid = sc[0]
        sc_valid = sc[1]
        value = sa.func.replace(Local.state_province, sc_invalid, sc_valid)
        try:
            session.query(Local) \
                .update(values={Local.state_province: value}, synchronize_session=False)
            session.commit()
        except Exception as e:
            print(e)
            session.flush()


def exists_state(session, state):
    return session.query(State).filter(State.name.__eq__(state)).first()
