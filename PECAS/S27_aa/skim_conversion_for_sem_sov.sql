drop table if exists {taz_skimtbl};

create table {taz_skimtbl} (
    origin_taz integer,
    destination_taz integer,
    am_sov_tr_m_dist double precision,
    am_sov_tr_m_time double precision,
    am_sov_tr_m_tollcost double precision,
    origin_luz integer,
    destination_luz integer,
    primary key (origin_taz, destination_taz, origin_luz, destination_luz)
);

create index on {taz_skimtbl} (origin_taz);
create index on {taz_skimtbl} (destination_taz);
create index on {taz_skimtbl} (origin_luz);
create index on {taz_skimtbl} (destination_luz);

insert into {taz_skimtbl}
select a.*, b.luz, c.luz
from {tdm_skimtbl} a
join {taztbl} b on a.origin = b.tdm_taz
join {taztbl} c on a.destination = c.tdm_taz;

-- append externals
-- External zones, use the best one for the world market
with besttime as (select
	tzs.origin, wm.worldmarket, 
		tzs.am_sov_tr_m_time + wm.time as time, wm.externalstation
	from {tdm_skimtbl} tzs
	join {worldtbl} wm
	on tzs.destination = wm.externalstation
	order by tzs.origin, wm.worldmarket, tzs.am_sov_tr_m_time + wm.time
)
insert into {taz_skimtbl}
select tz3o.origin,
    tz3o.destination,
    tz3o.am_sov_tr_m_dist + wm.distance,
    tz3o.am_sov_tr_m_time + wm.time,
    tz3o.am_sov_tr_m_tollcost,
    xw.luz as o_luz, besttime.worldmarket as d_luz
from {tdm_skimtbl} tz3o
join {taztbl} xw on tz3o.origin = xw.tdm_taz
join besttime on tz3o.origin = besttime.origin and tz3o.destination = besttime.externalstation
join {worldtbl} wm on tz3o.destination = wm.externalstation and besttime.worldmarket = wm.worldmarket
order by o_luz, d_luz, tz3o.origin, tz3o.destination;

with besttime as (select
	tzs.destination, wm.worldmarket, 
		tzs.am_sov_tr_m_time + wm.time as time, wm.externalstation
	from {tdm_skimtbl} tzs
	join {worldtbl} wm
	on tzs.origin = wm.externalstation
	order by tzs.destination, wm.worldmarket, tzs.am_sov_tr_m_time + wm.time
)
insert into {taz_skimtbl}
select tz3o.origin,
    tz3o.destination,
    tz3o.am_sov_tr_m_dist + wm.distance,
    tz3o.am_sov_tr_m_time + wm.time,
    tz3o.am_sov_tr_m_tollcost,
    besttime.worldmarket as o_luz, xw.luz as d_luz
from {tdm_skimtbl} tz3o
join {taztbl} xw on tz3o.destination = xw.tdm_taz
join besttime on tz3o.destination = besttime.destination and tz3o.origin = besttime.externalstation
join {worldtbl} wm on tz3o.origin = wm.externalstation and besttime.worldmarket = wm.worldmarket
order by o_luz, d_luz, tz3o.origin, tz3o.destination;

-- BREAK

drop table if exists {luz_skimtbl};

create table {luz_skimtbl} (
    origin integer,
    destination integer,
    am_sov_tr_m_dist double precision,
    am_sov_tr_m_time double precision,
    am_sov_tr_m_tollcost double precision,
    primary key (origin, destination)
);

insert into {luz_skimtbl}
select sp.origin_luz, sp.destination_luz,
	case when tot.totflow = 0 then sp.min_am_sov_tr_m_dist else sp.am_sov_tr_m_dist_sp / tot.totflow end, 
	case when tot.totflow = 0 then sp.min_am_sov_tr_m_time else sp.am_sov_tr_m_time_sp / tot.totflow end, 
	case when tot.totflow = 0 then sp.min_am_sov_tr_m_tollcost else sp.am_sov_tr_m_tollcost_sp / tot.totflow end
from
	(select a.origin_luz, a.destination_luz,
		min(a.am_sov_tr_m_dist) as min_am_sov_tr_m_dist, sum(a.am_sov_tr_m_dist * f.flows) as am_sov_tr_m_dist_sp, 
		min(a.am_sov_tr_m_time) as min_am_sov_tr_m_time, sum(a.am_sov_tr_m_time * f.flows) as am_sov_tr_m_time_sp, 
		min(a.am_sov_tr_m_tollcost) as min_am_sov_tr_m_tollcost, sum(a.am_sov_tr_m_tollcost * f.flows) as am_sov_tr_m_tollcost_sp
	 from {taz_skimtbl} a, {middaytbl} f
		where a.origin_taz = f.i and a.destination_taz = f.j
		group by a.origin_luz, a.destination_luz
	    order by min_am_sov_tr_m_time desc
	) sp,
	(select a.origin_luz, a.destination_luz, 
		sum(f."flows") as totflow
	 from {taz_skimtbl} a, {middaytbl} f
		where a.origin_taz = f.i and a.destination_taz = f.j
		group by a.origin_luz, a.destination_luz) tot
where sp.origin_luz = tot.origin_luz and
sp.destination_luz = tot.destination_luz
and sp.origin_luz > 0
and sp.destination_luz > 0;
