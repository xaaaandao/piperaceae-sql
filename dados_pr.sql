USE dados_herbarios;
SET GLOBAL local_infile = TRUE;

-- sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
-- systemctl restart mysql
-- sudo chmod 777 -R tmp/ 

-- cabecalho
-- "seq", "modified", "institutionCode", "collectionCode", "catalogNumber", "basisOfRecord",
-- "kingdom", "phylum", "class", "order", "family", "genus", "specificEpithet", "infraspecificEpithet",
-- "scientificName", "scientificNameAuthorship", "identifiedBy", "yearIdentified", "monthIdentified",
-- "dayIdentified", "typeStatus", "recordedBy", "recordNumber", "fieldNumber",
-- "year", "month", "day", "eventTime", "continentOcean", "country", "stateProvince",
-- "county", "locality", "decimalLongitude", "decimalLatitude", "verbatimLongitude", "verbatimLatitude",
-- "coordinatePrecision", "boundingBox", "minimumElevationInMeters", "maximumElevationInMeters", "minimumDepthInMeters",
-- "maximumDepthInMeters", "sex", "preparationType", "individualCount", "previousCatalogNumber", "relationshipType",
-- "relatedCatalogItem", "occurrenceRemarks", "barcode", "imagecode", "geoFlag"

-- gera exportacao
(SELECT 
	"identified_by"
) 
UNION
SELECT
	DISTINCT identified_by
FROM d30m05a2022
	JOIN cidades c on c.nome=d30m05a2022.state_province -- considera todas cidades do PR
	WHERE
	NOT (identified_by='' OR identified_by IS NULL) AND -- considera amostras identificadas
	(country='Brazil' OR country='Brasil' OR country IS NULL) AND -- considera Brazil, Brasil e vazio
	(state_province LIKE 'Paran%' OR state_province='PR') AND -- considera Parana, Paraná e PR
	NOT (county='' OR county IS NULL) -- evita cidade vazio
    ORDER BY identified_by ASC
    INTO OUTFILE '/home/xandao/tmp/dados4.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'; -- exportar
    
    