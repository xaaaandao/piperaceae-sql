import sqlalchemy as sa

from database.models import Local, County
from database.unaccent import unaccent


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
    3- Procura na tabela county se existe aquela cidade.
    :param session:
    :param unencoded_characters:
    """
    remove_words_county(session)
    update_county_unencoded_character(session, unencoded_characters)
    update_county_encoded_character(session)


def update_county_old_to_county(session):
    """
    Atualiza a coluna county (condado) com o valor que está na coluna antiga (county_old).
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
