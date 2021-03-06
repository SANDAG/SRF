# Supply Module

Real Estate Development Model targeting SANDAG's MGRA level datasets

## Recommended System Requirements

- OS:
  - Windows 10 64 bit, MacOS 10.15.4 or greater, or a GNU/Linux that can run python 3.6 or higher, `ldd`, `objdump` and `objcopy`
- Hard Disk Space:
  - 4 times total model file size times the number of simulation years (SSD preferred)
    - For example: 4 x 300MB model x 35 simulation years = 42GB minimum
- RAM:
  - 8 GB, or 4x total model file size, whichever is greater
- Processor:
  - Intel i5-2400 or equivalent, or better

### System requirements notes

- We will use `pyinstaller` to create distributable software, the dist files will work with any specific OS, as long as `pyinstaller` is run on a matching OS. The operating systems listed are those available for us to build on.
- We use a `pipenv` virtual environment, [here are instructions for installing `pipenv`](https://medium.com/@mahmudahsan/how-to-use-python-pipenv-in-mac-and-windows-1c6dc87b403e)

## Installation

- Install dependencies with: `pipenv install`
  - You will need to install [c++ build tools for visual studio](https://visualstudio.microsoft.com/downloads/) if you haven't already
- Test with: `pipenv run python run_tests.py -t` or `pipenv run ./test_with_coverage.sh`
  - Note that this step is not required, and tests expect local files by default
- Create distributable folder with: `pipenv run pyinstaller main.py`

## Usage

### Data Folder

Up to date data files will be downloaded from the SANDAG database, alternatively you can provide the same files:

- Add MGRA level data to the `data` folder
  - Ensure that the column labels match those found in `labels.yaml`
- If the mgra version 4.1 is not found, the program will look for `interpolated_vars.csv` and `SRF_Input_Base_V4.csv` to create one
- If adding scheduled development, ensure that there is a compatible sites file; `Sites_MGRAs.dbf`
- If exporting to AA, ensure that there is a compatible crosswalk file; `CRE2FSC.csv`

### Parameter Configuration

Change program inputs parameters in `parameters.yaml`

### Execution

Run with `pipenv run python main.py`

- Alternatively, run the main executable from the pyinstaller dist folder after following installation steps
- Omit `pipenv run` from commands by first running `pipenv shell`

## Module Process

- Note that the supply module considers vacancy rates as an important factor, for development, but that there is also _vacant land_ which is just greenfield, and doesn't factor into the vacancy rate.

## Interface

The Supply module attempts a database download, or accepts a .csv file. In either case, it expects the following data on each MGRA:

### Input and Output Columns

The Supply module expects these columns and updates them during program execution

- SqFt_SF | total squarefootage of single-family units
- SqFt_MF | total squarefootage of multiple-family units
- hs | Housing units
- hs_sf | Single-family housing units
- hs_mf | Multiple-family housing units
- job_spaces | total job spaces
- office_js | office total job spaces
- comm_js | commercial total job spaces
- indus_js | industrial total job spaces
- dev_sf | acres developed as single family residential; detached housing units on lots smaller than one acre
- dev_mf | acres developed as multiple family residential
- dev_indus | acres developed as industrial, wholesale trade, airport, rail station, communications and utilities, center city parking, park and ride lots, other transportation, or marine terminals
- dev_comm | acres developed as retail trade, hotels/motels/resorts, public services, hospitals, or commercial recreation
- dev_office | acres developed as offices
- vac_sf | undeveloped acres planned for single family residential
- vac_mf | undeveloped acres planned for multiple family residential
- vac_indus | undeveloped acres planned for industrial, wholesale trade, airport, rail station, communications and utilities, center city parking, park and ride lots, other transportation, or marine terminals
- vac_comm | undeveloped acres planned for retail trade, hotels/motels/resorts, public services, hospitals, or commercial recreation
- vac_office | undeveloped acres planned for offices
- dev | total developed acres
- vac | total vacant acres
- Ind_Ct | number of industrial buildings
- Ind_SqFt | total squarefootage of industrial buildings
- Ofc_Ct | number of office buildings
- Ofc_SqFt | total squarefootage of office buildings
- Ret_Ct | number of commercial/retail buildings
- Ret_SqFt | total squarefootage of commercial/retail buildings
- redev_sf_m | acres developed as single family residential, planned for redevelopment as multiple family residential
- redev_sf_e | acres developed as single family residential, planned for redevelopment as employment use
- redev_mf_e | acres developed as multiple family residential, planned for redevelopment as employment use
- redev_mh_s | acres developed as mobile home parks, planned for redevelopment as single family residential
- redev_mh_m | acres developed as mobile home parks, planned for redevelopment as multiple family residential
- redev_mh_e | acres developed as mobile home parks, planned for redevelopment as employment use
- redev_ag_l | acres developed as agricultural, extractive industry, or junkyard/dumps/landfills planned for redevelopment as spaced rural residential
- redev_ag_s | acres developed as agricultural, extractive industry, or junkyard/dumps/landfills planned for redevelopment as single family residential
- redev_ag_m | acres developed as agricultural, extractive industry, or junkyard/dumps/landfills planned for redevelopment as multiple family residential
- redev_ag_i | acres developed as agricultural, extractive industry, or junkyard/dumps/landfills planned for redevelopment as industrial, wholesale trade, airport, rail station, communications and utilities, center city parking, park and ride lots, other transportation,
- redev_ag_c | acres developed as agricultural, extractive industry, or junkyard/dumps/landfills planned for redevelopment as retail trade, hotels/motels/resorts, public services, hospitals, or commercial recreation
- redev_ag_o | acres developed as agricultural, extractive industry, or junkyard/dumps/landfills planned for redevelopment as offices
- redev_ag_r | acres developed as agricultural, extractive industry, or junkyard/dumps/landfills planned for redevelopment as residential
- redev_emp\_ | acres developed as employment use, planned for redevelopment as a different category of employment use
- infill_sf | developed acres planned for single family residential infill
- infill_mf | developed acres planned for multiple family residential infill
- infill_emp | developed acres planned for employment infill

### Additional Inputs

The following inputs are also required, but are not changed during execution:

- MGRA | Series 13 MGRA (Master Geographic Reference Area)
- Shape_Area | area of MGRA object (square footage)
- Land_Cost | cost of land per acre
- Price_SF | price/rent cost per square foot for single family dwelling
- Price_MF | price/rent cost per square foot for multi family dwelling
- hh | Households (occupied housing units)
- hh_sf | Single-family households (occupied housing units)
- hh_mf | Multiple-family households (occupied housing units)
- emp_indus\_ | Employment in industrial land uses
- emp_comm_l | Employment in commercial land uses
- emp_office | Employment in office land uses
- emp_other\_ | Employment in other land uses
- acres | total acres
- unusable | vacant land not available for development for physical, public policy, or environmental reasons
- DUA | dwelling units per acre
- Cap_HS | housing stock (dwelling unit) capacity
- Cap_HS_SF | housing stock (dwelling unit) capacity - single-family
- Cap_HS_MF | housing stock (dwelling unit) capacity - multi-family
- Ind_Cost | price/rent per squarefoot of industrial buildings
- Ofc_Cost | price/rent per squarefoot of office buildings
- Ret_Cost | price/rent per squarefoot of commercial/retail buildings
