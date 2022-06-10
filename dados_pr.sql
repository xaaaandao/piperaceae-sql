USE dados_herbarios;
SET GLOBAL local_infile = TRUE;

-- sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
-- add: secure-file-priv = ''
-- systemctl restart mysql
-- sudo chown -R mysql:mysql *
-- sudo chmod 777 -R tmp/ 

(SELECT 
	"seq", "modified", "institutionCode", "collectionCode", "catalogNumber", "basisOfRecord",
	"kingdom", "phylum", "class", "order", "family", "genus", "specificEpithet", "infraspecificEpithet",
	"scientificName", "scientificNameAuthorship", "identifiedBy", "yearIdentified", "monthIdentified",
	"dayIdentified", "typeStatus", "recordedBy", "recordNumber", "fieldNumber",
	"year", "month", "day", "eventTime", "continentOcean", "country", "stateProvince",
	"county", "locality", "decimalLongitude", "decimalLatitude", "verbatimLongitude", "verbatimLatitude",
	"coordinatePrecision", "boundingBox", "minimumElevationInMeters", "maximumElevationInMeters", "minimumDepthInMeters",
	"maximumDepthInMeters", "sex", "preparationType", "individualCount", "previousCatalogNumber", "relationshipType",
	"relatedCatalogItem", "occurrenceRemarks", "barcode", "imagecode", "geoFlag", "GEORGE"
) 
UNION
SELECT	
	dados.seq, dados.modified, dados.institution_code, dados.collection_code, dados.catalogNumber, dados.basis_of_record,
 	dados.kingdom, dados.phylum, dados.classe, dados.ordem, dados.family, dados.genus, dados.specific_epithet, dados.infraspecific_epithet,
 	dados.scientific_name, dados.scientific_name_authorship, dados.identified_by,dados.year_identified, dados.month_identified,
 	dados.day_identified, dados.type_status, dados.recorded_by, dados.record_number, dados.field_number,
 	dados.year, dados.month, dados.day, dados.event_time, dados.continent_ocean, dados.country, dados.state_province,
 	dados.county, dados.locality, dados.decimal_longitude, dados.decimal_latitude, dados.verbatim_longitude, dados.verbatim_latitude,
 	dados.coordinate_precision, dados.bounding_box, dados.minimum_elevationInMeters, dados.maximum_elevationInMeters, dados.minimum_depthInMeters,
 	dados.maximum_depthInMeters, dados.sex, dados.preparation_type, dados.individual_count, dados.previous_catalogNumber, dados.relationship_type,
 	dados.related_catalogItem, dados.occurrence_remarks, dados.barcode, dados.imagecode, dados.geo_flag,dados.GEORGE
FROM dados
	JOIN cidades c on c.nome=dados.state_province -- considera todas cidades do PR
	WHERE
	NOT (dados.identified_by='' OR dados.identified_by IS NULL) AND -- considera amostras identificadas
	(dados.country='Brazil' OR dados.country='Brasil' OR dados.country IS NULL) AND -- considera Brazil, Brasil e vazio
	(state_province LIKE 'Paran%' OR state_province='PR') AND -- considera Parana, Paraná e PR
	NOT (dados.county='' OR dados.county IS NULL) -- evita cidade vazio
INTO OUTFILE '/home/xandao/tmp/dados4.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'; -- exportar
