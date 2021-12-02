REM This batch file can be used to restore an SRF System database from backup (i.e. during installation)
ECHO OFF
SET /p PGUSER="Please enter PostgreSQL username: "
set /p PGPASSWORD="Please enter PostgreSQL password: "
SET /p globals = "Please specify path to globals.sql file: "
ECHO Restoring PostgreSQL globals...
psql -f %globals%
SET /p new_db = "Please specify new database name"
SET /p backup_dir = "Please specify path to source database backup directory: "
ECHO Creating new database and restoring from backup...
createdb %new_db%
pg_restore -Fd -j 4 -d %new_db% %backup_dir%
