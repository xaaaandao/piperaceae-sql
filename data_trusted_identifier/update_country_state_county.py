import sqlalchemy as sa

import database as db
from models import DataIdentifiersSelectedGeorge

list_unencoded_characters = {
    'error': ['Ã¡', 'Ãº', 'Ã', 'Ã³', 'Ã±', 'Ã©'],
    'correct': ['á', 'ú', 'í', 'ó', 'ñ', 'é']
}

list_variations_br = ['Brasil', 'BRASIL', 'Brasil/Bolivia', 'Brasilia', 'brazil', 'Brazil', 'BRazil', 'BRAZIL', '[Brésil]', 'Brésil']


def main():
    engine, session = db.connect()

    replace_uneconded_character(session)
    update_column_country(session)

    # check
    # count_of_brazil_in_country_trusted = session.query(DataIdentifiersSelectedGeorge) \
    #     .filter(DataIdentifiersSelectedGeorge.country_trusted == 'Brasil') \
    #     .count()
    #
    # # this query should return 12144
    # print('count of Brasil in country trusted: %d' % count_of_brazil_in_country_trusted)

    session.close()
    engine.dispose()


def update_column_country(session):
    count_of_brazil_in_country_trusted = session.query(DataIdentifiersSelectedGeorge) \
        .filter(DataIdentifiersSelectedGeorge.country_trusted == 'Brasil') \
        .count()

    if count_of_brazil_in_country_trusted == 0:
        records_with_variations_brasil = session.query(DataIdentifiersSelectedGeorge) \
            .filter(DataIdentifiersSelectedGeorge.country.in_(list_variations_br)) \
            .all()

        # this query should return 11206 rows
        print('count of records with variations of Brazil: %d' % len(records_with_variations_brasil))

        try:
            session.query(DataIdentifiersSelectedGeorge) \
                .filter(DataIdentifiersSelectedGeorge.country.in_(list_variations_br)) \
                .update({'country_trusted': 'Brasil'}, synchronize_session=False)
            session.commit()
        except Exception as e:
            print(e)
            session.flush()


def replace_uneconded_character(session):
    for column in [DataIdentifiersSelectedGeorge.state_province, DataIdentifiersSelectedGeorge.county]:
        list_character_error = list_unencoded_characters['error']
        list_character_correct = list_unencoded_characters['correct']
        for special_character in zip(list_character_error, list_character_correct):
            special_character_to_find = special_character[0]
            special_character_to_replace = special_character[1]
            value = sa.func.replace(column, special_character_to_find, special_character_to_replace)
            try:
                session.query(DataIdentifiersSelectedGeorge) \
                    .update(values={column: value}, synchronize_session=False)
                session.commit()
            except Exception as e:
                print(e)
                session.flush()


if __name__ == '__main__':
    main()
