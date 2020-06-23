Build Instructions:

The only dependency required is boost-1.54 or superior preinstalled on the system.

On unix/linux systems
- `sh builder.sh -u`  : This will generate the build directory from the sources.
- `cd build && make`  : This will build the binary 
- `sudo make install` : Will create a portable binary on the directory /opt/mu-land/bin/

The windows 64bit version requires mingw64 for cross compile.
- `sh builder.sh -m 64 -u` : This will generate the build-w64 directory from the sources.
- `cd build-w64 && cp -r ../local/nix/include/m2l ../local/mingw/include` : copy the m2l files to the local/mingw files before making
- `make`  : This will build the binary 
- `sudo make install` : Will create a portable binary for windows on the directory /opt/mu-land/bin/

