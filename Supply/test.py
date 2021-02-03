import main as m
parameters=m.parameters

if parameters is not None:
    # load dataframe(s)
    use_database = parameters['use_database']
    parameters['input_filename']=None
    mgra_dataframe = m.open_mgra_io_file(from_database=use_database, filename=parameters['input_filename'])
    planned_sites = m.open_sites_file(from_database=True)

        # start simulation
    m.run(mgra_dataframe, planned_sites)
