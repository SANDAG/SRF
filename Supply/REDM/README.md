# REDM

Real Estate Development Model, currently targeting SANDAG MGRA level datasets

## Recommended System Requirements

- OS:
  - Windows 10 64 bit, MacOS 10.15.4 or greater, or a GNU/Linux that can run python 3.6 or higher, `ldd`, `objdump` and `objcopy`
- Hard Disk Space:
  - 4 times total model file size times the number of simulation years (SSD preferred)
    - for example: 4 x 300MB model x 35 simulation years = 42GB minimum
- RAM:
  - 8 GB, or 4x total model file size, whichever is greater
- Processor:
  - Intel i5-2400 or equivalent, or better

### System requirements notes

We will use pyinstaller to create distributable software, this works with any specific OS, as long as pyinstaller is run on a matching OS. The operating systems listed are those available for us to build on.

## Installation

- Test with `python redm_main.py -t`
- Create distributable folder with `pyinstaller redm_main.py`

## Usage

- Add MGRA level data to the `data` folder
  - Ensure that the column labels match those in `data/README.md`
- Configure program inputs in `parameters.yaml`
- Run with `python redm_main.py`
  - Or, run the redm_main executable from the pyinstaller dist folder after following installation steps

## Data Explanations

See `data/README.md`

### MGRA's

SANDAG uses a multilevel, nested geographic reference system. The foundation of the reference system is the Master Geographic Reference Area (MGRA). The 23,002 MGRAs are the combinations of census blocks, census tracts, community planning areas, city boundaries, spheres of influence, and zip codes. Blocks also are split using other criteria (e.g. ridgelines) to develop traffic analysis zones. Accordingly, MGRAs can aggregate to these standard geographic units, including subregional areas and major statistical areas, which are aggregations of census tracts. Because MGRAs are small, their aggregation can closely approximate any nonstandard or user-specified areas, such as school districts or fire districts. Along with the MGRAs, another geographic boundary system used in the subregional allocation process is the 229 Land Use Zones (LUZ). In general, LUZs represent groups of census tracts. Within the City and County of San Diego, they adhere to community plan area boundaries. For the other jurisdictions, they adhere to current (2012) city boundaries.

## Interface

### Inputs

REDM accepts a .csv file and requires these columns:

- MGRA Series 13 MGRA (Master Geographic Reference Area)
- Shape_Area area of MGRA object (square footage)
- SqFt_SF total squarefootage of single-family units
- SqFt_MF total squarefootage of multiple-family units
- Land_Cost cost of land per acre
- Price_SF price/rent cost per square foot for single family dwelling
- Price_MF price/rent cost per square foot for multi family dwelling
- hs Housing units
- hs_sf Single-family housing units
- hs_mf Multiple-family housing units
- hh Households (occupied housing units)
- hh_sf Single-family households (occupied housing units)
- hh_mf Multiple-family households (occupied housing units)
- emp*indus* Employment in industrial land uses
- emp_comm_l Employment in commercial land uses
- emp_office Employment in office land uses
- emp*other* Employment in other land uses
- dev_sf acres developed as single family residential; detached housing units on lots smaller than one acre
- dev_mf acres developed as multiple family residential
- dev_indus acres developed as industrial, wholesale trade, airport, rail station, communications and utilities, center city parking, park and ride lots, other transportation, or marine terminals
- dev_comm acres developed as retail trade, hotels/motels/resorts, public services, hospitals, or commercial recreation
- dev_office acres developed as offices
- vac_sf undeveloped acres planned for single family residential
- vac_mf undeveloped acres planned for multiple family residential
- vac_oth undeveloped acres planned for group quarters residential
- vac_indus undeveloped acres planned for industrial, wholesale trade, airport, rail station, communications and utilities, center city parking, park and ride lots, other transportation, or marine terminals
- vac_comm undeveloped acres planned for retail trade, hotels/motels/resorts, public services, hospitals, or commercial recreation
- vac_office undeveloped acres planned for offices
- acres total acres
- dev total developed acres
- vac total vacant acres
- unusable vacant land not available for development for physical, public policy, or environmental reasons
- DUA dwelling units per acre
- Cap_HS housing stock (dwelling unit) capacity
- Cap_HS_SF housing stock (dwelling unit) capacity - single-family
- Cap_HS_MF housing stock (dwelling unit) capacity - multi-family
- Ind_Ct number of industrial buildings
- Ind_SqFt total squarefootage of industrial buildings
- Ind_Cost price/rent per squarefoot of industrial buildings
- Ofc_Ct number of office buildings
- Ofc_SqFt total squarefootage of office buildings
- Ofc_Cost price/rent per squarefoot of office buildings
- Ret_Ct number of commercial/retail buildings
- Ret_SqFt total squarefootage of commercial/retail buildings
- Ret_Cost price/rent per squarefoot of commercial/retail buildings
- Unoc_Tot number of unoccupied buildings
- Unoc_Indus number of unoccupied industrial buildings
- Unoc_Offic number of unoccupied office buildings
- Unoc_Retl number of unoccupied retail buildings

### Outputs

These columns will be updated by REDM

- SqFt_SF total squarefootage of single-family units
- SqFt_MF total squarefootage of multiple-family units
- hs Housing units
- hs_sf Single-family housing units
- hs_mf Multiple-family housing units
- dev_sf acres developed as single family residential; detached housing units on lots smaller than one acre
- dev_mf acres developed as multiple family residential
- dev_indus acres developed as industrial, wholesale trade, airport, rail station, communications and utilities, center city parking, park and ride lots, other transportation, or marine terminals
- dev_comm acres developed as retail trade, hotels/motels/resorts, public services, hospitals, or commercial recreation
- dev_office acres developed as offices
- vac_sf undeveloped acres planned for single family residential
- vac_mf undeveloped acres planned for multiple family residential
- vac_indus undeveloped acres planned for industrial, wholesale trade, airport, rail station, communications and utilities, center city parking, park and ride lots, other transportation, or marine terminals
- vac_comm undeveloped acres planned for retail trade, hotels/motels/resorts, public services, hospitals, or commercial recreation
- vac_office undeveloped acres planned for offices
- dev total developed acres
- vac total vacant acres
- Ind_Ct number of industrial buildings
- Ind_SqFt total squarefootage of industrial buildings
- Ofc_Ct number of office buildings
- Ofc_SqFt total squarefootage of office buildings
- Ret_Ct number of commercial/retail buildings
- Ret_SqFt total squarefootage of commercial/retail buildings
- Unoc_Tot number of unoccupied buildings
- Unoc_Indus number of unoccupied industrial buildings
- Unoc_Offic number of unoccupied office buildings
- Unoc_Retl number of unoccupied retail buildings
