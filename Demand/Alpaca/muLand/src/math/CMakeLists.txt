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

# Math module

# Libraries generated
ADD_LIBRARY(muland_functions ${LIBRARY_BUILD_FLAG} muland_functions.cpp )
ADD_LIBRARY(muland_algorithm ${LIBRARY_BUILD_FLAG} muland_algorithm.cpp )
ADD_LIBRARY(muland_tools     ${LIBRARY_BUILD_FLAG} muland_tools.cpp )

# Dependencies required
TARGET_LINK_LIBRARIES(muland_functions muland_data muland_tools      ${Boost_LIBRARIES})
TARGET_LINK_LIBRARIES(muland_algorithm muland_data muland_functions  ${Boost_LIBRARIES})
TARGET_LINK_LIBRARIES(muland_tools                                   ${Boost_LIBRARIES})

# Installation rules 
set (muland_libraries muland_algorithm muland_functions muland_tools)

set (all_math_libraries 
     muland_algorithm muland_functions  muland_tools
    )


set_target_properties(${all_math_libraries} PROPERTIES 
                      INSTALL_RPATH ${CMAKE_INSTALL_PREFIX}/lib
                      INSTALL_RPATH_USE_LINK_PATH TRUE)

install(TARGETS ${all_math_libraries}
  RUNTIME DESTINATION lib
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib )#EXPORT exported_targets)
