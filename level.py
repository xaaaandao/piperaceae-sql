import pandas as pd
import sqlalchemy as sa

from database.models import Level
from dataframe import preprocess


def exists_level(row, session):
    return session.query(Level) \
        .filter(sa.and_(Level.genus_old.__eq__(row['genus']),
                        Level.specific_epithet_old.__eq__(row['specific_epithet']),
                        Level.infraspecific_epithet_old.__eq__(row['infraspecific_epithet']),
                        Level.scientific_name_authorship_old.__eq__(row['scientific_name']))) \
        .first()


def create_level(row):
    return Level(kingdom_old=row['kingdom'], phylum_old=row['phylum'],
                 classe_old=row['class'], order_old=row['order'],
                 family_old=row['family'], genus_old=row['genus'],
                 specific_epithet_old=row['specific_epithet'], infraspecific_epithet_old=row['infraspecific_epithet'],
                 scientific_name_old=row['scientific_name'],
                 scientific_name_authorship_old=row['scientific_name_authorship'])


def update_level(session):
    """
    Remove caracteres indesejados de subespécie e nome científico.
    :param session:
    """
    update_infraspecific_epithet(session)
    update_scientific_name_authorship(session)
    update_genus(session)


def update_scientific_name_authorship(session):
    exp = '!| |(|)|.|&'
    value = sa.func.regexp_replace(Level.scientific_name_authorship_old, exp, '')
    session.query(Level) \
        .update({Level.scientific_name_authorship_old: value}, synchronize_session=False)
    session.commit()


def update_infraspecific_epithet(session):
    invalid_characteres = ['f. ', 'var. ']
    for char in invalid_characteres:
        value = sa.func.replace(Level.infraspecific_epithet_old, char, '')
        session.query(Level) \
            .update({Level.infraspecific_epithet_old: value}, synchronize_session=False)
        session.commit()


def update_genus(session):
    # old_genus = [['Sarcorhachis'], ['Ottonia', 'Pothomorphe', 'Potomorphe'], ['Piperomia', 'Peperonia', 'Piperamia']]
    old_genus = [['Sarcorhachis'], ['Ottonia', 'Pothomorphe', 'Potomorphe'], ['Piperomia', 'Peperonia', 'Piperamia']]
    new_genus = ['Manekia', 'Piper', 'Peperomia']

    for g in zip(old_genus, new_genus):
        olds = g[0]
        news = g[1]
        for old in olds:
            session.query(Level) \
                .filter(Level.genus_old.__eq__(old)) \
                .update(values={Level.genus_old: news}, synchronize_session=False)
            session.commit()


def update_level_valid(session, filename='./csv/genus_species.csv'):
    """
    A função carrega o arquivo CSV que contém os nomes (gênero, espécie, subespécie...) antigos e os nomes novos.
    Logo após, é removido os caracteres indesejados.
    Por fim, é procurado no banco se existe alguma espécie com aquele nome antigo.
    Caso postivo, é feita a troca pelo nome mais recente.
    :param session: conexão com o banco de dados.
    :param filename: nome do arquivo CSV com as informações dos nomes.
    """
    df = pd.read_csv(filename, sep=';', index_col=False, header=0, encoding='utf-8')
    df = preprocess(df)

    invalid_characteres = ['f. ', 'var. ']
    for char in invalid_characteres:
        df['infraspecific_epithet'].replace(char, '', inplace=True)
        df['infraspecific_epithet_trusted'].replace(char, '', inplace=True)

    exp = '!| |(|)|.|&'
    df['scientific_name_authorship'].replace(exp, '', regex=True, inplace=True)
    df['scientific_name_authorship_trusted'].replace(exp, '', regex=True, inplace=True)
    df['scientific_name_authorship'].replace('\W+', '', regex=True, inplace=True)
    df['scientific_name_authorship_trusted'].replace('\W+', '', regex=True, inplace=True)

    for idx, row in df.iterrows():
        session.query(Level) \
            .filter(sa.and_(Level.genus_old.__eq__(row['genus']),
                            Level.specific_epithet_old.__eq__(row['specific_epithet']),
                            sa.or_(Level.infraspecific_epithet_old.__eq__(row['infraspecific_epithet']),
                                   Level.scientific_name_authorship_old.__eq__(row['scientific_name_authorship'])))
                    ) \
            .update({Level.genus: row['genus_trusted'],
                     Level.specific_epithet: row['specific_epithet_trusted'],
                     Level.infraspecific_epithet: row['infraspecific_epithet_trusted'],
                     Level.scientific_name_authorship: row['scientific_name_authorship_trusted']},
                    synchronize_session=False)

        session.commit()


def update_level_old_to_level(session):
    session.query(Level) \
        .filter(sa.and_(Level.genus_old.__ne__(None), Level.genus.__eq__(None))) \
        .update({Level.genus: Level.genus_old}, synchronize_session=False)

    session.query(Level) \
        .filter(sa.and_(Level.specific_epithet_old.__ne__(None), Level.specific_epithet.__eq__(None))) \
        .update({Level.specific_epithet: Level.specific_epithet_old}, synchronize_session=False)

    session.query(Level) \
        .filter(sa.and_(Level.infraspecific_epithet_old.__ne__(None), Level.infraspecific_epithet.__eq__(None))) \
        .update({Level.infraspecific_epithet: Level.infraspecific_epithet_old}, synchronize_session=False)

    session.query(Level) \
        .filter(sa.and_(Level.scientific_name_authorship_old.__ne__(None), Level.scientific_name_authorship.__eq__(None))) \
        .update({Level.scientific_name_authorship: Level.scientific_name_authorship_old}, synchronize_session=False)
    session.commit()
