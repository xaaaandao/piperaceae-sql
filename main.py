import os

import numpy
import pandas
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.orm.decl_api
from sqlalchemy.orm import sessionmaker

import Data


def add(session, data):
    try:
        session.add(data)
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)


def insert_data(dataframe, session):
    for row in dataframe.iterrows():
        data = Data.DataSP(seq=row[1]["seq"], modified=row[1]["modified"], institution_code=row[1]["institutionCode"],
                           collection_code=row[1]["collectionCode"], catalog_number=row[1]["catalogNumber"],
                           basis_of_record=row[1]["basisOfRecord"], kingdom=row[1]["kingdom"], phylum=row[1]["phylum"],
                           classe=row[1]["class"], order=row[1]["order"], family=row[1]["family"], genus=row[1]["genus"],
                           specific_epithet=row[1]["specificEpithet"],
                           infraspecific_epithet=row[1]["infraspecificEpithet"],
                           scientific_name=row[1]["scientificName"],
                           scientific_name_authorship=row[1]["scientificNameAuthorship"],
                           identified_by=row[1]["identifiedBy"], year_identified=row[1]["yearIdentified"],
                           month_identified=row[1]["monthIdentified"], day_identified=row[1]["dayIdentified"],
                           type_status=row[1]["typeStatus"],
                           recorded_by=row[1]["recordedBy"], record_number=row[1]["recordNumber"],
                           field_number=row[1]["fieldNumber"], year=row[1]["year"], month=row[1]["month"],
                           day=row[1]["day"], event_time=row[1]["eventTime"],
                           continent_ocean=row[1]["continentOcean"], country=row[1]["country"],
                           state_province=row[1]["stateProvince"], county=row[1]["county"], locality=row[1]["locality"],
                           decimal_longitude=row[1]["decimalLongitude"],
                           decimal_latitude=row[1]["decimalLatitude"], verbatim_longitude=row[1]["verbatimLongitude"],
                           verbatim_latitude=row[1]["verbatimLatitude"],
                           coordinate_precision=row[1]["coordinatePrecision"],
                           bounding_box=row[1]["boundingBox"],
                           minimum_elevation_in_meters=row[1]["minimumElevationInMeters"],
                           maximum_elevation_in_meters=row[1]["maximumElevationInMeters"],
                           minimum_depth_in_meters=row[1]["minimumDepthInMeters"],
                           maximum_depth_in_meters=row[1]["maximumDepthInMeters"], sex=row[1]["sex"],
                           preparation_type=row[1]["preparationType"],
                           individual_count=row[1]["individualCount"],
                           previous_catalog_number=row[1]["previousCatalogNumber"],
                           relationship_type=row[1]["relationshipType"],
                           related_catalog_item=row[1]["relatedCatalogItem"],
                           occurrence_remarks=row[1]["occurrenceRemarks"], barcode=row[1]["barcode"],
                           imagecode=row[1]["imagecode"], geo_flag=row[1]["geoFlag"])

        add(session, data)


def replace_nan_for_none(dataframe):
    return dataframe.replace({numpy.nan: None})


def create_connection_database(cfg):
    engine = sqlalchemy.create_engine(f"postgresql+psycopg2://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['database']}", echo=True)
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    return engine, session


def create_table_if_not_exists(base, database, engine, table_name):
    i = sqlalchemy.inspect(engine)
    if not i.has_table(table_name, schema=database):
        base.metadata.create_all(engine)


def missing_integer(seq):
    l = []
    sx = set(seq)
    for i in range(1, max(seq)):
        if i not in sx:
    # missing_integer = list([i for i in range(min(seq), max(seq)) if i not in set(seq)])
    #
            l.append(i)
    # print(l)
    return l


def main():
    cfg = {
        "user": f"{os.environ['POSTGRE_USER']}",
        "password": f"{os.environ['POSTGRE_PASSWORD']}",
        "host": "192.168.1.6",
        "port": "5432",
        "database": "herbario"
    }

    filename = "original.csv"
    filename_george = "dados-george.csv"
    base = Data.get_base()

    # try:
    engine, session = create_connection_database(cfg)
    engine.connect()

    create_table_if_not_exists(base, cfg["database"], engine, "data")

    try:
        # insert(filename, session)
        # update(filename_george, session)
        seq= [s for s, in session.query(Data.DataSP.seq)]
        
        print(missing_integer(seq))
        # session.commit()
    except FileNotFoundError:
        raise FileNotFoundError(f"file {filename} not found")

    engine.dispose()


def update(filename_george, session):
    dataframe = pandas.read_csv(filename_george, sep=";", low_memory=False)
    for row in dataframe.iterrows():
        if row[1]["GEORGE"].lower() == "sim":
            session.query(Data.DataSP).filter(Data.DataSP.seq == row[1]["seq"]).update({"george": True},
                                                                                       synchronize_session=False)
            session.commit()
        # row[1]["seq"]


def insert(filename, session):
    dataframe = pandas.read_csv(filename, sep=";", low_memory=False)
    dataframe = replace_nan_for_none(dataframe)
    if len(dataframe.index) - 1 > session.query(Data.DataSP).count():
        insert_data(dataframe, session)


if __name__ == '__main__':
    main()
