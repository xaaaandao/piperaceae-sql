-- importar dados do specieslink
-- mysql --local-infile=1 -u root -p

USE herbario;
SET GLOBAL local_infile = TRUE;
LOAD DATA LOCAL INFILE '/home/xandao/herbario/dados.csv' INTO TABLE dados FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
