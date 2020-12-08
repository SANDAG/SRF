drop table if exists {taz_skimtbl};

create table {taz_skimtbl} as
select a.origin as origin_taz, a.destination as destination_taz,
a.am_sov_tr_m_dist, a.am_sov_tr_m_time, a.am_sov_tr_m_tollcost, 
b.luz as origin_luz, c.luz as destination_luz
from {tdm_skimtbl} a
join {taztbl} b on a.origin = b.tdm_taz
join {taztbl} c on a.destination = c.tdm_taz;

-- append externals
-- External zones, use the best one for the world market

insert into {taz_skimtbl}
select tz3o.origin,
    tz3o.destination,
    tz3o.am_sov_tr_m_dist + wm.distance,
    tz3o.am_sov_tr_m_time + wm.time,
    tz3o.am_sov_tr_m_tollcost,
    xw.luz as o_luz, wm.worldmarket as d_luz
from {tdm_skimtbl} tz3o
join {taztbl} xw on tz3o.origin = xw.tdm_taz
join {worldtbl} wm on tz3o.destination = wm.externalstation 
order by o_luz, d_luz, tz3o.origin, tz3o.destination;

insert into {taz_skimtbl}
select tz3o.origin,
    tz3o.destination,
    tz3o.am_sov_tr_m_dist + wm.distance,
    tz3o.am_sov_tr_m_time + wm.time,
    tz3o.am_sov_tr_m_tollcost,
    wm.worldmarket as o_luz, xw.luz as d_luz
from {tdm_skimtbl} tz3o
join {taztbl} xw on tz3o.destination = xw.tdm_taz
join {worldtbl} wm on tz3o.origin = wm.externalstation 
order by o_luz, d_luz, tz3o.origin, tz3o.destination;

alter table {taz_skimtbl} add primary key(origin_taz, destination_taz, origin_luz, destination_luz);
analyze {taz_skimtbl};


-- BREAK

drop table if exists {luz_skimtbl};

Create table  {luz_skimtbl} 
as
select a.origin_luz as origin, a.destination_luz as destination,
		case when sum(f."flows")<=0 then min(a.am_sov_tr_m_dist) else sum(a.am_sov_tr_m_dist * f.flows)/sum(f."flows") end as am_sov_tr_m_dist, 
		case when sum(f."flows")<=0 then min(a.am_sov_tr_m_time) else sum(a.am_sov_tr_m_time * f.flows)/sum(f."flows") end as am_sov_tr_m_time, 
		case when sum(f."flows")<=0 then min(a.am_sov_tr_m_tollcost) else sum(a.am_sov_tr_m_tollcost * f.flows)/sum(f."flows") end as am_sov_tr_m_tollcost
	 from {taz_skimtbl} a join {middaytbl} f
		on a.origin_taz = f.i and a.destination_taz = f.j 
	 where a.origin_luz>0 and a.destination_luz>0
		group by a.origin_luz, a.destination_luz;

alter table {luz_skimtbl} add primary key(origin, destination);
analyze {luz_skimtbl};

