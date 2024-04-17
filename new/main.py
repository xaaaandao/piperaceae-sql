import datetime
import inspect
import logging
import sqlalchemy
import sys

import pandas as pd

from county import api
from data_sp.dataframe import rename_header_dataframe, preprocess
from database import connect
from models import get_base, County, DataSP, TrustedIdentifier, DataTrustedIdentifier, create_data_trusted_identifier

import sys

import sqlalchemy

from database import connect

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


def create_table(base, engine):
    # cls[0] -> name
    # cls[1] -> obj
    classes = [cls for cls in inspect.getmembers(sys.modules['models'], inspect.isclass) if
               'base' not in cls[0].lower()]

    insp = sqlalchemy.inspect(engine)
    tables = insp.get_table_names()
    for c in classes:
        if c[1].__table__.name not in tables:
            table_name = c[1].__table__.name
            base.metadata.tables[table_name].create(bind=engine)
            print('Created table %s' % table_name)


def create_county(json):
    uf, state, regiao = api.get_uf(json)
    return County(id=api.get_id(json), county=api.get_county_name(json), uf=uf, state=state, regiao=regiao)


def insert_counties(base, session):
    response = api.get_data_api()

    count = session.query(County).count()
    if is_query_empty(count):
        for i, county in enumerate(response.json()):
            record = create_county(county)
            try:
                session.add(record)
                session.commit()
            except Exception:
                session.rollback()

    count = session.query(County).count()
    logging.info('count of counties is %d' % count)


def is_query_empty(count):
    return count == 0


def create_datasp(info):
    return DataSP(seq=info['seq'],
                  modified=info['modified'], institution_code=info['institution_code'],
                  collection_code=info['collection_code'], catalog_number=info['catalog_number'],
                  basis_of_record=info['basis_of_record'], kingdom=info['kingdom'], phylum=info['phylum'],
                  classe=info['class'], order=info['order'], family=info['family'],
                  genus=info['genus'],
                  specific_epithet=info['specific_epithet'],
                  infraspecific_epithet=info['infraspecific_epithet'],
                  scientific_name=info['scientific_name'],
                  scientific_name_authorship=info['scientific_name_authorship'],
                  identified_by=info['identified_by'], year_identified=info['year_identified'],
                  month_identified=info['month_identified'], day_identified=info['day_identified'],
                  type_status=info['type_status'],
                  recorded_by=info['recorded_by'], record_number=info['record_number'],
                  field_number=info['field_number'], year=info['year'], month=info['month'],
                  day=info['day'], event_time=info['event_time'],
                  continent_ocean=info['continent_ocean'], country=info['country'],
                  state_province=info['state_province'], county=info['county'], locality=info['locality'],
                  decimal_longitude=info['decimal_longitude'],
                  decimal_latitude=info['decimal_latitude'], verbatim_longitude=info['verbatim_longitude'],
                  verbatim_latitude=info['verbatim_latitude'],
                  coordinate_precision=info['coordinate_precision'],
                  bounding_box=info['bounding_box'],
                  minimum_elevation_in_meters=info['minimum_elevation_in_meters'],
                  maximum_elevation_in_meters=info['maximum_elevation_in_meters'],
                  minimum_depth_in_meters=info['minimum_depth_in_meters'],
                  maximum_depth_in_meters=info['maximum_depth_in_meters'], sex=info['sex'],
                  preparation_type=info['preparation_type'],
                  individual_count=info['individual_count'],
                  previous_catalog_number=info['previous_catalog_number'],
                  relationship_type=info['relationship_type'],
                  related_catalog_item=info['related_catalog_item'],
                  occurrence_remarks=info['occurrence_remarks'], barcode=info['barcode'],
                  imagecode=info['imagecode'], geo_flag=info['geo_flag'])


def insert_specieslink(session):
    filename = '../csv/original.csv'
    df = pd.read_csv(filename, sep=';', low_memory=False, skipinitialspace=True)

    count = session.query(DataSP).count()
    if is_query_empty(count):
        rename_header_dataframe(df)
        df = preprocess(df)
        for row in df.iterrows():
            data_sp = create_datasp(row[1])
            try:
                session.add(data_sp)
                session.commit()
            except Exception:
                session.rollback()

    count = session.query(DataSP).count()
    logging.info('count of specieslink data is %d' % count)

    assert count == 55453


def update_data_selected_george(session):
    filename = '../csv/george_data.csv'
    df = pd.read_csv(filename, sep=';', low_memory=False, skipinitialspace=True)

    count = session.query(DataSP) \
        .filter(DataSP.george) \
        .count()

    if is_query_empty(count):
        for row in df.iterrows():
            get_value_column_george = row[1]['GEORGE']
            if get_value_column_george.lower() == 'sim':
                try:
                    session.query(DataSP) \
                        .filter(DataSP.seq == row[1]['seq']) \
                        .update({'george': True}, synchronize_session=False)
                except Exception:
                    session.rollback()

    count = session.query(DataSP) \
        .filter(DataSP.george) \
        .count()
    logging.info('count of data update is %d' % count)

    assert count == 1419


def update_identifier_name(session):
    list_identifier_trusted = {
        'full_name': ['Aline Vieira de Melo Silva', 'Carmen Lúcia Falcão Ichaso', 'Daniele Monteiro Ferreira',
                      'Daniel Ruschel', 'Elsie Franklin Guimarães', 'Eric J Tepe',
                      'Erika Erika Von Sohsten de Souza Medeiros', 'George Azevedo de Queiroz',
                      'Micheline Carvalho-Silva', 'Ricardo de la Merced Callejas Posada', 'Truman George Yuncker',
                      'William Trelease'],
        'searched_name': ['Silva', 'Ichaso', 'Monteiro', 'Ruschel', 'Guimar', 'Tepe', 'Medeiros', 'Queiroz', 'Carvalho',
                          'Callejas', 'Yuncker', 'Trelease']
    }

    count = session.query(TrustedIdentifier).count()

    if is_query_empty(count):
        full_names = list_identifier_trusted['full_name']
        target_names = list_identifier_trusted['searched_name']
        for item in zip(full_names, target_names):
            full_name_identifier = item[0]
            target = item[1]

            query = session.query(DataSP.identified_by) \
                .filter(DataSP.identified_by.ilike('%{}%'.format(target))) \
                .distinct(DataSP.identified_by) \
                .all()

            for q in query:
                logging.info('full name identifier: %s variation founded: %s' % (full_name_identifier, q.identified_by))
                new_identifier_trusted = TrustedIdentifier(name=full_name_identifier, searched_name=target,
                                                           value_founded=q.identified_by, trusted=False)
                try:
                    session.add(new_identifier_trusted)
                    session.commit()
                except Exception:
                    session.rollback()

    count = session.query(TrustedIdentifier).count()
    logging.info('count identifiers inserted: %d' % count)

    assert count == 340

    count = session.query(TrustedIdentifier.value_founded) \
        .filter(TrustedIdentifier.trusted) \
        .distinct() \
        .count()

    logging.info('count of variations: %d' % count)

    assert count == 187


def insert_data_trusted_identifier(session):
    list_identifier_trusted = {
        'full_name': ['Aline Vieira de Melo Silva', 'Carmen Lúcia Falcão Ichaso', 'Daniele Monteiro Ferreira', 'Daniel Ruschel', 'Elsie Franklin Guimarães', 'Eric J Tepe', 'Erika Erika Von Sohsten de Souza Medeiros', 'George Azevedo de Queiroz', 'Micheline Carvalho-Silva', 'Ricardo de la Merced Callejas Posada', 'Truman George Yuncker', 'William Trelease'],
        'searched_name': ['Silva', 'Ichaso', 'Monteiro', 'Ruschel', 'Guimar', 'Tepe', 'Medeiros', 'Queiroz', 'Carvalho', 'Callejas', 'Yuncker', 'Trelease']
    }

    query = session.query(TrustedIdentifier.value_founded) \
        .filter(TrustedIdentifier.trusted) \
        .distinct() \
        .all()

    list_variations_of_identifiers_trusted = [q.value_founded for q in query]

    count_of_records_with_variations_identifier_name = session.query(DataSP) \
        .filter(DataSP.identified_by.in_(list_variations_of_identifiers_trusted)) \
        .count()

    logging.info('count of records founded with variations of identifier name: %d' % count_of_records_with_variations_identifier_name)

    assert count_of_records_with_variations_identifier_name == 13182

    count_data_in_data_trusted_identifier = session.query(DataTrustedIdentifier).count()

    if count_data_in_data_trusted_identifier == 0:
        query = session.query(DataSP) \
            .filter(DataSP.identified_by.in_(list_variations_of_identifiers_trusted)) \
            .all()

        for i, q in enumerate(query):
            try:
                new_data_of_identifier_trusted = create_data_trusted_identifier(q)
                session.add(new_data_of_identifier_trusted)
                session.commit()
            except Exception as e:
                session.rollback()

    count_data_from_trusted_identifers = session.query(DataTrustedIdentifier).count()
    print('count of records in table %s: %d' % (DataTrustedIdentifier.__tablename__, count_data_from_trusted_identifers))


def main():
    base = get_base()
    engine, session = connect()

    create_table(base, engine)
    insert_counties(base, session)
    insert_specieslink(session)
    update_data_selected_george(session)
    update_identifier_name(session)
    insert_data_trusted_identifier(session)

    engine.dispose()
    session.close()


if __name__ == '__main__':
    main()
