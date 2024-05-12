import logging

import sqlalchemy
from models import County, DataIdentifiersSelectedGeorge
from unaccent import unaccent


def get_list_uf_state_county(query):
    list_uf = [unaccent(sqlalchemy.func.lower(q.uf)) for q in query]
    list_state = [unaccent(sqlalchemy.func.lower(q.state)) for q in query]
    list_county = [unaccent(sqlalchemy.func.lower(q.county)) for q in query]

    uf_unaccented_lower = unaccent(sqlalchemy.func.lower(DataIdentifiersSelectedGeorge.state_province)).in_(list_uf)
    state_unaccented_lower = unaccent(sqlalchemy.func.lower(DataIdentifiersSelectedGeorge.state_province)).in_(
        list_state)
    county_unaccented_lower = unaccent(sqlalchemy.func.lower(DataIdentifiersSelectedGeorge.county)).in_(list_county)

    return uf_unaccented_lower, state_unaccented_lower, county_unaccented_lower


def update_country(session):
    list_variations_br = ['Brasil', 'BRASIL', 'Brasil/Bolivia', 'Brasilia', 'brazil', 'Brazil', 'BRazil', 'BRAZIL',
                          '[Brésil]', 'Brésil']

    # if count_of_brazil_in_country_trusted == 0:
    records_with_variations_brasil = session.query(DataIdentifiersSelectedGeorge) \
        .filter(DataIdentifiersSelectedGeorge.country.in_(list_variations_br)) \
        .all()

    logging.info('count of records with variations of Brazil: %d' % len(records_with_variations_brasil))

    try:
        session.query(DataIdentifiersSelectedGeorge) \
            .filter(DataIdentifiersSelectedGeorge.country.in_(list_variations_br)) \
            .update({'country_trusted': 'Brasil'}, synchronize_session=False)
        session.commit()
    except Exception:
        session.rollback()


def update_local(session):
    list_unencoded_characters = {
        'error': ['Ã¡', 'Ãº', 'Ã', 'Ã³', 'Ã±', 'Ã©'],
        'correct': ['á', 'ú', 'í', 'ó', 'ñ', 'é']
    }

    update_state_county(list_unencoded_characters, session)
    update_country(session)
    update_country_uf_state_county_brazil(session)


# Se o country_trusted está vazio, e se uf, state ou county está na tabela county set country_trusted="Brasil"
def update_country_uf_state_county_brazil(session):
    query = session.query(County).distinct().all()
    uf_unaccented_lower, state_unaccented_lower, county_unaccented_lower = get_list_uf_state_county(query)
    try:
        session.query(DataIdentifiersSelectedGeorge) \
            .filter(sqlalchemy.and_(DataIdentifiersSelectedGeorge.country_trusted.is_(None),
                                    sqlalchemy.or_(uf_unaccented_lower, state_unaccented_lower),
                                    county_unaccented_lower)) \
            .update({'country_trusted': 'Brasil'}, synchronize_session=False)
        session.commit()
    except Exception:
        session.rollback()
    #
    count_of_brazil_in_country_trusted = session.query(DataIdentifiersSelectedGeorge) \
        .filter(DataIdentifiersSelectedGeorge.country_trusted == 'Brasil') \
        .count()
    logging.info('count of Brasil in country trusted: %d' % count_of_brazil_in_country_trusted)
    assert count_of_brazil_in_country_trusted == 12144


def update_state_county(list_unencoded_characters, session):
    for column in [DataIdentifiersSelectedGeorge.state_province, DataIdentifiersSelectedGeorge.county]:

        list_character_error = list_unencoded_characters['error']
        list_character_correct = list_unencoded_characters['correct']
        for special_character in zip(list_character_error, list_character_correct):
            special_character_to_find = special_character[0]
            special_character_to_replace = special_character[1]
            value = sqlalchemy.func.replace(column, special_character_to_find, special_character_to_replace)
            try:
                session.query(DataIdentifiersSelectedGeorge) \
                    .update(values={column: value}, synchronize_session=False)
                session.commit()
            except Exception:
                session.rollback()
