import sqlalchemy as sa
import sqlalchemy.orm

Base = sa.orm.declarative_base()


def get_base():
    return Base


class County(Base):
    __tablename__ = 'county'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=True)
    state = sa.orm.relationship('State', back_populates='county')
    state_id = sa.Column(sa.Integer, sa.ForeignKey('state.id'))


class State(Base):
    __tablename__ = 'state'

    # id: sa.orm.Mapped[int] = sa.orm.mapped_column(primary_key=True)
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, unique=True)
    name = sa.Column(sa.String, primary_key=True, unique=True)
    uf = sa.Column(sa.String, primary_key=True, unique=True)
    region = sa.Column(sa.String, nullable=True)
    county = sa.orm.relationship('County', back_populates='state')


class Exsiccata(Base):
    __tablename__ = 'exsiccata'

    seq = sa.Column(sa.Integer, primary_key=True)
    modified = sa.Column(sa.String, nullable=True)
    institution_code = sa.Column(sa.String, nullable=True)
    collection_code = sa.Column(sa.String, nullable=True)
    catalog_number = sa.Column(sa.String, nullable=True)
    basis_of_record = sa.Column(sa.String, nullable=True)
    identified_by = sa.Column(sa.String, nullable=True)
    year_identified = sa.Column(sa.Integer, nullable=True)
    month_identified = sa.Column(sa.Integer, nullable=True)
    day_identified = sa.Column(sa.Integer, nullable=True)
    type_status = sa.Column(sa.String, nullable=True)
    recorded_by = sa.Column(sa.String, nullable=True)
    record_number = sa.Column(sa.String, nullable=True)
    field_number = sa.Column(sa.String, nullable=True)
    year = sa.Column(sa.Integer, nullable=True)
    month = sa.Column(sa.Integer, nullable=True)
    day = sa.Column(sa.Integer, nullable=True)
    event_time = sa.Column(sa.String, nullable=True)
    bounding_box = sa.Column(sa.String, nullable=True)
    minimum_elevation_in_meters = sa.Column(sa.Integer, nullable=True)
    maximum_elevation_in_meters = sa.Column(sa.Integer, nullable=True)
    minimum_depth_in_meters = sa.Column(sa.Integer, nullable=True)
    maximum_depth_in_meters = sa.Column(sa.Integer, nullable=True)
    sex = sa.Column(sa.String, nullable=True)
    preparation_type = sa.Column(sa.String, nullable=True)
    individual_count = sa.Column(sa.String, nullable=True)
    previous_catalog_number = sa.Column(sa.String, nullable=True)
    relationship_type = sa.Column(sa.String, nullable=True)
    related_catalog_item = sa.Column(sa.String, nullable=True)
    occurrence_remarks = sa.Column(sa.String, nullable=True)
    barcode = sa.Column(sa.String, nullable=True)
    imagecode = sa.Column(sa.String, nullable=True)
    geo_flag = sa.Column(sa.String, nullable=True)
    level_id: sa.orm.Mapped[int] = sa.orm.mapped_column(sa.ForeignKey('level.id'))
    level: sa.orm.Mapped['Level'] = sa.orm.relationship(back_populates='exsiccata')
    local_id: sa.orm.Mapped[int] = sa.orm.mapped_column(sa.ForeignKey('county.id'))
    local: sa.orm.Mapped['Local'] = sa.orm.relationship(back_populates='exsiccata')
    identifier_id: sa.orm.Mapped[int] = sa.orm.mapped_column(sa.ForeignKey('identifier.id'))
    identifier: sa.orm.Mapped['Identifier'] = sa.orm.relationship(back_populates='exsiccata')
    george_data: sa.orm.Mapped['GeorgeData'] = sa.orm.relationship(back_populates='exsiccata')


class Level(Base):
    __tablename__ = 'level'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    kingdom_old = sa.Column(sa.String, nullable=True)
    phylum_old = sa.Column(sa.String, nullable=True)
    classe_old = sa.Column(sa.String, nullable=True)
    order_old = sa.Column(sa.String, nullable=True)
    family_old = sa.Column(sa.String, nullable=True)
    genus_old = sa.Column(sa.String, nullable=True)
    specific_epithet_old = sa.Column(sa.String, nullable=True)
    infraspecific_epithet_old = sa.Column(sa.String, nullable=True)
    scientific_name_old = sa.Column(sa.String, nullable=True)
    scientific_name_authorship_old = sa.Column(sa.String, nullable=True)
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
    exsiccata: sa.orm.Mapped['Exsiccata'] = sa.orm.relationship(back_populates='level')


class Local(Base):
    __tablename__ = 'county'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    continent_ocean = sa.Column(sa.String, nullable=True)
    country_old = sa.Column(sa.String, nullable=True)
    state_province_old = sa.Column(sa.String, nullable=True)
    county_old = sa.Column(sa.String, nullable=True)
    country = sa.Column(sa.String, nullable=True)
    state_province = sa.Column(sa.String, nullable=True)
    county = sa.Column(sa.String, nullable=True)
    locality = sa.Column(sa.String, nullable=True)
    decimal_longitude = sa.Column(sa.Float, nullable=True)
    decimal_latitude = sa.Column(sa.Float, nullable=True)
    verbatim_longitude = sa.Column(sa.String, nullable=True)
    verbatim_latitude = sa.Column(sa.String, nullable=True)
    coordinate_precision = sa.Column(sa.Float, nullable=True)
    exsiccata: sa.orm.Mapped['Exsiccata'] = sa.orm.relationship(back_populates='county')


class Identifier(Base):
    __tablename__ = 'identifier'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    identified_by = sa.Column(sa.String, nullable=True)
    year_identified = sa.Column(sa.Integer, nullable=True)
    month_identified = sa.Column(sa.Integer, nullable=True)
    day_identified = sa.Column(sa.Integer, nullable=True)
    exsiccata: sa.orm.Mapped['Exsiccata'] = sa.orm.relationship(back_populates='identifier')


class GeorgeData(Base):
    __tablename__ = 'george_data'

    id: sa.orm.Mapped[int] = sa.orm.mapped_column(primary_key=True)
    exsiccata_id: sa.orm.Mapped[int] = sa.orm.mapped_column(sa.ForeignKey("exsiccata.seq"))
    exsiccata: sa.orm.Mapped['Exsiccata'] = sa.orm.relationship(back_populates="george_data")


class TrustedIdentifier(Base):
    __tablename__ = 'trusted_identifier'

    id: sa.orm.Mapped[int] = sa.orm.mapped_column(primary_key=True, autoincrement=True)
    fullname = sa.Column(sa.String, nullable=True)
    search = sa.Column(sa.String, nullable=True)
    value_founded = sa.Column(sa.String, nullable=True)
    selected = sa.Column(sa.Boolean, nullable=True)
