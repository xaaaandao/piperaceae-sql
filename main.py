import database
from county.insert_county import insert_counties
from create_table import create_tables
from data_george.data_selected_by_george import set_george_data
from data_sp.insert_metadata import insert_csv_sp
from trusted_identifier.trusted_identifiers import insert_trusted_identifiers


def main():
    engine, session = database.connect()

    create_tables(engine)
    insert_csv_sp(session)
    set_george_data(session)
    insert_counties(session)
    insert_trusted_identifiers(session)

    session.close()
    engine.dispose()


if __name__ == '__main__':
    main()
