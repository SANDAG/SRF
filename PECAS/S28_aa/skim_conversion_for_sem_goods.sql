drop table if exists {taz_skimtbl};

create table {taz_skimtbl} 
as
select a.origin as origin_taz, a.destination as destination_taz,
a.dist_da_t_op,  a.time_da_t_op, a.toll_op, b.luz as origin_luz, c.luz as destination_luz
from {tdm_skimtbl} a
join {taztbl} b on a.origin = b.tdm_taz
join {taztbl} c on a.destination = c.tdm_taz;



-- append externals
-- External zones, use the best one for the world market
insert into {taz_skimtbl}
select tz3o.origin,
    tz3o.destination,
    tz3o.dist_da_t_op + wm.distance,
    tz3o.time_da_t_op + wm.time,
    tz3o.toll_op,
    xw.luz as o_luz, wm.worldmarket as d_luz
from {tdm_skimtbl} tz3o
join {taztbl} xw on tz3o.origin = xw.tdm_taz
join {worldtbl} wm on tz3o.destination = wm.externalstation 
order by o_luz, d_luz, tz3o.origin, tz3o.destination;

insert into {taz_skimtbl}
select tz3o.origin,
    tz3o.destination,
    tz3o.dist_da_t_op + wm.distance,
    tz3o.time_da_t_op + wm.time,
    tz3o.toll_op,
    wm.worldmarket as o_luz, xw.luz as d_luz
from {tdm_skimtbl} tz3o
join {taztbl} xw on tz3o.destination = xw.tdm_taz
join {worldtbl} wm on tz3o.origin = wm.externalstation 
order by o_luz, d_luz, tz3o.origin, tz3o.destination;

alter table {taz_skimtbl} add primary key(origin_taz, destination_taz, origin_luz, destination_luz);
analyze {taz_skimtbl};

-- BREAK

drop table if exists {luz_skimtbl};

create table {luz_skimtbl} 
as 
select a.origin_luz as origin, a.destination_luz as destination, 
case when sum(f."flows")<=0 then min(a.dist_da_t_op) else sum(a.dist_da_t_op * f.flows)/sum(f."flows") end as  dist_da_t_op,
case when sum(f."flows")<=0 then min(a.time_da_t_op) else sum(a.time_da_t_op * f.flows)/sum(f."flows") end as time_da_t_op,
case when sum(f."flows")<=0 then min(a.toll_op) else sum(a.toll_op * f.flows)/sum(f."flows") end as toll_op
from  {taz_skimtbl} a join {middaytbl} f
 on a.origin_taz = f.i and a.destination_taz = f.j
 where a.origin_luz>0 and  a.destination_luz>0
		group by a.origin_luz, a.destination_luz;

alter table {luz_skimtbl} add primary key(origin, destination);
analyze {luz_skimtbl};

