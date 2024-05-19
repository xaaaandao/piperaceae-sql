select le.genus_old, le.specific_epithet_old, le.genus, le.specific_epithet,
       lo.country_old, lo.country, lo.county_old, lo.county, lo.state_province_old, lo.state_province
from exsiccata e
         join level le on le.id=e.level_id
         join local lo on lo.id=e.local_id
where e.seq=47016;

truncate table datasets;

select (le.genus, le.specific_epithet), count(*) as total
from exsiccata e
         join local lo on lo.id=e.local_id
         join level le on le.id=e.level_id
         join identifier i on i.id=e.identifier_id
         join trusted_identifier ti on ti.value_founded=i.identified_by
where
    (lo.county in (select c.name from county c) or
     lo.state_province in (select s.name from state s) or
     lo.country='Brasil') and
    ti.selected and
    (le.genus is not null and le.specific_epithet is not null)
group by (le.genus, le.specific_epithet)
having count((le.genus, le.specific_epithet)) >= 5;

select sum(t.total) from (select (le.genus, le.specific_epithet), count(*) as total
                          from exsiccata e
                                   join local lo on lo.id=e.local_id
                                   join level le on le.id=e.level_id
                                   join identifier i on i.id=e.identifier_id
                                   join trusted_identifier ti on ti.value_founded=i.identified_by
                          where
                              (lo.county in (select c.name from county c) or
                               lo.state_province in (select s.name from state s) or
                               lo.country='Brasil') and
                              ti.selected and
                              (le.genus is not null and le.specific_epithet is not null)
                          group by (le.genus, le.specific_epithet)
                          having count((le.genus, le.specific_epithet)) >= 5) as t;


