import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm


def connect(cfg):
    list_hosts = ("192.168.0.160", "localhost")
    for host in list_hosts:
        try:
            engine = sqlalchemy.create_engine(f"postgresql+psycopg2://{cfg['user']}:{cfg['password']}@{host}:{cfg['port']}/{cfg['database']}", echo=True, pool_pre_ping=True)
            Session = sqlalchemy.orm.sessionmaker(bind=engine)
            Session.configure(bind=engine)
            session = Session()
            if engine.connect():
                return engine, session
        except Exception as e:
            print(f"problems with host {host} ({e})")


def make_operation(session):
    try:
        session.commit()
        session.flush()
    except Exception as e:
        session.rollback()
        print(e)
        raise
    finally:
        session.close()


def create_table_if_not_exists(cfg, engine, table_name):
    if not sqlalchemy.inspect(engine).has_table(table_name, schema=cfg["database"]):
        Base.metadata.create_all(engine)


def create_datasp(info):
    return DataSP(seq=info["seq"],
                  modified=info["modified"], institution_code=info["institutionCode"],
                  collection_code=info["collectionCode"], catalog_number=info["catalogNumber"],
                  basis_of_record=info["basisOfRecord"], kingdom=info["kingdom"], phylum=info["phylum"],
                  classe=info["class"], order=info["order"], family=info["family"],
                  genus=info["genus"],
                  specific_epithet=info["specificEpithet"],
                  infraspecific_epithet=info["infraspecificEpithet"],
                  scientific_name=info["scientificName"],
                  scientific_name_authorship=info["scientificNameAuthorship"],
                  identified_by=info["identifiedBy"], year_identified=info["yearIdentified"],
                  month_identified=info["monthIdentified"], day_identified=info["dayIdentified"],
                  type_status=info["typeStatus"],
                  recorded_by=info["recordedBy"], record_number=info["recordNumber"],
                  field_number=info["fieldNumber"], year=info["year"], month=info["month"],
                  day=info["day"], event_time=info["eventTime"],
                  continent_ocean=info["continentOcean"], country=info["country"],
                  state_province=info["stateProvince"], county=info["county"], locality=info["locality"],
                  decimal_longitude=info["decimalLongitude"],
                  decimal_latitude=info["decimalLatitude"], verbatim_longitude=info["verbatimLongitude"],
                  verbatim_latitude=info["verbatimLatitude"],
                  coordinate_precision=info["coordinatePrecision"],
                  bounding_box=info["boundingBox"],
                  minimum_elevation_in_meters=info["minimumElevationInMeters"],
                  maximum_elevation_in_meters=info["maximumElevationInMeters"],
                  minimum_depth_in_meters=info["minimumDepthInMeters"],
                  maximum_depth_in_meters=info["maximumDepthInMeters"], sex=info["sex"],
                  preparation_type=info["preparationType"],
                  individual_count=info["individualCount"],
                  previous_catalog_number=info["previousCatalogNumber"],
                  relationship_type=info["relationshipType"],
                  related_catalog_item=info["relatedCatalogItem"],
                  occurrence_remarks=info["occurrenceRemarks"], barcode=info["barcode"],
                  imagecode=info["imagecode"], geo_flag=info["geoFlag"])


def get_key(json, key):
    if key in json:
        return json[key]
    raise KeyError(f"key {key} not found")


def get_id(json):
    if "id" in json:
        return json["id"]
    raise KeyError(f"key id not found")


def get_county_name(json):
    if "nome" in json:
        return json["nome"]
    raise KeyError(f"key nome not found")


def get_uf(json):
    if "microrregiao" in json:
        if "mesorregiao" in json["microrregiao"]:
            if "UF" in json["microrregiao"]["mesorregiao"]:
                return json["microrregiao"]["mesorregiao"]["UF"]["sigla"], json["microrregiao"]["mesorregiao"]["UF"]["nome"]
            raise KeyError("key UF not found")
        raise KeyError("key mesorregiao not found")
    raise KeyError("key microrregiao not found")


def create_county(json):
    uf, uf_name = get_uf(json)
    return County(id=get_id(json), county=get_county_name(json), uf=uf, uf_name=uf_name)


Base = sqlalchemy.ext.declarative.declarative_base()


class DataSP(Base):
    __tablename__ = "data"

    seq = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    modified = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    institution_code = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    collection_code = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    catalog_number = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    basis_of_record = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    kingdom = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    phylum = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    classe = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    order = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    family = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    genus = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    specific_epithet = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    infraspecific_epithet = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    scientific_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    scientific_name_authorship = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    identified_by = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    year_identified = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    month_identified = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    day_identified = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    type_status = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    recorded_by = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    record_number = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    field_number = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    year = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=True)
    month = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=True)
    day = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=True)
    event_time = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    continent_ocean = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    country = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    state_province = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    county = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    locality = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    decimal_longitude = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    decimal_latitude = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    verbatim_longitude = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    verbatim_latitude = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    coordinate_precision = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    bounding_box = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    minimum_elevation_in_meters = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=True)
    maximum_elevation_in_meters = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=True)
    minimum_depth_in_meters = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=True)
    maximum_depth_in_meters = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=True)
    sex = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    preparation_type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    individual_count = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=True)
    previous_catalog_number = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    relationship_type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    related_catalog_item = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    occurrence_remarks = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    barcode = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    imagecode = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    geo_flag = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    george = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    my_country = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    my_state = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    my_city = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return "DataSP(seq=%s, modified=%s, institution_code=%s, collection_code=%s, catalog_number=%s, " \
               "basis_of_record=%s, kingdom=%s, phylum=%s, classe=%s, order=%s, family=%s, genus=%s, " \
               "specific_epithet=%s, infraspecific_epithet=%s, scientific_name=%s, scientific_name_authorship=%s, " \
               "identified_by=%s, year_identified=%s, month_identified=%s, day_identified=%s, type_status=%s, " \
               "recorded_by=%s, record_number=%s, field_number=%s, year=%s, month=%s, day=%s, event_time=%s, " \
               "continent_ocean=%s, country=%s, state_province=%s, county=%s, locality=%s, decimal_longitude=%s, " \
               "decimal_latitude=%s, verbatim_longitude=%s, verbatim_latitude=%s, coordinate_precision=%s, " \
               "bounding_box=%s, minimum_elevation_in_meters=%s, maximum_elevation_in_meters=%s, " \
               "minimum_depth_in_meters=%s, maximum_depth_in_meters=%s, sex=%s, preparation_type=%s, " \
               "individual_count=%s, previous_catalog_number=%s, relationship_type=%s, related_catalog_item=%s, " \
               "occurrence_remarks=%s, barcode=%s, imagecode=%s, geo_flag=%s)"


# County is muncipio, condado
class County(Base):
    __tablename__ = "county"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    county = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    uf = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    uf_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return "County(id=%s, county=%s, county_normalized=%s, uf=%s, uf_normalized=%s, uf_name=%s, uf_name_normalized=%s)"




