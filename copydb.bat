REM This batch file can be used to create a copy of an SRF System database as a starting point for a new SRF scenario
REM Arguments:
REM 1. PostgreSQL username
REM 2. PostgreSQL password
REM 3. Source database name
REM 4. Target database name
REM 5. Temporary working folder
set PGUSER=%1
set PGPASSWORD=%2
pg_dump -Fd -j 4 -d %3 -f %5/%3
createdb %4
pg_restore -Fd -j 4 -d $4 %5/%3
