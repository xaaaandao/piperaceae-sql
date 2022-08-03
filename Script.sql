drop table data;
truncate table data;


ALTER TABLE data ADD COLUMN test tsvector;
UPDATE data SET test = setweight(to_tsvector(data.country), 'A') || setweight(to_tsvector(data.state_province), 'B') || setweight(to_tsvector(data.county), 'C');
CREATE INDEX IF NOT EXISTS idx_test ON data USING gin(test);
--select data.seq, ts_rank(test, q) as rank from data, plainto_tsquery('curitiba') q where test @@ q ORDER BY rank desc;
SELECT seq, DISts_rank(test, query) AS score FROM data, to_tsquery('portuguese', 'paraná') query WHERE test @@ query ORDER BY score DESC;

select * from data where data.seq=42;