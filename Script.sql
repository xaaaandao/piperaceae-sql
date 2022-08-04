drop table data;

truncate
	table data;

alter table data add column test tsvector;

update
	data set
	test = setweight(to_tsvector('portuguese', coalesce(data.country, '')), 'A') ||
setweight(to_tsvector('portuguese', coalesce(data.state_province, '')), 'B') ||
setweight(to_tsvector('portuguese', coalesce(data.county, '')), 'C');

create index if not exists idx_test on
data
	using gin(test);
--SELECT seq, ts_rank(test, query) AS score FROM data, to_tsquery('portuguese', 'paraná') query WHERE test @@ query ORDER BY score DESC;

select
	seq,
	ts_rank(test, query) as score
from
	data,
	to_tsquery('portuguese', 'Paraná') query
where
	test @@ query
order by
	score desc;

select
	seq,
	ts_rank(test, query) as score
from
	data,
	to_tsquery('portuguese', 'Paraná') query
where
	test @@ query
order by
	score;

select
	seq,
	ts_rank(test, query) as score
from
	data,
	to_tsquery('portuguese', 'Paraná') query
where
	test @@ query
order by
	score;

select
	distinct (ts_rank(test, query)) as score
from
	data,
	to_tsquery('portuguese', 'Paraná') query
where
	test @@ query;

select
	data.seq,
	data.county,
	data.state_province,
	data.country,
	data.test
from
	data;
	
select count(*) from data;

select * from data;
