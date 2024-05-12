import logging

from models import DataIdentifiersSelectedGeorge, DataSP, TrustedIdentifier


def create_data_trusted_identifier(info):
    return DataIdentifiersSelectedGeorge(seq=info.seq,
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
                                         decimal_latitude=info.decimal_latitude,
                                         verbatim_longitude=info.verbatim_longitude,
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


def insert_data_trusted_identifier(session):
    query = session.query(TrustedIdentifier.value_founded) \
        .filter(TrustedIdentifier.trusted) \
        .distinct() \
        .all()

    list_variations_of_identifiers_trusted = [q.value_founded for q in query]

    count_of_records_with_variations_identifier_name = session.query(DataSP) \
        .filter(DataSP.identified_by.in_(list_variations_of_identifiers_trusted)) \
        .count()

    logging.info(
        'count of records founded with variations of identifier name: %d' % count_of_records_with_variations_identifier_name)

    assert count_of_records_with_variations_identifier_name == 13182

    count_data_in_data_trusted_identifier = session.query(DataIdentifiersSelectedGeorge).count()

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

    count_data_from_trusted_identifers = session.query(DataIdentifiersSelectedGeorge).count()
    logging.info(
        'count of records in table %s: %d' % (
            DataIdentifiersSelectedGeorge.__tablename__, count_data_from_trusted_identifers))

    assert count_data_from_trusted_identifers == 13182
