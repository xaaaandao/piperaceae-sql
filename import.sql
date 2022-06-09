USE dados_herbarios;
SET GLOBAL local_infile = TRUE;
LOAD DATA LOCAL INFILE '/home/xandao/herbario/dados.csv' INTO TABLE dados FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
