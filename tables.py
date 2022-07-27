import sqlalchemy
import sqlalchemy.ext.declarative

Base = sqlalchemy.ext.declarative.declarative_base()


def create_tsvector(*args):
    field, weight = args[0]
    exp = sqlalchemy.func.setweight(sqlalchemy.func.to_tsvector('portuguese', field), weight)
    for field, weight in args[1:]:
        exp = sqlalchemy.sql.operators.op(exp, '||', sqlalchemy.func.setweight(sqlalchemy.func.to_tsvector('portuguese', field), weight))
    print(exp)
    return exp


def create_datasp(info):
    return DataSP(seq=info["seq"],
                  modified=info["modified"], institution_code=info["institution_code"],
                  collection_code=info["collection_code"], catalog_number=info["catalog_number"],
                  basis_of_record=info["basis_of_record"], kingdom=info["kingdom"], phylum=info["phylum"],
                  classe=info["class"], order=info["order"], family=info["family"],
                  genus=info["genus"],
                  specific_epithet=info["specific_epithet"],
                  infraspecific_epithet=info["infraspecific_epithet"],
                  scientific_name=info["scientific_name"],
                  scientific_name_authorship=info["scientific_name_authorship"],
                  identified_by=info["identified_by"], year_identified=info["year_identified"],
                  month_identified=info["month_identified"], day_identified=info["day_identified"],
                  type_status=info["type_status"],
                  recorded_by=info["recorded_by"], record_number=info["record_number"],
                  field_number=info["field_number"], year=info["year"], month=info["month"],
                  day=info["day"], event_time=info["event_time"],
                  continent_ocean=info["continent_ocean"], country=info["country"],
                  state_province=info["state_province"], county=info["county"], locality=info["locality"],
                  decimal_longitude=info["decimal_longitude"],
                  decimal_latitude=info["decimal_latitude"], verbatim_longitude=info["verbatim_longitude"],
                  verbatim_latitude=info["verbatim_latitude"],
                  coordinate_precision=info["coordinate_precision"],
                  bounding_box=info["bounding_box"],
                  minimum_elevation_in_meters=info["minimum_elevation_in_meters"],
                  maximum_elevation_in_meters=info["maximum_elevation_in_meters"],
                  minimum_depth_in_meters=info["minimum_depth_in_meters"],
                  maximum_depth_in_meters=info["maximum_depth_in_meters"], sex=info["sex"],
                  preparation_type=info["preparation_type"],
                  individual_count=info["individual_count"],
                  previous_catalog_number=info["previous_catalog_number"],
                  relationship_type=info["relationship_type"],
                  related_catalog_item=info["related_catalog_item"],
                  occurrence_remarks=info["occurrence_remarks"], barcode=info["barcode"],
                  imagecode=info["imagecode"], geo_flag=info["geo_flag"])


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
                return json["microrregiao"]["mesorregiao"]["UF"]["sigla"], json["microrregiao"]["mesorregiao"]["UF"][
                    "nome"]
            raise KeyError("key UF not found")
        raise KeyError("key mesorregiao not found")
    raise KeyError("key microrregiao not found")


def create_county(json):
    uf, uf_name = get_uf(json)
    return County(id=get_id(json), county=get_county_name(json), uf=uf, uf_name=uf_name)


def get_base():
    return Base


class DataSP(Base):
    __tablename__ = "data"

    seq = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    modified = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    institution_code = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    collection_code = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    catalog_number = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    basis_of_record = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    kingdom = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    phylum = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    classe = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    order = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    family = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    genus = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    specific_epithet = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    infraspecific_epithet = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    scientific_name = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    scientific_name_authorship = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    identified_by = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    year_identified = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    month_identified = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    day_identified = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    type_status = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    recorded_by = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    record_number = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    field_number = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    year = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=True)
    month = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=True)
    day = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=True)
    event_time = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    continent_ocean = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    country = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    state_province = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    county = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    locality = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    decimal_longitude = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    decimal_latitude = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    verbatim_longitude = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    verbatim_latitude = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    coordinate_precision = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    bounding_box = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    minimum_elevation_in_meters = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=True)
    maximum_elevation_in_meters = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=True)
    minimum_depth_in_meters = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=True)
    maximum_depth_in_meters = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=True)
    sex = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    preparation_type = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    individual_count = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=True)
    previous_catalog_number = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    relationship_type = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    related_catalog_item = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    occurrence_remarks = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    barcode = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    imagecode = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    geo_flag = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    george = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    my_country = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    my_state = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    my_city = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)

    # 1#
    __ts_vector__ = create_tsvector(
        (county, 'A'),
        (state_province, 'B')
    )

    __table_args__ = (
        sqlalchemy.Index('my_index', __ts_vector__, postgresql_using='gin'),
    )

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
    county = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    uf = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    uf_name = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)

    def __repr__(self):
        return "County(id=%s, county=%s, county_normalized=%s, uf=%s, uf_normalized=%s, uf_name=%s, uf_name_normalized=%s)"