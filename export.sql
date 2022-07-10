-- sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
-- add: secure-file-priv = ''
-- systemctl restart mysql
-- sudo chown -R mysql:mysql *
-- sudo chmod 777 -R tmp/ 

USE herbario;
SET GLOBAL local_infile = TRUE;

SELECT GROUP_CONCAT(CONCAT(" '", COLUMN_NAME, "' ")) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'cidades' AND TABLE_SCHEMA = 'herbario' ORDER BY ORDINAL_POSITION INTO OUTFILE '/home/xandao/tmp/csv-postgresql/cidades_h.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n';
SELECT * INTO OUTFILE '/home/xandao/tmp/csv-postgresql/cidades_d.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n' FROM cidades;

SELECT GROUP_CONCAT(CONCAT(" '", COLUMN_NAME, "' ")) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'dados_api_sp' AND TABLE_SCHEMA = 'herbario' ORDER BY ORDINAL_POSITION INTO OUTFILE '/home/xandao/tmp/csv-postgresql/dados_api_sp_h.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n';
SELECT * INTO OUTFILE '/home/xandao/tmp/csv-postgresql/dados_api_sp_d.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n' FROM dados_api_sp;

SELECT GROUP_CONCAT(CONCAT(" '", COLUMN_NAME, "' ")) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'dados_web_reflora' AND TABLE_SCHEMA = 'herbario' ORDER BY ORDINAL_POSITION INTO OUTFILE '/home/xandao/tmp/csv-postgresql/dados_web_reflora_h.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n';
SELECT * INTO OUTFILE '/home/xandao/tmp/csv-postgresql/dados_web_reflora_d.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n' FROM dados_web_reflora;

SELECT GROUP_CONCAT(CONCAT(" '", COLUMN_NAME, "' ")) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'determinacao_web_reflora' AND TABLE_SCHEMA = 'herbario' ORDER BY ORDINAL_POSITION INTO OUTFILE '/home/xandao/tmp/csv-postgresql/determinacao_web_reflora_h.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n';
SELECT * INTO OUTFILE '/home/xandao/tmp/csv-postgresql/determinacao_web_reflora_d.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n' FROM determinacao_web_reflora;

SELECT GROUP_CONCAT(CONCAT(" '", COLUMN_NAME, "' ")) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'duplicatas_web_reflora' AND TABLE_SCHEMA = 'herbario' ORDER BY ORDINAL_POSITION INTO OUTFILE '/home/xandao/tmp/csv-postgresql/duplicatas_web_reflora_h.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n';
SELECT * INTO OUTFILE '/home/xandao/tmp/csv-postgresql/duplicatas_web_reflora_d.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n' FROM duplicatas_web_reflora;

SELECT GROUP_CONCAT(CONCAT(" '", COLUMN_NAME, "' ")) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'figuras_web_reflora' AND TABLE_SCHEMA = 'herbario' ORDER BY ORDINAL_POSITION INTO OUTFILE '/home/xandao/tmp/csv-postgresql/figuras_web_reflora_h.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n';
SELECT * INTO OUTFILE '/home/xandao/tmp/csv-postgresql/figuras_web_reflora_d.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n' FROM figuras_web_reflora;

SELECT GROUP_CONCAT(CONCAT(" '", COLUMN_NAME, "' ")) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'historico_web_reflora' AND TABLE_SCHEMA = 'herbario' ORDER BY ORDINAL_POSITION INTO OUTFILE '/home/xandao/tmp/csv-postgresql/historico_web_reflora_h.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n';
SELECT * INTO OUTFILE '/home/xandao/tmp/csv-postgresql/historico_web_reflora_d.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n' FROM historico_web_reflora;

SELECT GROUP_CONCAT(CONCAT(" '", COLUMN_NAME, "' ")) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'iwssip' AND TABLE_SCHEMA = 'herbario' ORDER BY ORDINAL_POSITION INTO OUTFILE '/home/xandao/tmp/csv-postgresql/iwssip_h.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n';
SELECT * INTO OUTFILE '/home/xandao/tmp/csv-postgresql/iwssip_d.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n' FROM iwssip;

-- EXPORTAR DADOS PR
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

-- CONSULTAS QUE TEM O GEORGE
-- QUANTIDADE DE AMOSTRAS APROVADAS PELO GEORGE
SELECT    
    barcode
FROM dados_api_sp
    WHERE GEORGE IS TRUE;

-- QUANTIDADE DE GÊNEROS APROVADOS PELO GEORGE
SELECT COUNT(DISTINCT genus) FROM dados_api_sp WHERE GEORGE IS TRUE;

-- QUANTIDADE DE AMOSTRAS POR GÊNERO APROVADOS PELO GEORGE
SELECT DISTINCT genus, COUNT(*) FROM dados_api_sp WHERE GEORGE IS TRUE GROUP BY genus;

-- QUANTIDADE DE ESPÉCIES
SELECT COUNT(DISTINCT infraspecific_epithet) FROM dados_api_sp WHERE GEORGE IS TRUE;

-- QUANTIDADE DE AMOSTRAS POR ESPÉCIE
SELECT DISTINCT specific_epithet, COUNT(*) AS QUANTIDADE FROM dados_api_sp WHERE GEORGE IS TRUE GROUP BY specific_epithet ORDER BY QUANTIDADE DESC;

-- QUANTIDADE DE IDENTIFICADORES
SELECT DISTINCT identified_by, COUNT(*) AS QUANTIDADE FROM dados_api_sp WHERE GEORGE IS TRUE GROUP BY identified_by ORDER BY QUANTIDADE DESC;
    
-- AMOSTRAS IGUAIS DO DATASET DO IWSSIP    
SELECT COUNT(*) FROM dados_api_sp JOIN iwssip on dados_api_sp.barcode = iwssip.cod_barra WHERE GEORGE IS TRUE;

-- IDENTIFICADORES DOS GÊNEROS
SELECT identified_by, genus FROM dados_api_sp WHERE GEORGE IS TRUE ORDER BY genus ASC LIMIT 5;

-- VERIFICA SE AS ESPÉCIES QUE ESTÃO NA API SÃO IGUAIS AO SITE
SELECT A.specific_epithet AS AG, A.barcode AS AB, W.species AS WG, W.barcode AS WB
	FROM dados_api_sp AS A
    JOIN dados_web_sp W ON W.barcode=A.barcode
    WHERE GEORGE IS TRUE AND A.specific_epithet<>W.species;	
    
-- APRESENTA OS ESPÉCIES, QUANTIDADE DE AMOSTRAS POR ESPÉCIE E OS SEUS RESPECTIVOS COD_BARRA
SELECT specific_epithet AS ESPÉCIES, COUNT(*) AS QUANTIDADE, GROUP_CONCAT(barcode) AS COD_BARRA
	FROM dados_api_sp
	WHERE GEORGE=TRUE GROUP BY specific_epithet ORDER BY QUANTIDADE DESC;
	
-- APRESENTA OS GÊNEROS, QUANTIDADE DE AMOSTRAS POR GÊNERO E OS SEUS RESPECTIVOS COD_BARRA
SELECT genus AS GÊNEROS, COUNT(*) AS QUANTIDADE, GROUP_CONCAT(barcode) AS COD_BARRA
	FROM dados_api_sp
	WHERE GEORGE=TRUE GROUP BY genus ORDER BY QUANTIDADE DESC;
