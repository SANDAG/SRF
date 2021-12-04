REM This script is written to streamline installation of required software libraries for the SRF System
ECHO "Warning!  You must have already installed Anaconda Python and R before running this script!"
proceed = "N"
SET /p proceed="Have you done so? (y/N):"
IF proceed EQU "N" CANCEL
conda install psycopg2
pip install pipenv
cd Supply
pipenv install
cd ..
rscript Demand\install_requirements.R
ECHO "Installation of required libraries complete."
SET PATH=%PATH%;%ProgramFiles%\PostgreSQL
ECHO "PostgreSQL added to path variable"
SET /p mupath="Please specify location of mu-land.exe:"
SET PATH=%PATH%;%mupath%
