# SRF System
The SRF (Sub-Regional Forecasting) System is a tool for allocating land use and socio-economic activity within the Greater San Diego region, co-extensive with San Diego County.  A consulting team led by Manhan Group, LLC developed the system under contract to the San Diego Association of Governments.

The SRF System includes three major sub-models:

* SRF Supply micro-simulates real estate development events across the region;
* Activity Allocation (PECAS AA) allocates households and jobs to coarse zones called LUZs; and
* SRF Demand uses bid-rent analysis to allocate households and jobs by LUZ to MGRAs.

The components of the system are connected via transfer of shared data; for example, the AA model uses floorspace estimates updated by the SRF Supply model, which uses rent values updated by the SRF Demand model.

In addition, these three components interface with several exogneous, SANDAG-maintained models:

* The GPALL and CAPACITY processes provide constraints on development by type and location;
* A regional demographic model forecasts households and housing units by type;
* A regional economic model (REMI PI+) forecasts employment by sector;
* A population synthesizer (PopSyn3) simulates a complete enumeration of County residents; and
* SANDAG's ABM2 (CT-RAMP) simulates the travel behavior of this synthetic population

# System Requirements
The SRF System has been developed and tested by the consulting team on an Amazon Web Services (AWS) Elastic Cloud Compute (EC2) c5d.4xlarge instance with the following attributes:

* **OS**: Microsoft Windows Server 2019 Datacenter 
* **Processor**: Intel(R) Xeon(R) Platinum 8124M CPU @ 3.00GHz, 3000 Mhz, 8 Core(s), 16 Logical Processor(s)
* **Installed Physical Memory (RAM)**:	32.0 GB
* **Hard Disk Capacity**: 1 TB

For best results it is reccomended to run the SRF system on a computer matching or exceeding these specifications.

# Installation

Many of the inputs to the SRF System (e.g. base year input data) are currently stored in a PostgreSQL database with secure password-protected access to ensure data integrity.  Please contact Manhan Group, LLC (info@manhangroup.com) if you wish to replicate the contents of this database on another server.

Most recent version of PostgreSQL is recommended. If you are using PostgreSQL 10 and above, make sure to edit postgresql.conf and change the password encription parameter to
password_encryption = md5
The default password encryption method is "scram-sha-256" which is not supported by RPostgresql module used in the SRF demand model and hence need to revert back to "md5". 
Change the password authentication method to "md5" for user: "usrPostgres"  in pg_hba.conf  as well.  
In addition, if the user "usrPostgres" was created before the above change, make sure to reset the password for this user. Its password will now be hashed with md5.

Since PECAS AA model java code was compiled with Java 10. Make sure your Java version is 10 or higher. 

Check machine_settings.py to make sure correct paths are set for pgpath, javaRunCommand, pythonCommand.
Each of the core sub-modules are coded in different languages and use different libraries.  A separate Readme file under the sub-folder for each module describes these pre-requisites.  Before attempting to run the system, please visit each of these sub-folders and follow the instructions to ensure all required libraries are installed.

# Operation

After populating the input data and installing required code libraries, you can begin a test run of the baseline forecast scenario by opening the Anaconda command-line prompt, navigating to the top-level SRF System directly, and executing the following command:

`StartSRF.BAT`

Note that the system will not run properly if this command is executed from an ordinary Windows command-line prompt; the Anaconda prompt must be used in order to ensure availability of required libraries in the Python environment.