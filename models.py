import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

Base = sqlalchemy.ext.declarative.declarative_base()


# def create_data_trusted_identifier(info):
#     return DataIdentifiersSelectedGeorge(seq=info.seq,
#                                          modified=info.modified, institution_code=info.institution_code,
#                                          collection_code=info.collection_code, catalog_number=info.catalog_number,
#                                          basis_of_record=info.basis_of_record, kingdom=info.kingdom, phylum=info.phylum,
#                                          classe=info.classe, order=info.order, family=info.family,
#                                          genus=info.genus,
#                                          specific_epithet=info.specific_epithet,
#                                          infraspecific_epithet=info.infraspecific_epithet,
#                                          scientific_name=info.scientific_name,
#                                          scientific_name_authorship=info.scientific_name_authorship,
#                                          identified_by=info.identified_by, year_identified=info.year_identified,
#                                          month_identified=info.month_identified, day_identified=info.day_identified,
#                                          type_status=info.type_status,
#                                          recorded_by=info.recorded_by, record_number=info.record_number,
#                                          field_number=info.field_number, year=info.year, month=info.month,
#                                          day=info.day, event_time=info.event_time,
#                                          continent_ocean=info.continent_ocean, country=info.country,
#                                          state_province=info.state_province, ibge=info.ibge, locality=info.locality,
#                                          decimal_longitude=info.decimal_longitude,
#                                          decimal_latitude=info.decimal_latitude, verbatim_longitude=info.verbatim_longitude,
#                                          verbatim_latitude=info.verbatim_latitude,
#                                          coordinate_precision=info.coordinate_precision,
#                                          bounding_box=info.bounding_box,
#                                          minimum_elevation_in_meters=info.minimum_elevation_in_meters,
#                                          maximum_elevation_in_meters=info.maximum_elevation_in_meters,
#                                          minimum_depth_in_meters=info.minimum_depth_in_meters,
#                                          maximum_depth_in_meters=info.maximum_depth_in_meters, sex=info.sex,
#                                          preparation_type=info.preparation_type,
#                                          individual_count=info.individual_count,
#                                          previous_catalog_number=info.previous_catalog_number,
#                                          relationship_type=info.relationship_type,
#                                          related_catalog_item=info.related_catalog_item,
#                                          occurrence_remarks=info.occurrence_remarks, barcode=info.barcode,
#                                          imagecode=info.imagecode, geo_flag=info.geo_flag)


# def create_identifier(full_name, searched_name, value_founded, trusted=False):
#     return TrustedIdentifier(name=full_name, searched_name=searched_name, value_founded=value_founded, trusted=trusted)
#
#
# def create_info_image(color_mode, path, seq, height, width):
#     return Image(color_mode=color_mode, path=path, seq_id=seq, height=height, width=width)


def get_base():
    return Base


class DataSP(Base):
    __tablename__ = 'data_sp'

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


# County is muncipio, condado
class County(Base):
    __tablename__ = 'ibge'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    county = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    uf = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    state = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    regiao = sqlalchemy.Column(sqlalchemy.String, nullable=True)


class TrustedIdentifier(Base):
    __tablename__ = 'trusted_identifier'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    searched_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    value_founded = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    trusted = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)


class GeorgeData(Base):
    __tablename__ = 'george_selected'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    seq = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('data_sp.seq'), nullable=False)
    data_sp = sqlalchemy.orm.relationship('DataSP', backref=sqlalchemy.orm.backref("george_selected"), uselist=False)


class DataIdentifiersSelectedGeorge(Base):
    __tablename__ = 'data_identifiers_selected_george'

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
    # field selected by George
    country_trusted = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    state_trusted = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    county_trusted = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    kingdom_trusted = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    phylum_trusted = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    classe_trusted = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    order_trusted = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    family_trusted = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    genus_trusted = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    specific_epithet_trusted = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    infraspecific_epithet_trusted = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    scientific_name_authorship_trusted = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # george = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    # list_src = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.String()), nullable=True)
    # list_title = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.String()), nullable=True)
    # info_image = sqlalchemy.orm.relationship('Image', backref='dti')


class Image(Base):
    __tablename__ = 'image_sp'

    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True, autoincrement=True)
    color_mode = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    height = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    width = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    path_segmented = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    path = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    filename = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    seq_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('data_identifiers_selected_george.seq'))
