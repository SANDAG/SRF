# REDM
Real Estate Development Model; targeting SANDAG MGRA level datasets 

## Recommended System Requirements 
* OS:
   * Windows 10 64 bit, MacOS 10.15.4 or greater, or a GNU/Linux that can run python 3.6 or higher, `ldd`, `objdump` and `objcopy`
* Hard Disk Space:
   * 4 times total model file size times the number of simulation years (SSD preferred)
     * for example: 4 x 300MB model x 35 simulation years = 42GB minimum
* RAM:
   * 8 GB, or 4x total model file size, whichever is greater
* Processor:
   * Intel i5-2400 or equivalent, or better

### System requirements notes
We will use pyinstaller to create distributable software, this works with any specific OS, as long as pyinstaller is run on a matching OS. The operating systems listed are those available for us to build on.

## Installation
* Test with `python redm_main.py -t`
* Create distributable with `pyinstaller redm_main.py`

