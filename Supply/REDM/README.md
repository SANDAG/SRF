# REDM
Real Estate Development Model, currently targeting SANDAG MGRA level datasets 

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
* Create distributable folder with `pyinstaller redm_main.py`

## Usage
* Add MGRA level data to the `data` folder
   * Ensure that the column labels match those in `data/README.md`
* Configure program inputs in `parameters.yaml`
* Run with `python redm_main.py`
  * Or, run the redm_main executable from the pyinstaller dist folder after following installation steps

## Data Definitions
See `data/README.md`
### MGRA's 
SANDAG uses a multilevel, nested geographic reference system. The foundation of the reference system is the Master Geographic Reference Area (MGRA). The 23,002 MGRAs are the combinations of census blocks, census tracts, community planning areas, city boundaries, spheres of influence, and zip codes. Blocks also are split using other criteria (e.g. ridgelines) to develop traffic analysis zones. Accordingly, MGRAs can aggregate to these standard geographic units, including subregional areas and major statistical areas, which are aggregations of census tracts. Because MGRAs are small, their aggregation can closely approximate any nonstandard or user-specified areas, such as school districts or fire districts. Along with the MGRAs, another geographic boundary system used in the subregional allocation process is the 229 Land Use Zones (LUZ). In general, LUZs represent groups of census tracts. Within the City and County of San Diego, they adhere to community plan area boundaries. For the other jurisdictions, they adhere to current (2012) city boundaries.
