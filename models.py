import sqlalchemy as sa
import sqlalchemy.ext.declarative
import sqlalchemy.orm

Base = sa.ext.declarative.declarative_base()


def create_data_trusted_identifier(info):
    return DataTrustedIdentifier(seq=info.seq,
                                 modified=info.modified, institution_code=info.institution_code,
                                 collection_code=info.collection_code, catalog_number=info.catalog_number,
                                 basis_of_record=info.basis_of_record, kingdom=info.kingdom, phylum=info.phylum,
                                 classe=info.classe, order=info.order, family=info.family,
                                 genus=info.genus,
                                 specific_epithet=info.specific_epithet,
                                 infraspecific_epithet=info.infraspecific_epithet,
                                 scientific_name=info.scientific_name,
                                 scientific_name_authorship=info.scientific_name_authorship,
                                 identified_by=info.identified_by, year_identified=info.year_identified,
                                 month_identified=info.month_identified, day_identified=info.day_identified,
                                 type_status=info.type_status,
                                 recorded_by=info.recorded_by, record_number=info.record_number,
                                 field_number=info.field_number, year=info.year, month=info.month,
                                 day=info.day, event_time=info.event_time,
                                 continent_ocean=info.continent_ocean, country=info.country,
                                 state_province=info.state_province, county=info.county, locality=info.locality,
                                 decimal_longitude=info.decimal_longitude,
                                 decimal_latitude=info.decimal_latitude, verbatim_longitude=info.verbatim_longitude,
                                 verbatim_latitude=info.verbatim_latitude,
                                 coordinate_precision=info.coordinate_precision,
                                 bounding_box=info.bounding_box,
                                 minimum_elevation_in_meters=info.minimum_elevation_in_meters,
                                 maximum_elevation_in_meters=info.maximum_elevation_in_meters,
                                 minimum_depth_in_meters=info.minimum_depth_in_meters,
                                 maximum_depth_in_meters=info.maximum_depth_in_meters, sex=info.sex,
                                 preparation_type=info.preparation_type,
                                 individual_count=info.individual_count,
                                 previous_catalog_number=info.previous_catalog_number,
                                 relationship_type=info.relationship_type,
                                 related_catalog_item=info.related_catalog_item,
                                 occurrence_remarks=info.occurrence_remarks, barcode=info.barcode,
                                 imagecode=info.imagecode, geo_flag=info.geo_flag)


def create_identifier(full_name, searched_name, value_founded, trusted=False):
    return TrustedIdentifier(name=full_name, searched_name=searched_name, value_founded=value_founded, trusted=trusted)


def create_info_image(color_mode, path, seq, height, width):
    return Image(color_mode=color_mode, path=path, seq_id=seq, height=height, width=width)


def get_base():
    return Base




class DataSP(Base):
    __tablename__ = 'data_sp'

    seq = sa.Column(sa.BigInteger, primary_key=True)
    modified = sa.Column(sa.DateTime, nullable=True)
    institution_code = sa.Column(sa.String, nullable=True)
    collection_code = sa.Column(sa.String, nullable=True)
    catalog_number = sa.Column(sa.String, nullable=True)
    basis_of_record = sa.Column(sa.String, nullable=True)
    kingdom = sa.Column(sa.String, nullable=True)
    phylum = sa.Column(sa.String, nullable=True)
    classe = sa.Column(sa.String, nullable=True)
    order = sa.Column(sa.String, nullable=True)
    family = sa.Column(sa.String, nullable=True)
    genus = sa.Column(sa.String, nullable=True)
    specific_epithet = sa.Column(sa.String, nullable=True)
    infraspecific_epithet = sa.Column(sa.String, nullable=True)
    scientific_name = sa.Column(sa.String, nullable=True)
    scientific_name_authorship = sa.Column(sa.String, nullable=True)
    identified_by = sa.Column(sa.String, nullable=True)
    year_identified = sa.Column(sa.String, nullable=True)
    month_identified = sa.Column(sa.String, nullable=True)
    day_identified = sa.Column(sa.String, nullable=True)
    type_status = sa.Column(sa.String, nullable=True)
    recorded_by = sa.Column(sa.String, nullable=True)
    record_number = sa.Column(sa.String, nullable=True)
    field_number = sa.Column(sa.String, nullable=True)
    year = sa.Column(sa.BigInteger, nullable=True)
    month = sa.Column(sa.BigInteger, nullable=True)
    day = sa.Column(sa.BigInteger, nullable=True)
    event_time = sa.Column(sa.String, nullable=True)
    continent_ocean = sa.Column(sa.String, nullable=True)
    country = sa.Column(sa.String, nullable=True)
    state_province = sa.Column(sa.String, nullable=True)
    county = sa.Column(sa.String, nullable=True)
    locality = sa.Column(sa.String, nullable=True)
    decimal_longitude = sa.Column(sa.String, nullable=True)
    decimal_latitude = sa.Column(sa.String, nullable=True)
    verbatim_longitude = sa.Column(sa.String, nullable=True)
    verbatim_latitude = sa.Column(sa.String, nullable=True)
    coordinate_precision = sa.Column(sa.String, nullable=True)
    bounding_box = sa.Column(sa.String, nullable=True)
    minimum_elevation_in_meters = sa.Column(sa.BigInteger, nullable=True)
    maximum_elevation_in_meters = sa.Column(sa.BigInteger, nullable=True)
    minimum_depth_in_meters = sa.Column(sa.BigInteger, nullable=True)
    maximum_depth_in_meters = sa.Column(sa.BigInteger, nullable=True)
    sex = sa.Column(sa.String, nullable=True)
    preparation_type = sa.Column(sa.String, nullable=True)
    individual_count = sa.Column(sa.BigInteger, nullable=True)
    previous_catalog_number = sa.Column(sa.String, nullable=True)
    relationship_type = sa.Column(sa.String, nullable=True)
    related_catalog_item = sa.Column(sa.String, nullable=True)
    occurrence_remarks = sa.Column(sa.String, nullable=True)
    barcode = sa.Column(sa.String, nullable=True)
    imagecode = sa.Column(sa.String, nullable=True)
    geo_flag = sa.Column(sa.String, nullable=True)
    george_data = sa.orm.relationship("GeorgeData", backref="data_sp", uselist=False)
    # george = sa.Column(sa.Boolean, nullable=True)

    def __repr__(self):
        return 'DataSP(seq=%s, modified=%s, institution_code=%s, collection_code=%s, catalog_number=%s, ' \
               'basis_of_record=%s, kingdom=%s, phylum=%s, classe=%s, order=%s, family=%s, genus=%s, ' \
               'specific_epithet=%s, infraspecific_epithet=%s, scientific_name=%s, scientific_name_authorship=%s, ' \
               'identified_by=%s, year_identified=%s, month_identified=%s, day_identified=%s, type_status=%s, ' \
               'recorded_by=%s, record_number=%s, field_number=%s, year=%s, month=%s, day=%s, event_time=%s, ' \
               'continent_ocean=%s, country=%s, state_province=%s, county=%s, locality=%s, decimal_longitude=%s, ' \
               'decimal_latitude=%s, verbatim_longitude=%s, verbatim_latitude=%s, coordinate_precision=%s, ' \
               'bounding_box=%s, minimum_elevation_in_meters=%s, maximum_elevation_in_meters=%s, ' \
               'minimum_depth_in_meters=%s, maximum_depth_in_meters=%s, sex=%s, preparation_type=%s, ' \
               'individual_count=%s, previous_catalog_number=%s, relationship_type=%s, related_catalog_item=%s, ' \
               'occurrence_remarks=%s, barcode=%s, imagecode=%s, geo_flag=%s)'


class GeorgeData(Base):
    __tablename__ = 'george_data'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    seq = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('data_sp.seq'), nullable=False)

# County is muncipio, condado
class County(Base):
    __tablename__ = 'county'

    id = sa.Column(sa.Integer, primary_key=True)
    county = sa.Column(sa.String, nullable=True)
    uf = sa.Column(sa.String, nullable=True)
    state = sa.Column(sa.String, nullable=True)
    regiao = sa.Column(sa.String, nullable=True)
    #
    # def __repr__(self):
    #     return 'County(id=%s, county=%s, uf=%s, state=%s, regiao=%s)'


class TrustedIdentifier(Base):
    __tablename__ = 'trusted_identifier'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=True)
    searched_name = sa.Column(sa.String, nullable=True)
    value_founded = sa.Column(sa.String, nullable=True)
    trusted = sa.Column(sa.Boolean, nullable=True)

    def __repr__(self):
        return 'TrustedIdentifier(name=%s, searched_name=%s, value_founded=%s, trusted=%s)'


class DataTrustedIdentifier(Base):
    __tablename__ = 'data_trusted_identifier'

    seq = sa.Column(sa.BigInteger, primary_key=True)
    modified = sa.Column(sa.DateTime, nullable=True)
    institution_code = sa.Column(sa.String, nullable=True)
    collection_code = sa.Column(sa.String, nullable=True)
    catalog_number = sa.Column(sa.String, nullable=True)
    basis_of_record = sa.Column(sa.String, nullable=True)
    kingdom = sa.Column(sa.String, nullable=True)
    phylum = sa.Column(sa.String, nullable=True)
    classe = sa.Column(sa.String, nullable=True)
    order = sa.Column(sa.String, nullable=True)
    family = sa.Column(sa.String, nullable=True)
    genus = sa.Column(sa.String, nullable=True)
    specific_epithet = sa.Column(sa.String, nullable=True)
    infraspecific_epithet = sa.Column(sa.String, nullable=True)
    scientific_name = sa.Column(sa.String, nullable=True)
    scientific_name_authorship = sa.Column(sa.String, nullable=True)
    identified_by = sa.Column(sa.String, nullable=True)
    year_identified = sa.Column(sa.String, nullable=True)
    month_identified = sa.Column(sa.String, nullable=True)
    day_identified = sa.Column(sa.String, nullable=True)
    type_status = sa.Column(sa.String, nullable=True)
    recorded_by = sa.Column(sa.String, nullable=True)
    record_number = sa.Column(sa.String, nullable=True)
    field_number = sa.Column(sa.String, nullable=True)
    year = sa.Column(sa.BigInteger, nullable=True)
    month = sa.Column(sa.BigInteger, nullable=True)
    day = sa.Column(sa.BigInteger, nullable=True)
    event_time = sa.Column(sa.String, nullable=True)
    continent_ocean = sa.Column(sa.String, nullable=True)
    country = sa.Column(sa.String, nullable=True)
    state_province = sa.Column(sa.String, nullable=True)
    county = sa.Column(sa.String, nullable=True)
    locality = sa.Column(sa.String, nullable=True)
    decimal_longitude = sa.Column(sa.String, nullable=True)
    decimal_latitude = sa.Column(sa.String, nullable=True)
    verbatim_longitude = sa.Column(sa.String, nullable=True)
    verbatim_latitude = sa.Column(sa.String, nullable=True)
    coordinate_precision = sa.Column(sa.String, nullable=True)
    bounding_box = sa.Column(sa.String, nullable=True)
    minimum_elevation_in_meters = sa.Column(sa.BigInteger, nullable=True)
    maximum_elevation_in_meters = sa.Column(sa.BigInteger, nullable=True)
    minimum_depth_in_meters = sa.Column(sa.BigInteger, nullable=True)
    maximum_depth_in_meters = sa.Column(sa.BigInteger, nullable=True)
    sex = sa.Column(sa.String, nullable=True)
    preparation_type = sa.Column(sa.String, nullable=True)
    individual_count = sa.Column(sa.BigInteger, nullable=True)
    previous_catalog_number = sa.Column(sa.String, nullable=True)
    relationship_type = sa.Column(sa.String, nullable=True)
    related_catalog_item = sa.Column(sa.String, nullable=True)
    occurrence_remarks = sa.Column(sa.String, nullable=True)
    barcode = sa.Column(sa.String, nullable=True)
    imagecode = sa.Column(sa.String, nullable=True)
    geo_flag = sa.Column(sa.String, nullable=True)
    george = sa.Column(sa.Boolean, nullable=True)
    country_trusted = sa.Column(sa.String, nullable=True)
    state_trusted = sa.Column(sa.String, nullable=True)
    kingdom_trusted = sa.Column(sa.String, nullable=True)
    phylum_trusted = sa.Column(sa.String, nullable=True)
    classe_trusted = sa.Column(sa.String, nullable=True)
    order_trusted = sa.Column(sa.String, nullable=True)
    family_trusted = sa.Column(sa.String, nullable=True)
    genus_trusted = sa.Column(sa.String, nullable=True)
    specific_epithet_trusted = sa.Column(sa.String, nullable=True)
    infraspecific_epithet_trusted = sa.Column(sa.String, nullable=True)
    scientific_name_authorship_trusted = sa.Column(sa.String, nullable=True)
    list_src = sa.Column(sa.ARRAY(sa.String()), nullable=True)
    list_title = sa.Column(sa.ARRAY(sa.String()), nullable=True)
    info_image = sqlalchemy.orm.relationship('Image', backref='dti')

    def __repr__(self):
        return 'DataTrustedIdentifier(seq=%s, modified=%s, institution_code=%s, collection_code=%s, catalog_number=%s, ' \
               'basis_of_record=%s, kingdom=%s, phylum=%s, classe=%s, order=%s, family=%s, genus=%s, ' \
               'specific_epithet=%s, infraspecific_epithet=%s, scientific_name=%s, scientific_name_authorship=%s, ' \
               'identified_by=%s, year_identified=%s, month_identified=%s, day_identified=%s, type_status=%s, ' \
               'recorded_by=%s, record_number=%s, field_number=%s, year=%s, month=%s, day=%s, event_time=%s, ' \
               'continent_ocean=%s, country=%s, state_province=%s, county=%s, locality=%s, decimal_longitude=%s, ' \
               'decimal_latitude=%s, verbatim_longitude=%s, verbatim_latitude=%s, coordinate_precision=%s, ' \
               'bounding_box=%s, minimum_elevation_in_meters=%s, maximum_elevation_in_meters=%s, ' \
               'minimum_depth_in_meters=%s, maximum_depth_in_meters=%s, sex=%s, preparation_type=%s, ' \
               'individual_count=%s, previous_catalog_number=%s, relationship_type=%s, related_catalog_item=%s, ' \
               'occurrence_remarks=%s, barcode=%s, imagecode=%s, geo_flag=%s, country_trusted=%s, state_trusted=%s,' \
               'county=%s )'


class Image(Base):
    __tablename__ = 'image_sp'

    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    color_mode = sa.Column(sa.String, nullable=True)
    height = sa.Column(sa.Integer, nullable=True)
    width = sa.Column(sa.Integer, nullable=True)
    path_segmented = sa.Column(sa.String, nullable=True)
    path = sa.Column(sa.String, nullable=True)
    filename = sa.Column(sa.String, nullable=True)
    seq_id = sa.Column(sa.Integer, sa.ForeignKey('data_trusted_identifier.seq'))

    # def __repr__(self):
    #     return 'Image(path=%s, color_mode=%s, seq_id=%d, height=%d, width=%d)'
