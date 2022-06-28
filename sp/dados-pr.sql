-- dados do Paraná

USE dados_api_sp;
SET GLOBAL local_infile = TRUE;

-- sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
-- add: secure-file-priv = ''
-- systemctl restart mysql
-- sudo chown -R mysql:mysql *
-- sudo chmod 777 -R tmp/ 

-- EXPORTAR
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
	dados_api_sp.seq, dados_api_sp.modified, dados_api_sp.institution_code, dados_api_sp.collection_code, dados_api_sp.catalogNumber, dados_api_sp.basis_of_record,
 	dados_api_sp.kingdom, dados_api_sp.phylum, dados_api_sp.classe, dados_api_sp.ordem, dados_api_sp.family, dados_api_sp.genus, dados_api_sp.specific_epithet, dados_api_sp.infraspecific_epithet,
 	dados_api_sp.scientific_name, dados_api_sp.scientific_name_authorship, dados_api_sp.identified_by,dados_api_sp.year_identified, dados_api_sp.month_identified,
 	dados_api_sp.day_identified, dados_api_sp.type_status, dados_api_sp.recorded_by, dados_api_sp.record_number, dados_api_sp.field_number,
 	dados_api_sp.year, dados_api_sp.month, dados_api_sp.day, dados_api_sp.event_time, dados_api_sp.continent_ocean, dados_api_sp.country, dados_api_sp.state_province,
 	dados_api_sp.county, dados_api_sp.locality, dados_api_sp.decimal_longitude, dados_api_sp.decimal_latitude, dados_api_sp.verbatim_longitude, dados_api_sp.verbatim_latitude,
 	dados_api_sp.coordinate_precision, dados_api_sp.bounding_box, dados_api_sp.minimum_elevationInMeters, dados_api_sp.maximum_elevationInMeters, dados_api_sp.minimum_depthInMeters,
 	dados_api_sp.maximum_depthInMeters, dados_api_sp.sex, dados_api_sp.preparation_type, dados_api_sp.individual_count, dados_api_sp.previous_catalogNumber, dados_api_sp.relationship_type,
 	dados_api_sp.related_catalogItem, dados_api_sp.occurrence_remarks, dados_api_sp.barcode, dados_api_sp.imagecode, dados_api_sp.geo_flag,dados_api_sp.GEORGE
FROM dados_api_sp
	JOIN cidades c on c.nome=dados_api_sp.state_province -- considera todas cidades do PR
	WHERE
	NOT (dados_api_sp.identified_by='' OR dados_api_sp.identified_by IS NULL) AND -- considera amostras identificadas
	(dados_api_sp.country='Brazil' OR dados_api_sp.country='Brasil' OR dados_api_sp.country IS NULL) AND -- considera Brazil, Brasil e vazio
	(state_province LIKE 'Paran%' OR state_province='PR') AND -- considera Parana, Paraná e PR
	NOT (dados_api_sp.county='' OR dados_api_sp.county IS NULL) -- evita cidade vazio
INTO OUTFILE '/home/xandao/tmp/dados_api_sp4.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'; -- exportar

-- QUANTIDADE DE AMOSTRAS QUE TEM NO PR
SELECT	
	COUNT(*)
FROM dados_api_sp
	JOIN cidades c on c.nome=dados_api_sp.state_province -- considera todas cidades do PR
	WHERE
	NOT (dados_api_sp.identified_by='' OR dados_api_sp.identified_by IS NULL) AND -- considera amostras identificadas
	(dados_api_sp.country='Brazil' OR dados_api_sp.country='Brasil' OR dados_api_sp.country IS NULL) AND -- considera Brazil, Brasil e vazio
	(state_province LIKE 'Paran%' OR state_province='PR') AND -- considera Parana, Paraná e PR
	NOT (dados_api_sp.county='' OR dados_api_sp.county IS NULL); -- evita cidade vazio
