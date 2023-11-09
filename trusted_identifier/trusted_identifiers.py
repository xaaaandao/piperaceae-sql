import database as db


'''
    To identifier Aline Vieira de Melo Silva was searched data that contains Silva in identified_by column
    To identifier Carmen Lúcia Falcão Ichaso was searched data that contains Ichaso in identified_by column
    ...
'''
#
list_identifiers_selected_by_george = {
    'full_name': ['Aline Vieira de Melo Silva', 'Carmen Lúcia Falcão Ichaso', 'Daniele Monteiro Ferreira', 'Daniel Ruschel', 'Elsie Franklin Guimarães', 'Eric J Tepe', 'Erika Erika Von Sohsten de Souza Medeiros', 'George Azevedo de Queiroz', 'Micheline Carvalho-Silva', 'Ricardo de la Merced Callejas Posada', 'Truman George Yuncker', 'William Trelease'],
    'searched_name': ['Silva', 'Ichaso', 'Monteiro', 'Ruschel', 'Guimar', 'Tepe', 'Medeiros', 'Queiroz', 'Carvalho', 'Callejas', 'Yuncker', 'Trelease']
}


def main():
    engine, session = db.connect()

    # query = session.query(TrustedIdentifier.value_founded) \
    #     .filter(TrustedIdentifier.trusted) \
    #     .distinct() \
    #     .all()
    #
    # list_variations_of_identifiers_trusted = [q.value_founded for q in query]
    #
    # count_of_records_with_variations_identifier_name = session.query(DataSP) \
    #     .filter(DataSP.identified_by.in_(list_variations_of_identifiers_trusted)) \
    #     .count()



    session.close()
    engine.dispose()


if __name__ == '__main__':
    main()
