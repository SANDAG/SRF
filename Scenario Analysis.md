# Scenario Analysis
Currently, the safest way to prepare a run of the SRF System using alternative assumptions is to first make a copy of the system.  Use Windows Explorer or the `XCOPY` DOS command to copy the entire SRF directory on disk, including all sub-folders and files.   You may wish to rename the copy with a descriptive suffix, e.g. "SRF-SCS".

Similarly, if your scenario involves changes to data stored in the PostgreSQL database accompanying the SRF system, the easiest way to accomplish this at present is to make a complete copy of the database created for the base scenario and then edit/update the copy. For example, you can use the following commands to dump the database to disk:

`set PGUSER=postgres`<br>
`set PGPASSWORD=******`<br>
`pg_dumpall -g > d:/tmp/globals.sql`<br>
`pg_dump -Fd -j 4 -d sandag_db -f d:/tmp/sandagbackup`<br>

Then, use the following commands to restore from the backup:

`set PGUSER=postgres`<br>
`set PGPASSWORD=******`<br>
`psql -f  d:/tmp/globals.sql`<br>
`createdb sandag_db_copy`<br>
`pg_restore -Fd -j 4 -d sandag_db_copy d:/tmp/sandagbackup`<br>

These same operations may also be performed using a graphical user interface, if preferred.  Refer to pgAdmin documentation for further details.

Finally, in the *dbparams.yaml* for the new scenario, set `database: "sandag_db_copy"` to reference the copy of the database restored from the backup.

## Example Scenarios
Users can edit input data to construct alternative forecast series representing different land use scenarios.  Examples include:

* Altering assumptions regarding housing and commercial real estate demand by land use type
* Analyzing hypothetical site-specific real estate development projects using the scheduled development input table

Specific procedures for implementing these changes are discussed below.

### Global real estate assumptions
SRF Supply utilizes projections of housing and non-residential floorspace demand by year and real estate type for the SANDAG region comprising San Diego County to determine how much development, re-development and infill should occur in a given year.  These input assumptions are stored in the *SR13_Regional_Totals_interpolated.csv* file within the Supply folder.  This file contains the following fields:

* **Year:** the series of years within the forecast to be performed;
* **hs_sf:** the number of single-family housing units for each year;
* **hs_mf:** the number of multi-family housing units for each year;
* **ws_ind:** the number of industrial-type workspaces for each year (where a "workspace" is simply the average total space per job in a business establishment);
* **ws_com:** the number of commercial/retail workspaces for each year; and
* **ws_ofc:** the number of office workspaces for each year.

Changing the total number of housing units or workspaces is not reccomended, as it could produce inconsistencies with the socio-economic control totals used by AA and Demand.  However, it is entirely possible to consider hypothetical trends favoring one development type or another (for example, market-wide shifts from single-family to multi-family housing).  An important caveat is that some changes may affect Supply's ability to find sufficient space for all the projected development, and/or convergence behavior of AA and Demand.  Other input parameters for these modules could be adjusted, if necessary, to work around such issues.

### Site-specific real estate development

The "scheduled development" input to the SRF Supply module is designed to allow known, high-probability development to be exogneously incorporated into the land use forecasting process.  However, it can also be used to test the effects of hypothetical future real estate projects that are proposed but not yet confirmed.  Such projects will consume some of the projected real estate demand in the interpolated regional totals noted above, and thus affect the overall spatial distribution of land use by type.

Scheduled development is, by default, stored in the PostgreSQL database associated with the SRF System.  When `use_database` is set to `True` in the *parameters.yaml* file under Supply, the `_supply_scheduled_sites` table is loaded from the SRF schema.  However, the user can override this behavior by setting `use_database: False`, which will cause Supply to look for a file named *Sites_MGRAs.dbf* in the *Data* sub-folder of the *Supply* module directory.  In either case the source table will have the same columns, following a previously defined format that is well-known to SANDAG from prior forecasting work.

The site-specific projects programmed into the user-input scheduled development table will be added to MGRAs and classified according to the seven land use types defined for the SRF System, including the two types not otherwise allocated by Supply (i.e. mobile homes and "other" non-residential real estate).  Thus the scheduled development input table also provides a mechanism for exogneously forecasting land use change that is not predicted using the SRF System's economic models.
