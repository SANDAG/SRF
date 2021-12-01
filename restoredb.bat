REM This batch file can be used to restore an SRF System database from backup (i.e. during installation)
REM Arguments:
REM 1. PostgreSQL username
REM 2. PostgreSQL password
REM 3. globals.sql path
REM 4. new db name
REM 5. database backup dir path
set PGUSER=%1
set PGPASSWORD=%2
psql -f %3
createdb %4
pg_restore -Fd -j 4 -d $4 %5
