REM This batch file can be used to create a copy of an SRF System database as a starting point for a new SRF scenario
ECHO OFF
set /p PGUSER="PostgreSQL username: "
set /p PGPASSWORD="PostgreSQL password: "
set /p source_db="Source database name: "
set /p target_db="Target database name: "
ECHO ON
ECHO Performing copy operation...
pg_dump -Fd -j 4 -d %source_db% -f %TMP%/%source_db%
createdb %target_db%
pg_restore -Fd -j 4 -d %target_db% %TEMP%/%source_db%
