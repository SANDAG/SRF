#*******************************************************************************
#*            Micro Land (mu-land) - Land Use Model 
#*                     Copyright 2016 by
#*
#*          Felipe Saavedra C. (fsaavedr@dcc.uchile.cl)
#*
#*
#*  This file is part of Micro Land (mu-land)
#*
#*  Mu-Land is free software: you can redistribute it and/or modify
#*  it under the terms of the GNU General Public License as published by
#*  the Free Software Foundation, either version 3 of the License, or
#*  (at your option) any later version.
#*
#*  Mu-Land is distributed in the hope that it will be useful,
#*  but WITHOUT ANY WARRANTY; without even the implied warranty of
#*  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#*  GNU General Public License for more details.
#*
#*  You should have received a copy of the GNU General Public License
#*  along with Mu-Land.  If not, see <http://www.gnu.org/licenses/>.
#*
#******************************************************************************/

# Solver module

# Libraries generated
ADD_LIBRARY(muland_configurator ${LIBRARY_BUILD_FLAG} configurator.cpp)
ADD_LIBRARY(m2l_solver       ${LIBRARY_BUILD_FLAG} solver.cpp)

GENERATE_EXPORT_HEADER ( muland_configurator
  BASE_NAME muland_configurator
  EXPORT_MACRO_NAME muland_configurator_EXPORT
  EXPORT_FILE_NAME muland_configurator_Export.h
  STATIC_DEFINE muland_configurator_BUILT_AS_STATIC
)

 GENERATE_EXPORT_HEADER ( m2l_solver
  BASE_NAME m2l_solver
  EXPORT_MACRO_NAME m2l_solver_EXPORT
  EXPORT_FILE_NAME m2l_solver_Export.h
  STATIC_DEFINE m2l_solver_BUILT_AS_STATIC
)

#add_compiler_export_flags()

# Libraries dependencies
TARGET_LINK_LIBRARIES(muland_configurator
  muland_data 
  txt_datafile_reader
  muland_tools
  ${Boost_LIBRARIES} 
  )
TARGET_LINK_LIBRARIES(m2l_solver
  muland_tools
  muland_configurator 
  muland_data 
  muland_algorithm 

  ${Boost_LIBRARIES})


# Installation rules 
set (solver_libraries muland_configurator m2l_solver)

set_target_properties(${solver_libraries} PROPERTIES 
                      INSTALL_RPATH ${CMAKE_INSTALL_PREFIX}/lib
                      INSTALL_RPATH_USE_LINK_PATH TRUE)

install(TARGETS ${solver_libraries}
  RUNTIME DESTINATION lib
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib)# EXPORT exported_targets)
  
