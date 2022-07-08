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
