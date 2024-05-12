import datetime
import logging
import re

import pandas as pd
import sqlalchemy

from county import insert_counties
from data_trusted_identifiers import create_data_trusted_identifier, insert_data_trusted_identifier
from george import data_selected_george
from local import update_local
from models import get_base, DataIdentifiersSelectedGeorge, DataSP, TrustedIdentifier, County
from species_link import insert_data_specieslink
from sql import connect, create_table
from unaccent import unaccent

datefmt = '%d-%m-%Y+%H-%M-%S'
dateandtime = datetime.datetime.now().strftime(datefmt)
bold_red = "\x1b[31;1m"
green = "\x1b[32m"
reset = "\x1b[0m"
format = '%(asctime)s [%(module)s - L:%(lineno)d - %(levelname)s] %(message)s'
format_info = green + format + reset
format_error = bold_red + format + reset
logging.basicConfig(format=format_info, datefmt='[%d/%m/%Y %H:%M:%S]', level=logging.INFO)
logging.basicConfig(format=format_error, datefmt='[%d/%m/%Y %H:%M:%S]', level=logging.ERROR)


def update_level(session, filename="./csv/list_genus_species_correct.csv"):
    df = pd.read_csv(filename, sep=';', index_col=None, header=0).astype(str)

    for d in df[['genus', 'specific_epithet', 'infraspecific_epithet', 'scientific_name_authorship', 'genus_trusted',
                 'specific_epithet_trusted', 'infraspecific_epithet_trusted',
                 'scientific_name_authorship_trusted']].iterrows():
        columns = [
            DataIdentifiersSelectedGeorge.genus,
            DataIdentifiersSelectedGeorge.specific_epithet,
            sqlalchemy.func.replace(
                sqlalchemy.func.replace(DataIdentifiersSelectedGeorge.infraspecific_epithet, 'f. ', ''), 'var. ',
                '').label('infraspecific_epithet'),
            sqlalchemy.func.regexp_replace(DataIdentifiersSelectedGeorge.scientific_name_authorship, '!| |(|)|.|&',
                                           '').label('scientific_name_authorship'),
        ]
        sub = session.query(*columns).subquery('sub')

        infraspecific_epithet = d[1].infraspecific_epithet
        if infraspecific_epithet:
            infraspecific_epithet = infraspecific_epithet.replace('f. ', '').replace('var. ', '')

        scientific_name_authorship = d[1].scientific_name_authorship
        if scientific_name_authorship:
            scientific_name_authorship = re.sub('\W+', '', scientific_name_authorship)

        print('genus (old): %s - (new): %s' % (d[1].genus, d[1].genus_trusted))
        print('specific_epithet (old): %s - (new): %s' % (d[1].specific_epithet, d[1].specific_epithet_trusted))
        print('infraspecific_epithet (old): %s - (new): %s' % (
            d[1].infraspecific_epithet, d[1].infraspecific_epithet_trusted))
        print('scientific_name_authorship (old): %s - (new): %s' % (
            d[1].scientific_name_authorship, d[1].scientific_name_authorship_trusted))

        try:
            session.query(DataIdentifiersSelectedGeorge) \
                .filter(sqlalchemy.and_(DataIdentifiersSelectedGeorge.genus.__eq__(d[1].genus),
                                        DataIdentifiersSelectedGeorge.specific_epithet.__eq__(d[1].specific_epithet),
                                        sqlalchemy.or_(sub.c.infraspecific_epithet.__eq__(infraspecific_epithet),
                                                       sub.c.scientific_name_authorship.__eq__(
                                                           scientific_name_authorship)))) \
                .update(values={DataIdentifiersSelectedGeorge.genus_trusted: d[1].genus_trusted,
                                DataIdentifiersSelectedGeorge.specific_epithet_trusted: d[1].specific_epithet_trusted,
                                DataIdentifiersSelectedGeorge.infraspecific_epithet_trusted: d[
                                    1].infraspecific_epithet_trusted,
                                DataIdentifiersSelectedGeorge.scientific_name_authorship_trusted: d[
                                    1].scientific_name_authorship_trusted}, synchronize_session=False)

            session.commit()
        except Exception as e:
            session.rollback()

    # update_genus(session)
    #
    # query = session.query(DataIdentifiersSelectedGeorge) \
    #     .filter(sqlalchemy.or_(DataIdentifiersSelectedGeorge.genus_trusted.is_not(None),
    #                            DataIdentifiersSelectedGeorge.specific_epithet_trusted.is_not(None),
    #                            DataIdentifiersSelectedGeorge.infraspecific_epithet_trusted.is_not(None),
    #                            DataIdentifiersSelectedGeorge.scientific_name_authorship_trusted.is_not(None))) \
    #     .all()
    #
    # logging.info('records updated in table %s was: %d' % (DataIdentifiersSelectedGeorge.__tablename__, len(query)))


def update_genus(session):
    old_genus = [['Sarcorhachis'], ['Ottonia', 'Pothomorphe'], ['Piperomia', 'Peperonia']]
    new_genus = ['Manekia', 'Piper', 'Peperomia']
    for g in zip(old_genus, new_genus):
        list_old_genus = g[0]
        new = g[1]
        for old in list_old_genus:
            session.query(DataIdentifiersSelectedGeorge) \
                .filter(DataIdentifiersSelectedGeorge.genus.__eq__(old)) \
                .update(values={DataIdentifiersSelectedGeorge.genus_trusted: new}, synchronize_session=False)
            session.commit()


def get_state_uf_county(query):
    list_uf = [unaccent(sqlalchemy.func.lower(q.uf)) for q in query]
    list_state = [unaccent(sqlalchemy.func.lower(q.state)) for q in query]
    list_county = [unaccent(sqlalchemy.func.lower(q.county)) for q in query]
    uf_unaccented_lower = unaccent(sqlalchemy.func.lower(DataIdentifiersSelectedGeorge.state_province)).in_(list_uf)
    state_unaccented_lower = unaccent(sqlalchemy.func.lower(DataIdentifiersSelectedGeorge.state_province)).in_(
        list_state)
    county_unaccented_lower = unaccent(sqlalchemy.func.lower(DataIdentifiersSelectedGeorge.county)).in_(list_county)

    return state_unaccented_lower, uf_unaccented_lower, county_unaccented_lower


def get_records_group_by_level(condition, level, minimum_image, session):
    columns = [level,
               sqlalchemy.func.array_agg(DataIdentifiersSelectedGeorge.seq).label('list_seq')]
    query = session.query(*columns) \
        .filter(condition) \
        .distinct() \
        .group_by(level) \
        .order_by(level) \
        .having(sqlalchemy.func.count(level) >= minimum_image) \
        .all()
    return query


def get_dataset_br(session):
    level = DataIdentifiersSelectedGeorge.specific_epithet_trusted
    query = session.query(County).distinct().all()
    state_unaccented_lower, uf_unaccented_lower, county_unaccented_lower = get_state_uf_county(query)

    condition = sqlalchemy.and_(DataIdentifiersSelectedGeorge.country_trusted.__eq__('Brasil'),
                                level.is_not(None),
                                sqlalchemy.or_(uf_unaccented_lower, state_unaccented_lower))

    query = get_records_group_by_level(condition, level, 5, session)

    list_seq_final = []
    for q in query:
        # print()
        list_seq_final = list_seq_final + q.list_seq

    print('-----------------> %d', len(list_seq_final))


def main():
    engine, session = connect(echo=False, database='herbario4')
    base = get_base()

    create_table(base, engine)
    insert_counties(session)
    insert_data_specieslink(session)
    data_selected_george(session)
    # insert and update trusted identifier.sql
    insert_data_trusted_identifier(session)
    update_local(session)
    update_level(session)

    # get_dataset_br(session)

    engine.dispose()
    session.close()


if __name__ == '__main__':
    main()
