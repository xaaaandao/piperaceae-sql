import logging

import pandas as pd
import sqlalchemy
import sqlalchemy as sa

from models import Level, LevelValid, exsiccata_level
from sql import insert, is_query_empty


def exists_level(data, session):
    return session.query(Level) \
        .filter(sqlalchemy.and_(Level.kingdom.__eq__(data['kingdom']),
                                Level.phylum.__eq__(data['phylum']),
                                Level.classe.__eq__(data['class']),
                                Level.order.__eq__(data['order']),
                                Level.family.__eq__(data['family']),
                                Level.genus.__eq__(data['genus']),
                                Level.specific_epithet.__eq__(data['specific_epithet']),
                                Level.infraspecific_epithet.__eq__(data['infraspecific_epithet']),
                                Level.scientific_name.__eq__(data['scientific_name']),
                                Level.scientific_name_authorship.__eq__(data['scientific_name_authorship']))).first()


def create_level(data):
    return Level(kingdom=data['kingdom'], phylum=data['phylum'], classe=data['class'], order=data['order'],
                 family=data['family'], genus=data['genus'], specific_epithet=data['specific_epithet'],
                 infraspecific_epithet=data['infraspecific_epithet'], scientific_name=data['scientific_name'],
                 scientific_name_authorship=data['scientific_name_authorship'])


def insert_level(data, session):
    l = exists_level(data, session)
    if not l:
        level = create_level(data)
        insert(level, session)
        return level

    return l


def insert_level_valid(session, filename='./csv/2list_genus_species_correct.csv'):
    count = session.query(LevelValid).count()
    if not is_query_empty(count):
        logging.info('count level valid is %d', count)
        return count

    df = pd.read_csv(filename, sep=';', index_col=False, header=0, encoding='utf-8')
    for idx, row in df.iterrows():
        level = session.query(Level) \
            .filter(sa.and_(Level.genus.__eq__(row['genus']),
                            Level.specific_epithet.__eq__(row['specific_epithet']),
                            sa.or_(Level.infraspecific_epithet.__eq__(row['infraspecific_epithet'].replace('f. ', '')),
                                   Level.scientific_name.__eq__(row['scientific_name_authorship_trusted']))))

        if level:
            l = LevelValid(kingdom=row['kingdom_trusted'], phylum=row['phylum_trusted'], order=row['order_trusted'],
                           classe=row['classe_trusted'],
                           family=row['family_trusted'], genus=row['genus_trusted'],
                           specific_epithet=row['specific_epithet_trusted'],
                           infraspecific_epithet=row['infraspecific_epithet_trusted'],
                           scientific_name_authorship=row['scientific_name_authorship_trusted'],
                           level_id=level.id)
            insert(l, session)


def update_level_valid(session):
    remove_string_infraspecific_epithet(session)
    remove_char_scientific_name_authorship(session)


def remove_string_infraspecific_epithet(session):
    invalid_characteres = ['f. ']  # , 'var. ']
    for column in [LevelValid.infraspecific_epithet, LevelValid.infraspecific_epithet_valid]:
        for char in invalid_characteres:
            value = sa.func.replace(column, char, '')
            session.query(LevelValid) \
                .update({column: value}, synchronize_session=False)
            session.commit()

    for char in invalid_characteres:
        value = sa.func.replace(Level.infraspecific_epithet, char, '')
        session.query(Level) \
            .update({Level.infraspecific_epithet: value}, synchronize_session=False)
        session.commit()


def remove_char_scientific_name_authorship(session):
    exp = '!| |(|)|.|&'
    for column in [LevelValid.scientific_name_authorship, LevelValid.scientific_name_authorship_valid]:
        value = sa.func.regexp_replace(column, exp, '')
        session.query(LevelValid) \
            .update({column: value}, synchronize_session=False)
        session.commit()

    value = sa.func.regexp_replace(Level.scientific_name_authorship, exp, '')
    session.query(Level) \
        .update({Level.scientific_name_authorship: value}, synchronize_session=False)
    session.commit()
