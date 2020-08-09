
drop table if exists {taz_skimtbl};

create table {taz_skimtbl} as
select distinct on (origin, destination)
origin, destination, am_allpen_totalivtt, am_allpen_totalwait,
am_allpen_totalwalk + origin_access + destination_access as am_allpen_totalwalk,
am_allpen_xfers
from
(
	select oa.origin, oa.origin_station, da.destination_station, da.destination,
	oa.access_skim as origin_access, da.access_skim as destination_access,
	ss.am_allpen_totalivtt, ss.am_allpen_totalwait, ss.am_allpen_totalwalk, ss.am_allpen_xfers
	from
	(
		select origin, origin_station, access_skim from 
		(
			select ac.origin, st.station as origin_station, ac.access_skim, min(ac.access_skim) over (partition by ac.origin) as shortest_access
			from {access_skimtbl} ac
			join {stationtbl} st
			on st.taz = ac.destination
		) oa
		where access_skim = shortest_access
	) oa
	join {station_skimtbl} ss
	using (origin_station)
	join
	(
		select destination_station, destination, access_skim from
		(
			select st.station as destination_station, ac.destination, ac.access_skim, min(ac.access_skim) over (partition by ac.destination) as shortest_access
			from {access_skimtbl} ac
			join {stationtbl} st
			on st.taz = ac.origin
		) da
		where access_skim = shortest_access
	) da
	using (destination_station)
) sub
order by origin, destination, am_allpen_totalivtt + am_allpen_totalwait + am_allpen_totalwalk;
