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
-- "relatedCatalogItem", "occurrenceRemarks", "barcode", "imagecode", "geoFlag", "GEORGE", "uf", "nome_estado"

-- gera exportacao
(SELECT 
	"identified_by"
) 
UNION
SELECT
	*
FROM dados
	JOIN cidades c on c.nome=dados.state_province -- considera todas cidades do PR
	WHERE
	NOT (dados.identified_by='' OR dados.identified_by IS NULL) AND -- considera amostras identificadas
	(dados.country='Brazil' OR dados.country='Brasil' OR dados.country IS NULL) AND -- considera Brazil, Brasil e vazio
	(state_province LIKE 'Paran%' OR state_province='PR') AND -- considera Parana, Paraná e PR
	NOT (dados.county='' OR dados.county IS NULL) -- evita cidade vazio
    ORDER BY identified_by ASC
    INTO OUTFILE '/home/xandao/tmp/dados4.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'; -- exportar
    
    
