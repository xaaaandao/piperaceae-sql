import re

import pandas as pd
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

    df = pd.read_csv('../csv/list_genus_species_correct.csv', sep=';', index_col=None, header=0).astype(str)
    df = df.replace('nan', None)

    # below genus level
    df_columns = ['genus', 'specific_epithet', 'infraspecific_epithet', 'scientific_name_authorship', 'genus_trusted', 'specific_epithet_trusted', 'infraspecific_epithet_trusted','scientific_name_authorship_trusted']
    for d in df[df_columns].iterrows():
        columns=[
            DataIdentifiersSelectedGeorge.genus,
            DataIdentifiersSelectedGeorge.specific_epithet,
            sa.func.replace(sa.func.replace(DataIdentifiersSelectedGeorge.infraspecific_epithet, 'f. ', ''), 'var. ', '').label('infraspecific_epithet'),
            sa.func.regexp_replace(DataIdentifiersSelectedGeorge.scientific_name_authorship, '!| |(|)|.|&', '').label('scientific_name_authorship'),
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
        print('infraspecific_epithet (old): %s - (new): %s' % (d[1].infraspecific_epithet, d[1].infraspecific_epithet_trusted))
        print('scientific_name_authorship (old): %s - (new): %s' % (d[1].scientific_name_authorship, d[1].scientific_name_authorship_trusted))

        session.query(DataIdentifiersSelectedGeorge) \
            .filter(sa.and_(DataIdentifiersSelectedGeorge.genus.__eq__(d[1].genus),
                            DataIdentifiersSelectedGeorge.specific_epithet.__eq__(d[1].specific_epithet),
                            sa.or_(sub.c.infraspecific_epithet.__eq__(infraspecific_epithet),
                                   sub.c.scientific_name_authorship.__eq__(scientific_name_authorship)))) \
            .update(values={DataIdentifiersSelectedGeorge.genus_trusted: d[1].genus_trusted,
                            DataIdentifiersSelectedGeorge.specific_epithet_trusted: d[1].specific_epithet_trusted,
                            DataIdentifiersSelectedGeorge.infraspecific_epithet_trusted: d[1].infraspecific_epithet_trusted,
                            DataIdentifiersSelectedGeorge.scientific_name_authorship_trusted: d[1].scientific_name_authorship_trusted}, synchronize_session=False)

        session.commit()

        try:
            query = session.query(DataIdentifiersSelectedGeorge) \
                .filter(sa.or_(DataIdentifiersSelectedGeorge.genus_trusted.is_not(None),
                               DataIdentifiersSelectedGeorge.specific_epithet_trusted.is_not(None),
                               DataIdentifiersSelectedGeorge.infraspecific_epithet_trusted.is_not(None),
                               DataIdentifiersSelectedGeorge.scientific_name_authorship_trusted.is_not(None))) \
                .all()
        except Exception as e:
            print(e)
            session.flush()

        print('records updated in table %s was: %d' % (DataIdentifiersSelectedGeorge.__tablename__, len(query)))

    session.close()
    engine.dispose()


if __name__ == '__main__':
    main()
