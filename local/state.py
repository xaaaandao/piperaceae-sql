import sqlalchemy as sa

from models import State, LocalTrusted, Local
from unaccent import unaccent


def find_state_uf(s, session):
    return session.query(Local) \
        .filter(sa.or_(Local.state_province.__eq__(s.uf),
                       Local.state_province.__eq__(s.uf.lower()))) \
        .all()


def find_state(s, session):
    return session.query(Local) \
        .filter(sa.or_(Local.state_province.__eq__(s.name),
                       Local.state_province.__eq__(s.name.upper()),
                       Local.state_province.__eq__(s.name.lower()),
                       Local.state_province.__eq__(unaccent(s.name)),
                       Local.state_province.__eq__(unaccent(s.name.upper())),
                       Local.state_province.__eq__(unaccent(s.name.lower())))) \
        .all()


def update_state(session, unencoded_characters):
    states = session.query(State) \
        .distinct() \
        .all()

    for s in states:
        update_state_unencoded(session, unencoded_characters)

        query = find_state_uf(s, session)
        locals_id = [q.id for q in query]

        query = find_state(s, session)
        locals_id = locals_id + [q.id for q in query]

        session.query(LocalTrusted) \
            .filter(LocalTrusted.local_id.in_(locals_id)) \
            .update({LocalTrusted.state_province: s.name}, synchronize_session=False)
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
