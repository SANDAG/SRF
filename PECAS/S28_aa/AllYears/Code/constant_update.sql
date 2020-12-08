--
delete from transition_constants_i_calib;
delete from transition_constants_i_calib;
copy transition_constants_i_calib from 'D:/PECASScag/W00/AllYears/Inputs/transition_constants_i.csv' csv header;
update transition_constants_i p
set transition_constant = q.transition_constant 
from transition_constants_i_calib q
where p.from_space_type_id = q.from_space_type_id and p.to_space_type_id = q.to_space_type_id;


delete from space_types_i_calib ;

copy space_types_i_calib from 'D:/PECASScag/W00/AllYears/Inputs/space_types_i.csv' csv header;

update space_types_i p
set 
  add_transition_const = q.add_transition_const,  new_transition_const = q.new_transition_const,
  renovate_transition_const = q.renovate_transition_const,
  demolish_transition_const = q.demolish_transition_const,
  derelict_transition_const = q.derelict_transition_const,
  no_change_transition_const = q.no_change_transition_const,
  new_type_dispersion_parameter=q.new_type_dispersion_parameter,
  gy_dispersion_parameter = q.gy_dispersion_parameter,
  gz_dispersion_parameter = q.gz_dispersion_parameter,
  gw_dispersion_parameter = q.gw_dispersion_parameter,
  gk_dispersion_parameter = q.gk_dispersion_parameter,
  nochange_dispersion_parameter = q.nochange_dispersion_parameter,
  intensity_dispersion_parameter = q.intensity_dispersion_parameter
from space_types_i_calib q
where p.space_type_id = q.space_type_id;
