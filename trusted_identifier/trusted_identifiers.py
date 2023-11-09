import pandas as pd

import database as db
from models import TrustedIdentifier, DataSP, DataIdentifiersSelectedGeorge, create_data_trusted_identifier

'''
    To identifier Aline Vieira de Melo Silva was searched data that contains Silva in identified_by column
    To identifier Carmen Lúcia Falcão Ichaso was searched data that contains Ichaso in identified_by column
    ...
'''
#
list_identifiers_selected_by_george = {
    'full_name': ['Aline Vieira de Melo Silva', 'Carmen Lúcia Falcão Ichaso', 'Daniele Monteiro Ferreira',
                  'Daniel Ruschel', 'Elsie Franklin Guimarães', 'Eric J Tepe',
                  'Erika Erika Von Sohsten de Souza Medeiros', 'George Azevedo de Queiroz', 'Micheline Carvalho-Silva',
                  'Ricardo de la Merced Callejas Posada', 'Truman George Yuncker', 'William Trelease'],
    'searched_name': ['Silva', 'Ichaso', 'Monteiro', 'Ruschel', 'Guimar', 'Tepe', 'Medeiros', 'Queiroz', 'Carvalho',
                      'Callejas', 'Yuncker', 'Trelease']
}


def main():
    engine, session = db.connect()

    insert_data_trusted_identifiers(session)

    query = session.query(TrustedIdentifier.value_founded) \
        .filter(TrustedIdentifier.trusted) \
        .distinct() \
        .all()

    list_variations_of_identifiers_trusted = [q.value_founded for q in query]

    count_of_records_with_variations_identifier_name = session.query(DataSP) \
        .filter(DataSP.identified_by.in_(list_variations_of_identifiers_trusted)) \
        .count()

    # this query should return 13182 rows
    print(count_of_records_with_variations_identifier_name)

    insert_data_identifiers_selected_george(list_variations_of_identifiers_trusted, session)

    session.close()
    engine.dispose()


def insert_data_trusted_identifiers(session):
    df = pd.read_csv('trusted_identifier.csv', sep=';', lineterminator='\n')
    n_rows = len(list(df.iterrows()))
    for i, (idx, row) in enumerate(df.iterrows()):
        print('%d/%d', (i, n_rows))
        identifier = TrustedIdentifier(name=row['name'], searched_name=row['searched_name'],
                                       value_founded=row['value_founded'], trusted=row['trusted'])
        try:
            session.add(identifier)
            session.commit()
        except Exception as e:
            print(e)
            session.flush()


def insert_data_identifiers_selected_george(list_variations_of_identifiers_trusted, session):
    count_data_in_data_trusted_identifier = session.query(DataIdentifiersSelectedGeorge).count()
    #
    if count_data_in_data_trusted_identifier == 0:
        query = session.query(DataSP) \
            .filter(DataSP.identified_by.in_(list_variations_of_identifiers_trusted)) \
            .all()

        for i, q in enumerate(query):
            print('%d/%d' % (i, len(query)))
            try:
                new_data_of_identifier_trusted = create_data_trusted_identifier(q)
                session.add(new_data_of_identifier_trusted)
                session.commit()
            except Exception as e:
                print(e)
    count_data_from_trusted_identifers = session.query(DataIdentifiersSelectedGeorge).count()
    # this query should return 13182 rows
    print('count of records in table %s: %d' % (
        DataIdentifiersSelectedGeorge.__tablename__, count_data_from_trusted_identifers))


if __name__ == '__main__':
    main()
