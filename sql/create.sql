CREATE DATABASE IF NOT EXISTS herbario;
USE herbario;

CREATE TABLE IF NOT EXISTS cidades (
	uf VARCHAR(4),
	nome VARCHAR(50)  
);

CREATE TABLE IF NOT EXISTS dados_api_sp(
	seq VARCHAR(100), 
	modified VARCHAR(100), 
	institution_code VARCHAR(100), 
	collection_code VARCHAR(100), 
	catalog_number VARCHAR(100), 
	basis_of_record VARCHAR(100), 
	kingdom VARCHAR(100), 
	phylum VARCHAR(100), 
	classe VARCHAR(100), 
	ordem VARCHAR(100), 
	family VARCHAR(100), 
	genus VARCHAR(100), 
	specific_epithet VARCHAR(100), 
	infraspecific_epithet VARCHAR(100), 
	scientific_name VARCHAR(100), 
	scientific_name_authorship VARCHAR(100), 
	identified_by VARCHAR(100),
	year_identified VARCHAR(100), 
	month_identified VARCHAR(100), 
	day_identified VARCHAR(100), 
	type_status VARCHAR(100), 
	recorded_by VARCHAR(100), 
	record_number VARCHAR(100), 
	field_number VARCHAR(100), 
	year VARCHAR(100), 
	month VARCHAR(100), 
	day VARCHAR(100), 
	event_time VARCHAR(100), 
	continent_ocean VARCHAR(100), 
	country VARCHAR(100), 
	state_province VARCHAR(100), 
	county VARCHAR(100), 
	locality VARCHAR(100), 
	decimal_longitude VARCHAR(100), 
	decimal_latitude VARCHAR(100), 
	verbatim_longitude VARCHAR(100), 
	verbatim_latitude VARCHAR(100), 
	coordinate_precision VARCHAR(100), 
	bounding_box VARCHAR(100), 
	minimum_elevationInMeters VARCHAR(100), 
	maximum_elevationInMeters VARCHAR(100), 
	minimum_depthInMeters VARCHAR(100), 
	maximum_depthInMeters VARCHAR(100), 
	sex VARCHAR(100), 
	preparation_type VARCHAR(100), 
	individual_count VARCHAR(100), 
	previous_catalog_number VARCHAR(100), 
	relationship_type VARCHAR(100), 
	related_catalog_item VARCHAR(100), 
	occurrence_remarks VARCHAR(100), 
	barcode VARCHAR(100), 
	imagecode VARCHAR(100), 
	geo_flag VARCHAR(100),
	GEORGE BOOLEAN
);

CREATE TABLE IF NOT EXISTS iwssip (
  cod_barra VARCHAR(30)
);
