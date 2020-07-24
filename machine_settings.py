# Machine-specific settings for PECAS.
# On each machine, create a copy of this template called machine_settings.py, then adjust the settings as needed for that machine.
# The machine_settings.py file is included in svnignore, so it will not be committed to the repository. This is by design. DO NOT change it!

postgres = "postgres"

# Using postgreSQL or SQL Server for SD?
sql_system = postgres
 
# installation configuration

javaRunCommand = "C:/Program Files/Java/jre-10.0.2/bin/java.exe"
pythonCommand = "python"

aa_maxthreads = 32

# Java memory settings
aa_memory = "30000M"
# Memory used by the population synthesizer
pop_syn_memory = "20000M"

db_param_files = "dbparams.yaml"


   






