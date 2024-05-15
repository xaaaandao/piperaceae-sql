from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.ext.declarative
import sqlalchemy.orm

Base = sa.orm.declarative_base()


def get_base():
    return Base


exsiccata_level = sa.Table(
    'exsiccata_level',
    Base.metadata,
    sa.Column('exsiccata_id', sa.ForeignKey('exsiccata.seq')),
    sa.Column('level_id', sa.ForeignKey('level.id')),
)

exsiccata_identifier = sa.Table(
    'exsiccata_identifier',
    Base.metadata,
    sa.Column('exsiccata_id', sa.ForeignKey('exsiccata.seq')),
    sa.Column('identifier_id', sa.ForeignKey('identifier.id')),
)


exsiccata_dataset = sa.Table(
    'exsiccata_dataset',
    Base.metadata,
    sa.Column('exsiccata_id', sa.ForeignKey('exsiccata.seq')),
    sa.Column('dataset_id', sa.ForeignKey('dataset.id')),
)

class County(Base):
    __tablename__ = 'county'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=True)
    state = sa.orm.relationship('State', back_populates='county')
    state_id = sa.Column(sa.Integer, sa.ForeignKey('state.id'))

    def __repr__(self):
        return 'County(name=%s, state_id=%s)'


class State(Base):
    __tablename__ = 'state'

    # id: sa.orm.Mapped[int] = sa.orm.mapped_column(primary_key=True)
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, unique=True)
    name = sa.Column(sa.String, primary_key=True, unique=True)
    uf = sa.Column(sa.String, primary_key=True, unique=True)
    region = sa.Column(sa.String, nullable=True)
    county = sa.orm.relationship('County', back_populates='state')

    def __repr__(self):
        return 'State(uf=%s, name=%s, region=%s)'


class Local(Base):
    __tablename__ = 'local'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    event_time = sa.Column(sa.String, nullable=True)
    continent_ocean = sa.Column(sa.String, nullable=True)
    country = sa.Column(sa.String, nullable=True)
    state_province = sa.Column(sa.String, nullable=True)
    county = sa.Column(sa.String, nullable=True)
    locality = sa.Column(sa.String, nullable=True)
    decimal_longitude = sa.Column(sa.Double, nullable=True)
    decimal_latitude = sa.Column(sa.Double, nullable=True)
    verbatim_longitude = sa.Column(sa.String, nullable=True)
    verbatim_latitude = sa.Column(sa.String, nullable=True)
    coordinate_precision = sa.Column(sa.Double, nullable=True)
    bounding_box = sa.Column(sa.String, nullable=True)
    minimum_elevation_in_meters = sa.Column(sa.Double, nullable=True)
    maximum_elevation_in_meters = sa.Column(sa.Double, nullable=True)
    minimum_depth_in_meters = sa.Column(sa.Double, nullable=True)
    maximum_depth_in_meters = sa.Column(sa.Double, nullable=True)
    local_trusted: sa.orm.Mapped['LocalTrusted'] = sa.orm.relationship(back_populates='local')
    exsiccata = sa.orm.relationship('Exsiccata', back_populates='local')
    exsiccata_id = sa.Column(sa.Integer, sa.ForeignKey('exsiccata.seq'))

    def __repr__(self):
        return 'Local(event_time=%s, continent_ocean=%s, country=%s, state_province=%s, county=%s, locality=%s, decimal_longitude=%s, decimal_latitude=%s, verbatim_longitude=%s, verbatim_latitude=%s, coordinate_precision=%s, bounding_box=%s, minimum_elevation_in_meters=%s, maximum_elevation_in_meters=%s, minimum_depth_in_meters=%s, maximum_depth_in_meters=%s)'


class LocalTrusted(Base):
    __tablename__ = 'local_trusted'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    country = sa.Column(sa.String, nullable=True)
    state_province = sa.Column(sa.String, nullable=True)
    county = sa.Column(sa.String, nullable=True)
    local_id: sa.orm.Mapped[int] = sa.orm.mapped_column(sa.ForeignKey("local.id"))
    local: sa.orm.Mapped['Local'] = sa.orm.relationship(back_populates="local_trusted")

    def __repr__(self):
        return 'LocalTrusted(local_id=%s)'


class Exsiccata(Base):
    __tablename__ = 'exsiccata'

    seq = sa.Column(sa.Integer, primary_key=True)
    institution_code = sa.Column(sa.String, nullable=True)
    collection_code = sa.Column(sa.String, nullable=True)
    catalog_number = sa.Column(sa.String, nullable=True)
    basis_of_record = sa.Column(sa.String, nullable=True)
    type_status = sa.Column(sa.String, nullable=True)
    recorded_by = sa.Column(sa.String, nullable=True)
    record_number = sa.Column(sa.String, nullable=True)
    field_number = sa.Column(sa.String, nullable=True)
    year = sa.Column(sa.Integer, nullable=True)
    month = sa.Column(sa.Integer, nullable=True)
    day = sa.Column(sa.Integer, nullable=True)
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
    levels: sa.orm.Mapped[List['Level']] = sa.orm.relationship(secondary=exsiccata_level)
    datasets: sa.orm.Mapped[List['Dataset']] = sa.orm.relationship(secondary=exsiccata_dataset)
    identifiers: sa.orm.Mapped[List['Identifier']] = sa.orm.relationship(secondary=exsiccata_identifier)
    local = sa.orm.relationship('Local', back_populates='exsiccata')
    george_data: sa.orm.Mapped['GeorgeData'] = sa.orm.relationship(back_populates='exsiccata')

    def __repr__(self):
        return 'Exsiccata(seq=%s, institution_code=%s, collection_code=%s, catalog_number=%s, basis_of_record=%s, type_status=%s, recorded_by=%s, record_number=%s, field_number=%s, year=%s, month=%s, day=%s, sex=%s, preparation_type=%s, individual_count=%s, previous_catalog_number=%s, relationship_type=%s, related_catalog_item=%s, occurrence_remarks=%s, barcode=%s, imagecode=%s, geo_flag=%s)'


class Identifier(Base):
    __tablename__ = 'identifier'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    identified_by = sa.Column(sa.String, nullable=True)
    year_identified = sa.Column(sa.Integer, nullable=True)
    month_identified = sa.Column(sa.Integer, nullable=True)
    day_identified = sa.Column(sa.Integer, nullable=True)

    # exsiccatas: sa.orm.Mapped[List['ExsiccataIdentifier']] = sa.orm.relationship(back_populates='identifier')

    def __repr__(self):
        return 'Identifier(identified_by=%s, year_identified=%s, month_identified=%s, day_identified=%s)'


class Level(Base):
    __tablename__ = 'level'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
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

    def __repr__(self):
        return 'Level(kingdom=%s, phylum=%s, classe=%s, order=%s, family=%s, genus=%s, specific_epithet=%s, infraspecific_epithet=%s, scientific_name=%s, scientific_name_authorship=%s)'


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
    trusted_identifier_selected = sa.orm.relationship('TrustedIdentifierSelected', back_populates='trusted_identifier')


class TrustedIdentifierSelected(Base):
    __tablename__ = 'trusted_identifier_selected'

    id: sa.orm.Mapped[int] = sa.orm.mapped_column(primary_key=True, autoincrement=True)
    value_founded = sa.Column(sa.String, nullable=True)
    selected = sa.Column(sa.Boolean, nullable=True)
    trusted_identifier = sa.orm.relationship('TrustedIdentifier', back_populates='trusted_identifier_selected')
    trusted_identifier_id = sa.Column(sa.Integer, sa.ForeignKey('trusted_identifier.id'))


class Dataset(Base):
    __tablename__ = 'dataset'

    id: sa.orm.Mapped[int] = sa.orm.mapped_column(primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=True)
    minimum = sa.Column(sa.Integer, nullable=True)

