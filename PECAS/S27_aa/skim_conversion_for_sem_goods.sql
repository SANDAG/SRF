drop table if exists {taz_skimtbl};

create table {taz_skimtbl} (
    origin_taz integer,
    destination_taz integer,
    dist_da_t_op double precision,
    time_da_t_op double precision,
    toll_op double precision,
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
		tzs.time_da_t_op + wm.time as time, wm.externalstation
	from {tdm_skimtbl} tzs
	join {worldtbl} wm
	on tzs.destination = wm.externalstation
	order by tzs.origin, wm.worldmarket, tzs.time_da_t_op + wm.time
)
insert into {taz_skimtbl}
select tz3o.origin,
    tz3o.destination,
    tz3o.dist_da_t_op + wm.distance,
    tz3o.time_da_t_op + wm.time,
    tz3o.toll_op,
    xw.luz as o_luz, besttime.worldmarket as d_luz
from {tdm_skimtbl} tz3o
join {taztbl} xw on tz3o.origin = xw.tdm_taz
join besttime on tz3o.origin = besttime.origin and tz3o.destination = besttime.externalstation
join {worldtbl} wm on tz3o.destination = wm.externalstation and besttime.worldmarket = wm.worldmarket
order by o_luz, d_luz, tz3o.origin, tz3o.destination;

with besttime as (select
	tzs.destination, wm.worldmarket, 
		tzs.time_da_t_op + wm.time as time, wm.externalstation
	from {tdm_skimtbl} tzs
	join {worldtbl} wm
	on tzs.origin = wm.externalstation
	order by tzs.destination, wm.worldmarket, tzs.time_da_t_op + wm.time
)
insert into {taz_skimtbl}
select tz3o.origin,
    tz3o.destination,
    tz3o.dist_da_t_op + wm.distance,
    tz3o.time_da_t_op + wm.time,
    tz3o.toll_op,
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
    dist_da_t_op double precision,
    time_da_t_op double precision,
    toll_op double precision,
    primary key (origin, destination)
);

insert into {luz_skimtbl}
select sp.origin_luz, sp.destination_luz,
	case when tot.totflow = 0 then sp.min_dist_da_t_op else sp.dist_da_t_op_sp / tot.totflow end, 
	case when tot.totflow = 0 then sp.min_time_da_t_op else sp.time_da_t_op_sp / tot.totflow end, 
	case when tot.totflow = 0 then sp.min_toll_op else sp.toll_op_sp / tot.totflow end
from
	(select a.origin_luz, a.destination_luz, 
		min(a.dist_da_t_op) as min_dist_da_t_op, sum(a.dist_da_t_op * f.flows) as dist_da_t_op_sp, 
		min(a.time_da_t_op) as min_time_da_t_op, sum(a.time_da_t_op * f.flows) as time_da_t_op_sp, 
		min(a.toll_op) as min_toll_op, sum(a.toll_op * f.flows) as toll_op_sp
	 from {taz_skimtbl} a, {middaytbl} f
		where a.origin_taz = f.i and a.destination_taz = f.j
		group by a.origin_luz, a.destination_luz
	    order by min_time_da_t_op desc
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
