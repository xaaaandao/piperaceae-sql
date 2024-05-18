select (le.genus, le.specific_epithet), array_agg(e.seq) from exsiccata e
                                                                  join identifier i on e.identifier_id=i.id
                                                                  join level le on e.level_id=le.id
                                                                  join local lo on e.local_id=lo.id
                                                                  join trusted_identifier ti on ti.value_founded = i.identified_by
where ti.selected and
    (lo.country='Brasil' or (lo.country is null and lo.state_province is not null and lo.county is not null)) and
    le.specific_epithet is not null and le.genus is not null
group by le.genus, le.specific_epithet
having count(*) >= 5;