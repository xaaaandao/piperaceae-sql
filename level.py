import logging

import pandas as pd
import sqlalchemy

from models import Level
from sql import insert


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


def update_level(session, filename='./csv/2list_genus_species_correct.csv'):
    df = pd.read_csv(filename, sep=';', index_col=False, header=0)
    for idx, row in df.iterrows():
        pass
