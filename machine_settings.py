# Machine-specific settings for PECAS.
# On each machine, create a copy of this template called machine_settings.py, then adjust the settings as needed for that machine.
# The machine_settings.py file is included in svnignore, so it will not be committed to the repository. This is by design. DO NOT change it!

postgres = "postgres"

# Using postgreSQL or SQL Server for SD?
sql_system = postgres
 
# installation configuration

# installation configuration
pgpath = "C:/Program Files/PostgreSQL/13/bin/"
javaRunCommand = "java"
pythonCommand = "C:/ProgramData/Anaconda3/python.exe"
winShCommand = "C:/Program Files/Git/bin/sh.exe"

aa_maxthreads = 32

# Java memory settings
aa_memory = "30000M"
# Memory used by the population synthesizer
pop_syn_memory = "20000M"

db_param_files = "dbparams.yaml"


   






