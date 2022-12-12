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

select count(dti.barcode)
    from data_trusted_identifier dti
    where dti.country_trusted = 'Brasil' and
    dti.specific_epithet is not null and
    (dti.state_province in (select distinct (c.uf) from county c) or
     dti.state_province in (select distinct (c.state) from county c) or
     dti.locality like any (select distinct (concat('%', c.state, '%')) from county c));

select count(dti.barcode)
    from data_trusted_identifier dti
    where dti.country_trusted = 'Brasil' and
    dti.specific_epithet is not null and
    (dti.state_province in (select distinct (c.uf) from county c) or
     dti.state_province in (select distinct (c.state) from county c));


select dti.state_province, dti.county
    from data_trusted_identifier dti
    where dti.country_trusted = 'Brasil' and
    dti.specific_epithet is not null and
    dti.state_province is not null and
    dti.county is not null and dti.barcode not in
    ( select dti.barcode
        from data_trusted_identifier dti
        where dti.country_trusted = 'Brasil' and
        dti.specific_epithet is not null and
        (dti.state_province in (select distinct (c.uf) from county c) or
         dti.state_province in (select distinct (c.state) from county c))
    );

select count(distinct(dti.barcode))
    from data_trusted_identifier dti
    where dti.country_trusted = 'Brasil' and
    dti.specific_epithet is not null and
    (unaccent(lower(dti.state_province))  in (select distinct (unaccent(lower(c.uf))) from county c) or
     unaccent(lower(dti.state_province)) in (select distinct (unaccent(lower(c.state))) from county c));

select count(distinct(dti.barcode))
    from data_trusted_identifier dti
    where dti.country_trusted = 'Brasil' and
    dti.specific_epithet is not null and
    (unaccent(lower(dti.state_province))  in (select distinct (unaccent(lower(c.uf))) from county c) or
     unaccent(lower(dti.state_province)) in (select distinct (unaccent(lower(c.state))) from county c) or
     unaccent(lower(dti.locality)) like any (select distinct (concat('%', unaccent(lower(c.state)), '%')) from county c));