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

##############################################################################
INCLUDE(CMakeForceCompiler)
### Cross Compiling Options
SET (CMAKE_SYSTEM_NAME Windows) 
SET (CMAKE_C_COMPILER   /usr/bin/x86_64-w64-mingw32-gcc)
SET (CMAKE_CXX_COMPILER /usr/bin/x86_64-w64-mingw32-g++)
SET (CMAKE_RC_COMPILER  /usr/bin/x86_64-w64-mingw32-windres)
# CMAKE_AR and CMAKE_RANLIB are auto configurated



