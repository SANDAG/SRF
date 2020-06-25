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

CMAKE_MINIMUM_REQUIRED(VERSION 2.6)
PROJECT(mu-land)

# Project Directories
SET(ROOT_DIR ${PROJECT_SOURCE_DIR}/..)
IF (MINGW)
  SET(LOCAL_INCLUDE ${ROOT_DIR}/local/mingw/include)
  SET(LOCAL_LIB ${ROOT_DIR}/local/mingw/lib)
  SET(INSTALL_DIR ${ROOT_DIR}/local/mingw)
ENDIF()
IF (${CMAKE_SYSTEM_NAME} MATCHES "Linux")
  SET(LOCAL_INCLUDE ${ROOT_DIR}/local/nix/include)
  SET(LOCAL_LIB ${ROOT_DIR}/local/nix/lib)
ENDIF()

SET(LOCAL_PKGS ${ROOT_DIR}/etc)


##############################################################################
# Compilation & Build configuration

# Only use if build is failing ### Automatic Discovery of Headers on Eclipse
SET(CMAKE_VERBOSE_MAKFILE on)
# Type of build ### Verbose debug
SET(CMAKE_BUILD_TYPE DEBUG)

# Project Compiler Flags
SET(CMAKE_CXX_FLAGS "-fPIC -Wall -Wno-long-long -pedantic")

# Debug & TestCoverage
# Added if GCOV is defined -fprofile-arcs -ftest-coverage
SET(CMAKE_CXX_FLAGS_DEBUG "-g3 -O0 -ggdb -Wunused-parameter -Wunused-function -Wunused -Wno-system-headers -Wno-deprecated -Woverloaded-virtual -Wwrite-strings")
# Release
SET(CMAKE_CXX_FLAGS_RELEASE "-O2 -DNDEBUG")

# CDT parse errors
IF(CMAKE_COMPILER_IS_GNUCXX)
  SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fmessage-length=0")
ENDIF(CMAKE_COMPILER_IS_GNUCXX)

# Should i use static or shared libraries?
SET(LIBRARY_BUILD_FLAG STATIC)

##############################################################################
### Mingw specific options
IF(MINGW)
  MESSAGE( STATUS "** Cross compilation with Mingw")
  MESSAGE( STATUS "** 64bit version")
  SET(HOST_OPTIONS      "--host=x86_64-w64-mingw32")
  SET(STDC_LIBRARIES    "/usr/x86_64-w64-mingw32/lib/")
  SET(STDC_INCLUDE_DIR  "/usr/x86_64-w64-mingw32/x86_64-w64-mingw32/include/")
  SET(BOOST_MINGW_PATCH "${LOCAL_PKGS}/user-config-64.patch")
  SET(BOOST_TOOLSET     "gcc-mingw64")
  # Project Compiler Flags
  SET(CMAKE_CXX_FLAGS "-Wall -Wno-long-long -pedantic")
  # Linker Flags
  SET(CMAKE_SHARED_LINKER_FLAGS "-Wl,--enable-auto-import -Wl,--no-undefined -static-libgcc -static-libstdc++")
  SET(CMAKE_EXE_LINKER_FLAGS "-Wl,--enable-auto-import -Wl,--no-undefined -static-libgcc -static-libstdc++")
ENDIF()

##############################################################################
# Cmake Includes
include (ExternalProject)
include (GenerateExportHeader)
##############################################################################
# External Projects
IF(MINGW)
SET(CONFIGURE "<SOURCE_DIR>/configure")
SET(MAKE "make")

SET(BOOST_CONFIGURE "<SOURCE_DIR>/bootstrap.sh")
SET(BOOST_MAKE "<SOURCE_DIR>/b2")

## configure command fails with library log
ExternalProject_Add(
  01_boost-1-54-0
  PREFIX "shared"
  URL ${LOCAL_PKGS}/boost_1_54_0.tar.bz2
  BUILD_IN_SOURCE 1
  PATCH_COMMAND patch -d <SOURCE_DIR> -p1 < ${BOOST_MINGW_PATCH}
  CONFIGURE_COMMAND ${BOOST_CONFIGURE} --prefix=${INSTALL_DIR} --with-toolset=gcc
                    --with-libraries=iostreams,filesystem,system,thread,test 
  BUILD_COMMAND ${BOOST_MAKE} toolset=${BOOST_TOOLSET} target-os=windows link=static runtime-link=static --layout=versioned
  INSTALL_COMMAND ${BOOST_MAKE} install toolset=${BOOST_TOOLSET} target-os=windows link=static runtime-link=static --layout=tagged
)

ENDIF()

##############################################################################

# IF project uses a system/external libraries
# see available modules and usage on http://www.cmake.org/cmake/help/cmake[version]docs.html#section_Standard\ CMake\ Modules
### Find Boost external installation
set(Boost_USE_STATIC_LIBS     ON)
set(Boost_USE_MULTITHREADED   ON)
set(Boost_USE_STATIC_RUNTIME  ON)
set(Boost_ALL_DYN_LINK        OFF) #force dynamic linking for all libraries
set(Boost_DEBUG 1)
IF(MINGW)
#  find_package(Boost COMPONENTS iostreams filesystem system unit_test_framework )
ELSE(MINGW)
  find_package(Boost COMPONENTS iostreams filesystem log log_setup system thread unit_test_framework )
ENDIF()

## Libraries setted 
message( STATUS "** Boost Includes: ${Boost_INCLUDE_DIR} ")
message( STATUS "** Boost Library : ${Boost_LIBRARY_DIRS}")
message( STATUS "** Boost Librares: ${Boost_LIBRARIES}   ")

##############################################################################
# Project Includes
# Order matters! System libraries used before local
INCLUDE_DIRECTORIES(${PROJECT_SOURCE_DIR})
INCLUDE_DIRECTORIES(${Boost_INCLUDE_DIR})
INCLUDE_DIRECTORIES(${STDC_INCLUDE_DIR})
INCLUDE_DIRECTORIES(${LOCAL_INCLUDE})

# Link Directories
IF(MINGW)
  LINK_DIRECTORIES(${LOCAL_LIB} ${STDC_LIBRARIES})
ENDIF()

##############################################################################
# Installation Options
# Installation Prefix
SET (CMAKE_INSTALL_PREFIX "/opt/mu-land")

# use, i.e. don't skip the full RPATH for the build tree
SET(CMAKE_SKIP_BUILD_RPATH  FALSE)
# when building, don't use the install RPATH already
# (but later on when installing)
SET(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE) 
# add the automatically determined parts of the RPATH
# which point to directories outside the build tree to the install RPATH
SET(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

# the RPATH to be used when installing, but only if it's not a system directory
LIST(FIND CMAKE_PLATFORM_IMPLICIT_LINK_DIRECTORIES "${CMAKE_INSTALL_PREFIX}/lib" isSystemDir)
IF("${isSystemDir}" STREQUAL "-1")
  SET(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")
ENDIF("${isSystemDir}" STREQUAL "-1")

MACRO (APPEND_CMAKE_INSTALL_RPATH RPATH_DIRS)
   IF (NOT ${ARGC} EQUAL 1)
     MESSAGE(SEND_ERROR "APPEND_CMAKE_INSTALL_RPATH takes 1 argument")
   ENDIF (NOT ${ARGC} EQUAL 1)
   FOREACH ( RPATH_DIR ${RPATH_DIRS} )
     IF ( NOT ${RPATH_DIR} STREQUAL "" )
        FILE( TO_CMAKE_PATH ${RPATH_DIR} RPATH_DIR )
        STRING( SUBSTRING ${RPATH_DIR} 0 1 RPATH_FIRST_CHAR )
        IF ( NOT ${RPATH_FIRST_CHAR} STREQUAL "/" )
          # relative path; CMake handling for these is unclear,
          # add them directly to the linker line. Add both $ORIGIN
          # and $$ORIGIN to ensure correct behavior for exes and
          # shared libraries.
          SET ( RPATH_DIR "$ORIGIN/${RPATH_DIR}:$$ORIGIN/${RPATH_DIR}" )
          SET ( CMAKE_EXE_LINKER_FLAGS
                "${CMAKE_EXE_LINKER_FLAGS} -Wl,-rpath,'${RPATH_DIR}'" )
          SET ( CMAKE_SHARED_LINKER_FLAGS
                "${CMAKE_SHARED_LINKER_FLAGS} -Wl,-rpath,'${RPATH_DIR}'" )
        ELSE ( NOT ${RPATH_FIRST_CHAR} STREQUAL "/" )
          # absolute path
          SET ( CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_RPATH}:${RPATH_DIR}" )
        ENDIF ( NOT ${RPATH_FIRST_CHAR} STREQUAL "/" )
     ENDIF ( NOT ${RPATH_DIR} STREQUAL "" )
   ENDFOREACH ( RPATH_DIR )
ENDMACRO ( APPEND_CMAKE_INSTALL_RPATH )

#fix library rpath
IF(UNIX)
  APPEND_CMAKE_INSTALL_RPATH(".;../lib;../shared/lib")
ENDIF(UNIX)


IF(MINGW)
  SET (EXTERNAL_BOOST_LIBRARIES 
  "${LOCAL_LIB}/libboost_iostreams-mt-s.a"
  "${LOCAL_LIB}/libboost_filesystem-mt-s.a"
  "${LOCAL_LIB}/libboost_system-mt-s.a"
  )
  SET (external_libraries ${EXTERNAL_BOOST_LIBRARIES} )
  set (Boost_LIBRARIES ${EXTERNAL_BOOST_LIBRARIES})
message( STATUS "** Boost Includes: ${Boost_INCLUDE_DIR}")
message( STATUS "** Boost Library: ${Boost_LIBRARY_DIRS}")
message( STATUS "** Boost Libraries: ${Boost_LIBRARIES}")
ELSE(MINGW)
  SET (EXTERNAL_BOOST_LIBRARIES
    ${Boost_IOSTREAMS_LIBRARY_RELEASE}
    ${Boost_FILESYSTEM_LIBRARY_RELEASE}
    ${Boost_LOG_LIBRARY_RELEASE}
    ${Boost_LOG_SETUP_LIBRARY_RELEASE}
    ${Boost_SYSTEM_LIBRARY_RELEASE}
    ${Boost_THREAD_LIBRARY_RELEASE}
    ${Boost_UNIT_TEST_FRAMEWORK_LIBRARY_RELEASE}
    )
  set (external_libraries ${EXTERNAL_BOOST_LIBRARIES} )
ENDIF()

##############################################################################

# Sources
# I/O module
ADD_SUBDIRECTORY(io)
# Main executable
ADD_SUBDIRECTORY(main)
# Algorithm module
ADD_SUBDIRECTORY(math)
# Data  module 
ADD_SUBDIRECTORY(data)
# Solver module
ADD_SUBDIRECTORY(solver)

