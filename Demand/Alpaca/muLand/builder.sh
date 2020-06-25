#!/bin/bash

# Directories prefixes
PROJECT_DIR=`pwd`
BUILD_DIR=$PROJECT_DIR/build
SOURCE_DIR=$PROJECT_DIR/src
PREFIX_DIR=$PROJECT_DIR/local
LIB_DIR=$PREFIX_DIR/lib
HEADER_DIR=$PREFIX_DIR/include
PKG_DIR=$PROJECT_DIR/etc/pkg


echo 'Generating build directory with CMake ...';
case $OSTYPE in
  darwin* )
  CMAKE_PROJECT="-G\"Xcode\""
  ;;
  linux*)
  CMAKE_PROJECT="-G\"Unix Makefiles\""
  ;;
esac


while getopts ":m:gu" optname
    do 
      case "$optname" in 
        m)
          echo "Mingw option given: Cross compilation activated with $OPTARG"
          case $OPTARG in 
            32)
              echo "32 bit toolchain DEPRECATED"
              ;;
            64)
              echo "64 bit toolchain selected"
              CMAKE_TOOLCHAIN="-DCMAKE_TOOLCHAIN_FILE=$SOURCE_DIR/cmake_extras/toolchain-mingw-64.cmake";
              BUILD_DIR=$PROJECT_DIR/build-w64
              CMAKE_OPTIONS="$CMAKE_TOOLCHAIN -D64B=1 -DGCOV=0"
              ;;
            esac
          CMAKE_OPTIONS="$CMAKE_OPTIONS -DBoost_NO_BOOST_CMAKE=TRUE -DBoost_NO_SYSTEM_PATHS=TRUE -DBOOST_ROOT=$PREFIX_DIR/mingw -DBoost_LIBRARY_DIRS=${PREFIX_DIR}/mingw/lib -DBoost_INCLUDE_DIR=${PREFIX_DIR}/mingw/include"
          ENVIRONMENT_CMAKE="BOOST_ROOT=$PREFIX_DIR/mingw GDAL_ROOT=$PREFIX_DIR/mingw"
          ;;
        g)
          echo "Compiling with testcoverage option"
          CMAKE_OPTIONS="$CMAKE_OPTIONS -DGCOV=1"
          ;;
        u)
          echo "Override OSTYPE: Generating UNIX MAKE FILES"
          CMAKE_PROJECT="-G\"Unix Makefiles\""
          ;;
        \?)
          echo "Unknown option $OPTARG"
          ;;
        :)
          echo "No argument value for option $OPTARG"
         ;;
        *)
          # Should not occur
          echo "Unknown error while processing options"
          ;;
      esac
    done

## always recreate build directory
if [ -d $BUILD_DIR ];
#	then rm -rf $BUILD_DIR;
then
  echo "build directory already exists";

  else mkdir $BUILD_DIR;
fi

CMAKE_COMMAND="cd $BUILD_DIR && $ENVIRONMENT_CMAKE cmake $CMAKE_PROJECT $CMAKE_TOOLCHAIN $CMAKE_OPTIONS $SOURCE_DIR && cd $PROJECT_DIR"
echo $CMAKE_OPTIONS

eval $CMAKE_COMMAND
