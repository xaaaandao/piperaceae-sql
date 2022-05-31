#!/bin/bash
current_date = `date +"d%dm%ma%y"`

download:
	@wget -O $(current_date).csv https://api.splink.org.br/records/format/csv/family/Piperaceae/images/yes
	"baixando arquivo de nome: $(current_date).csv"

create:
	@rm -f create.sql
	@echo "criando arquivo de nome: create.sql"
	@touch create.sql
	@echo "CREATE DATABASE IF NOT EXISTS dados_herbarios;" >> create.sql
	@echo "USE dados_herbarios;" >> create.sql
	@echo "CREATE TABLE IF NOT EXISTS $(current_date)(\
	    seq VARCHAR(100), \
	    modified VARCHAR(100), \
	    institution_code VARCHAR(100), \
	    collection_code VARCHAR(100), \
	    catalogNumber VARCHAR(100), \
	    basis_of_record VARCHAR(100), \
	    kingdom VARCHAR(100), \
	    phylum VARCHAR(100), \
	    classe VARCHAR(100), \
	    ordem VARCHAR(100), \
	    family VARCHAR(100), \
	    genus VARCHAR(100), \
	    specific_epithet VARCHAR(100), \
	    infraspecific_epithet VARCHAR(100), \
	    scientific_name VARCHAR(100), \
	    scientific_name_authorship VARCHAR(100), \
	    identified_by VARCHAR(100), \
	    year_identified VARCHAR(100), \
	    month_identified VARCHAR(100), \
	    day_identified VARCHAR(100), \
	    type_status VARCHAR(100), \
	    recorded_by VARCHAR(100), \
	    record_number VARCHAR(100), \
	    field_number VARCHAR(100), \
	    year VARCHAR(100), \
	    month VARCHAR(100), \
	    day VARCHAR(100), \
	    event_time VARCHAR(100), \
	    continent_ocean VARCHAR(100), \
	    country VARCHAR(100), \
	    state_province VARCHAR(100), \
	    county VARCHAR(100), \
	    locality VARCHAR(100), \
	    decimal_longitude VARCHAR(100), \
	    decimal_latitude VARCHAR(100), \
	    verbatim_longitude VARCHAR(100), \
	    verbatim_latitude VARCHAR(100), \
	    coordinate_precision VARCHAR(100), \
	    bounding_box VARCHAR(100), \
	    minimum_elevationInMeters VARCHAR(100), \
	    maximum_elevationInMeters VARCHAR(100), \
	    minimum_depthInMeters VARCHAR(100), \
	    maximum_depthInMeters VARCHAR(100), \
	    sex VARCHAR(100), \
	    preparation_type VARCHAR(100), \
	    individual_count VARCHAR(100), \
	    previous_catalogNumber VARCHAR(100), \
	    relationship_type VARCHAR(100), \
	    related_catalogItem VARCHAR(100), \
	    occurrence_remarks VARCHAR(100), \
	    barcode VARCHAR(100), \
	    imagecode VARCHAR(100), \
	    geo_flag VARCHAR(100) \
	);" >> create.sql

import:
	@rm -f import.sql
	@echo "criando o arquivo: import.sql"
	@touch import.sql
	@echo "USE dados_herbarios;" >> import.sql
	@echo "SET GLOBAL local_infile = TRUE;" >> import.sql
	@echo "LOAD DATA LOCAL INFILE '/home/xandao/herbario/$(current_date).csv' INTO TABLE $(current_date)\
		FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;" >> import.sql

pr:
	@rm -f pr.sql
	@echo "criando o arquivo: pr.sql"
	@touch pr.sql
	@echo "USE dados_herbarios;" >> pr.sql
	@echo "SET GLOBAL local_infile = TRUE;" >> pr.sql
	@echo "SELECT * FROM $(current_date) WHERE state_province \
		LIKE 'Paran%' OR state_province='PR' \
		INTO OUTFILE '/var/lib/mysql-files/pr.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';" >> pr.sql
	@echo "salvo em: /var/lib/mysql-files/pr.csv"

sc:
	@rm -f sc.sql
	@echo "criando o arquivo: sc.sql"
	@touch sc.sql
	@echo "USE dados_herbarios;" >> sc.sql
	@echo "SET GLOBAL local_infile = TRUE;" >> sc.sql \
	@echo "SELECT * FROM $(current_date) WHERE state_province='Santa Catarina' OR state_province='SC' \
		INTO OUTFILE '/var/lib/mysql-files/sc.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';" >> sc.sql
	@echo "salvo em: /var/lib/mysql-files/sc.csv"

rs:
	@rm -f rs.sql
	@echo "criando o arquivo: rs.sql"
	@touch rs.sql
	@echo "USE dados_herbarios;" >> rs.sql
	@echo "SET GLOBAL local_infile = TRUE;" >> rs.sql
	@echo "SELECT * FROM $(current_date) WHERE state_province='Rio Grande do Sul' OR state_province='RS' \
		INTO OUTFILE '/var/lib/mysql-files/rs.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';" >> rs.sql
	@echo "salvo em: /var/lib/mysql-files/rs.csv"		

sul:
	@rm -f sul.sql
	@echo "criando o arquivo: sul.sql"
	@touch sul.sql
	@echo "USE dados_herbarios;" >> sul.sql	
	@echo "SET GLOBAL local_infile = TRUE;" >> sul.sql
	@echo "SELECT * FROM $(current_date) WHERE state_province \
		LIKE 'Paran%' OR state_province='PR' OR \
		state_province='Santa Catarina' OR state_province='SC' OR  \
		state_province='Rio Grande do Sul' OR state_province='RS' \
		INTO OUTFILE '/var/lib/mysql-files/sul.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';" >> sul.sql
	@echo "salvo em: /var/lib/mysql-files/sul.csv"		
