drop table if exists {taz_skimtbl};

create table {taz_skimtbl} as
select a.origin as origin_taz, a.destination as destination_taz,
a.am_allpen_totalivtt, a.am_allpen_totalwait, a.am_allpen_totalwalk, a.am_allpen_xfers,
b.luz as origin_luz, c.luz as destination_luz
from {tdm_skimtbl} a
join {taztbl} b on a.origin = b.tdm_taz
join {taztbl} c on a.destination = c.tdm_taz;


-- append externals
-- External zones, use the best one for the world market
--insert into {taz_skimtbl}
--select tz3o.origin,
--    tz3o.destination,
--    tz3o.am_allpen_totalivtt + wm.time,
--    tz3o.am_allpen_totalwait,
--    tz3o.am_allpen_totalwalk,
--    tz3o.am_allpen_xfers,
--    xw.luz as o_luz, wm.worldmarket as d_luz
--from {tdm_skimtbl} tz3o
--join {taztbl} xw on tz3o.origin = xw.tdm_taz
--join {worldtbl} wm on tz3o.destination = wm.externalstation 
--order by o_luz, d_luz, tz3o.origin, tz3o.destination;

--insert into {taz_skimtbl}
--select tz3o.origin,
--    tz3o.destination,
--    tz3o.am_allpen_totalivtt + wm.time,
--    tz3o.am_allpen_totalwait,
--    tz3o.am_allpen_totalwalk,
--    tz3o.am_allpen_xfers,
--    wm.worldmarket as o_luz, xw.luz as d_luz
--from {tdm_skimtbl} tz3o
--join {taztbl} xw on tz3o.destination = xw.tdm_taz
--join {worldtbl} wm on tz3o.origin = wm.externalstation 
--order by o_luz, d_luz, tz3o.origin, tz3o.destination;

alter table {taz_skimtbl} add primary key(origin_taz, destination_taz, origin_luz, destination_luz);
analyze {taz_skimtbl};

-- BREAK

drop table if exists {luz_skimtbl};

create table {luz_skimtbl} 
as
select a.origin_luz as origin, a.destination_luz as destination,
case when sum(f."flows")=0 then min(a.am_allpen_totalivtt) else sum(a.am_allpen_totalivtt * f.flows)/sum(f."flows") end as am_allpen_totalivtt,
case when sum(f."flows")=0 then min(a.am_allpen_totalwait) else sum(a.am_allpen_totalwait * f.flows)/sum(f."flows") end as am_allpen_totalwait,
case when sum(f."flows")=0 then min(a.am_allpen_totalwalk) else sum(a.am_allpen_totalwalk * f.flows)/sum(f."flows") end as am_allpen_totalwalk,
case when sum(f."flows")=0 then min(a.am_allpen_xfers) else sum(a.am_allpen_xfers * f.flows)/sum(f."flows") end  as am_allpen_xfers
from {taz_skimtbl} a join {middaytbl} f
on a.origin_taz = f.i and a.destination_taz = f.j
where a.origin_luz>0 and a.destination_luz>0
group by a.origin_luz, a.destination_luz
;

alter table {luz_skimtbl} add primary key(origin, destination);
analyze {luz_skimtbl};
