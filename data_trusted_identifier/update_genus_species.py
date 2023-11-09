import pandas as pd
import re
import sqlalchemy as sa

import database as db

from models import DataIdentifiersSelectedGeorge

list_unencoded_characters = {
    'error': ['Ã¡', 'Ãº', 'Ã', 'Ã³', 'Ã±', 'Ã©'],
    'correct': ['á', 'ú', 'í', 'ó', 'ñ', 'é']
}

list_variations_br = ['Brasil', 'BRASIL', 'Brasil/Bolivia', 'Brasilia', 'brazil', 'Brazil', 'BRazil', 'BRAZIL',
                      '[Brésil]', 'Brésil']


def main():
    engine, session = db.connect()

    df = pd.read_csv('../csv/list_genus_species_correct.csv', sep=';', index_col=None, header=0).astype(str)
    df = df.replace('nan', None)

    # below genus level
    update_level_below_genus(df, session)
    update_genus_level(session)

    session.close()
    engine.dispose()


def update_level_below_genus(df, session):
    df_columns = ['genus', 'specific_epithet', 'infraspecific_epithet', 'scientific_name_authorship', 'genus_trusted',
                  'specific_epithet_trusted', 'infraspecific_epithet_trusted', 'scientific_name_authorship_trusted']
    for idx, row in df[df_columns].iterrows():
        columns = [
            DataIdentifiersSelectedGeorge.genus,
            DataIdentifiersSelectedGeorge.specific_epithet,
            sa.func.replace(sa.func.replace(DataIdentifiersSelectedGeorge.infraspecific_epithet, 'f. ', ''), 'var. ',
                            '').label('infraspecific_epithet'),
            sa.func.regexp_replace(DataIdentifiersSelectedGeorge.scientific_name_authorship, '!| |(|)|.|&', '').label(
                'scientific_name_authorship'),
        ]
        sub = session.query(*columns).subquery('sub')

        infraspecific_epithet = replace_infraspecific_epithet(row.infraspecific_epithet)

        scientific_name_authorship = replace_scientific_name_authorship(row.scientific_name_authorship)

        print('genus (old): %s - (new): %s' % (row.genus, row.genus_trusted))
        print('specific_epithet (old): %s - (new): %s' % (row.specific_epithet, row.specific_epithet_trusted))
        print('infraspecific_epithet (old): %s - (new): %s' % (
        row.infraspecific_epithet, row.infraspecific_epithet_trusted))
        print('scientific_name_authorship (old): %s - (new): %s' % (
        row.scientific_name_authorship, row.scientific_name_authorship_trusted))

        condition = sa.and_(DataIdentifiersSelectedGeorge.genus.__eq__(row.genus),
                            DataIdentifiersSelectedGeorge.specific_epithet.__eq__(row.specific_epithet),
                            sa.or_(sub.c.infraspecific_epithet.__eq__(infraspecific_epithet),
                                   sub.c.scientific_name_authorship.__eq__(scientific_name_authorship)))

        values_to_update = {DataIdentifiersSelectedGeorge.genus_trusted: row.genus_trusted,
                            DataIdentifiersSelectedGeorge.specific_epithet_trusted: row.specific_epithet_trusted,
                            DataIdentifiersSelectedGeorge.infraspecific_epithet_trusted: row.infraspecific_epithet_trusted,
                            DataIdentifiersSelectedGeorge.scientific_name_authorship_trusted: row.scientific_name_authorship_trusted}

        try:
            session.query(DataIdentifiersSelectedGeorge) \
                .filter(condition) \
                .update(values=values_to_update, synchronize_session=False)

            session.commit()
        except Exception as e:
            print(e)
            session.flush()

        condition = sa.or_(DataIdentifiersSelectedGeorge.genus_trusted.is_not(None),
                           DataIdentifiersSelectedGeorge.specific_epithet_trusted.is_not(None),
                           DataIdentifiersSelectedGeorge.infraspecific_epithet_trusted.is_not(None),
                           DataIdentifiersSelectedGeorge.scientific_name_authorship_trusted.is_not(None))

    query = session.query(DataIdentifiersSelectedGeorge) \
            .filter(condition) \
            .all()

    # this query should return 253 rows
    print('records updated in table %s was: %d' % (DataIdentifiersSelectedGeorge.__tablename__, len(query)))


def replace_scientific_name_authorship(scientific_name_authorship):
    return re.sub('\W+', '', scientific_name_authorship) if scientific_name_authorship else scientific_name_authorship


def replace_infraspecific_epithet(infraspecific_epithet):
    return infraspecific_epithet.replace('f. ', '').replace('var. ',
                                                            '') if infraspecific_epithet else infraspecific_epithet


def update_genus_level(session):
    old_genus = [['Sarcorhachis'], ['Ottonia', 'Pothomorphe'], ['Piperomia', 'Peperonia']]
    new_genus = ['Manekia', 'Piper', 'Peperomia']

    for g in zip(old_genus, new_genus):
        list_old_genus = g[0]
        new_genus = g[1]
        for old in list_old_genus:
            condition = DataIdentifiersSelectedGeorge.genus.__eq__(old)
            values_to_update = {DataIdentifiersSelectedGeorge.genus_trusted: new_genus}
            try:
                session.query(DataIdentifiersSelectedGeorge) \
                    .filter(condition) \
                    .update(values=values_to_update, synchronize_session=False)
                session.commit()
            except Exception as e:
                print(e)
                session.flush()


if __name__ == '__main__':
    main()
