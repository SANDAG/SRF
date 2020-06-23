/*******************************************************************************
 *            Micro Land (mu-land) - Land Use Model 
 *                     Copyright 2016 by
 *
 *          Felipe Saavedra C. (fsaavedr@dcc.uchile.cl)
 *
 *
 *  This file is part of Micro Land (mu-land)
 *
 *  Mu-Land is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  Mu-Land is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with Mu-Land.  If not, see <http://www.gnu.org/licenses/>.
 *
 ******************************************************************************/

#include <exception>

#include <iostream>
#include <fstream>

#include <io/txt_datafile_reader.hpp>
#include <data/muland_data.hpp>
#include <math/muland_tools.hpp>
#include <solver/configurator.hpp>

using namespace muland;

/* static member */
configurator* configurator::mps_instance = NULL; /**< Unique instance of configurator */

configurator*
configurator::GetInstance ( std::string sim_path )
{
    if ( configurator::mps_instance == 0 )
        configurator::mps_instance = new configurator ( sim_path );
    return configurator::mps_instance;
}

configurator*
configurator::GetInstance()
{
    /// This should be called only when already created with simfile
    if ( configurator::mps_instance == 0 )
        exit ( 1 );
    return configurator::mps_instance;

}
/******************************************************************************/
int
ParseInput ( io::DatafileReader* reader, io::Datafile::datafile_ptr datafile )
{
    try
    {
        reader = new txtDatafileReader(datafile); 
        reader->Parse();
        reader->Close();
        return 0;
    }
    catch ( std::exception& e )
    {
        std::cerr << "File: "+ datafile->getFileName() +" missing";
        return 1;
    }
}
/******************************************************************************/
configurator::configurator
( std::string sim_path )
{

    io::DatafileReader* reader = 0; // reader instance
    /// @todo must initialize files according to simulation id definition
    const std::string _input  ( sim_path+"/input" );
    const std::string _output ( sim_path+"/output" );
    
    mp_agents = io::Datafile::datafile_ptr ( new io::Datafile ( _input+"/agents.csv", io::Datafile::AGENTS ) );
    mp_zones  = io::Datafile::datafile_ptr ( new io::Datafile ( _input+"/zones.csv" , io::Datafile::ZONES  ) );
    mp_access_attraction = io::Datafile::datafile_ptr( new io::Datafile( _input+"/agents_zones.csv"       , io::Datafile::ACCESS_ATTRACTION ) );
    mp_real_estates      = io::Datafile::datafile_ptr( new io::Datafile( _input+"/real_estates_zones.csv" , io::Datafile::REAL_ESTATES ) );
    mp_demand            = io::Datafile::datafile_ptr( new io::Datafile( _input+"/demand.csv"             , io::Datafile::DEMAND ) );
    mp_demand_exogenous_cutoff = io::Datafile::datafile_ptr( new io::Datafile( _input+"/demand_exogenous_cutoff.csv", io::Datafile::DEMAND_EXOGENOUS_CUTOFF ) );
    mp_bid_function  = io::Datafile::datafile_ptr( new io::Datafile( _input+"/bids_functions.csv", io::Datafile::BID_FUNCTION ) );
    mp_rent_function = io::Datafile::datafile_ptr( new io::Datafile( _input+"/rent_functions.csv", io::Datafile::RENT_FUNCTION ) );
    mp_bid_adjustment  = io::Datafile::datafile_ptr( new io::Datafile( _input+"/bids_adjustments.csv", io::Datafile::BID_ADJUSTMENT ) );
    mp_rent_adjustment = io::Datafile::datafile_ptr( new io::Datafile(_input+"/rent_adjustments.csv", io::Datafile::RENT_ADJUSTMENT ) );
    mp_subsidies = io::Datafile::datafile_ptr( new io::Datafile( _input+"/subsidies.csv", io::Datafile::SUBSIDES ) );
    mp_supply    = io::Datafile::datafile_ptr( new io::Datafile( _input+"/supply.csv"   , io::Datafile::FIXED_SUPPLY ) );
    
    // try to create output directory if not exists
    io::Datafile* _directories = new io::Datafile ( _output, io::Datafile::OTHER, io::Datafile::PATH, io::Datafile::OUTPUT );
    _directories->create_directory();

    /// definition of input files sources
    // Should always exists
    ParseInput ( reader, mp_agents );
    ParseInput ( reader, mp_zones );
    ParseInput ( reader, mp_access_attraction );
    ParseInput ( reader, mp_real_estates );

    ParseInput ( reader, mp_demand );
    ParseInput ( reader, mp_demand_exogenous_cutoff );
    // functions definition should be always required
    ParseInput ( reader, mp_bid_function );
    ParseInput ( reader, mp_rent_function );

    ParseInput ( reader, mp_bid_adjustment );
    ParseInput ( reader, mp_rent_adjustment );

    ParseInput ( reader, mp_subsidies );
    ParseInput ( reader, mp_supply );



    /// @todo Review output files design
    mp_b_hvi     = io::Datafile::datafile_ptr (
                      new io::Datafile (
                          _output+"/bids.csv",
                          io::Datafile::BIDS,
                          io::Datafile::TXT,
                          io::Datafile::OUTPUT
                      )
                  );
    mp_b_h       = io::Datafile::datafile_ptr
                  (
                      new io::Datafile
                      (
                          _output+"/bh.csv",
                          io::Datafile::BH_BID_COMPONENT,
                          io::Datafile::TXT,
                          io::Datafile::OUTPUT

                      )

                  );
    mp_H_hvi = io::Datafile::datafile_ptr
                  (
                      new io::Datafile
                      (
                          _output+"/location.csv",
                          io::Datafile::LOCATION,
                          io::Datafile::TXT,
                          io::Datafile::OUTPUT

                      )

                  );
    mp_Prob_hvi = io::Datafile::datafile_ptr
                              (
                                  new io::Datafile
                                  (
                                      _output+"/location_probability.csv",
                                      io::Datafile::LOCATION_PROBABILITY,
                                      io::Datafile::DBF,
                                      io::Datafile::OUTPUT

                                  )

                              );
    mp_r_vi    = io::Datafile::datafile_ptr
                  (
                      new io::Datafile
                      (
                          _output+"/rents.csv",
                          io::Datafile::RENTS,
                          io::Datafile::TXT,
                          io::Datafile::OUTPUT

                      )

                  );
    mp_S_vi   = io::Datafile::datafile_ptr
                  (
                      new io::Datafile
                      (
                          _output+"/supply.csv",
                          io::Datafile::SUPPLY,
                          io::Datafile::TXT,
                          io::Datafile::OUTPUT

                      )
                  );

}

int configurator::save( )
{
    
    LandData* data = LandData::GetInstance();
    unsigned n_h = mp_agents->GetData()->size1();
    // save bh vector
    std::ofstream file;
    file.open ( mp_b_h->getPath().c_str() );
    file << "Agents;Value\n";
    for (unsigned i = 0; i < data->b_h.size(); i++)
        file << idx::reverseFindH( i%n_h) << ";" << data->b_h(i) << "\n";
    file.close();
    // save bids
    file.open ( mp_b_hvi->getPath().c_str() );
    file << "Realestate;Zone";
    for (unsigned h = 0; h < n_h; h++) file << ";H_Type[" << h+1 << "]";
    file << "\n";
    
    for (unsigned i = 0; i < data->b_hvi.size2(); i++)
    {
        file << idx::reverseFindVi(i).first << ";" << idx::reverseFindVi(i).second; 
        for (unsigned h = 0; h < n_h; h++) file << ";" << data->b_hvi(h, i);
        file << "\n";
    }
    file.close();
    
    // save location
    file.open ( mp_H_hvi->getPath().c_str() );
    file << "Realestate;Zone";
    for (unsigned h = 0; h < n_h; h++) file << ";H_Type[" << h+1 << "]";
    file << "\n";
    
    for (unsigned i = 0; i < data->H_hvi.size2(); i++)
    {
        file << idx::reverseFindVi(i).first << ";" << idx::reverseFindVi(i).second; 
        for (unsigned h = 0; h < n_h; h++) file << ";" << data->H_hvi(h, i);
        file << "\n";
    }
    file.close();

    // save location_probability
    file.open ( mp_Prob_hvi->getPath().c_str() );
    file << "Realestate;Zone";
    for (unsigned h = 0; h < n_h; h++) file << ";H_Type[" << h+1 << "]";
    file << "\n";
    
    for (unsigned i = 0; i < data->P_hvi.size2(); i++)
    {
        file << idx::reverseFindVi(i).first << ";" << idx::reverseFindVi(i).second; 
        for (unsigned h = 0; h < n_h; h++) file << ";" << data->P_hvi(h, i);
        file << "\n";
    }
    file.close();
    
    // save rents vector
    file.open ( mp_r_vi->getPath().c_str() );
    file << "Realestate;Zone;Value\n";
    for (unsigned i = 0; i < data->r_vi.size(); i++)
        file << idx::reverseFindVi(i).first << ";" << idx::reverseFindVi(i).second  << ";" << data->r_vi(i) << "\n";
    file.close();
    
    return 0;
}


// kate: indent-mode cstyle; indent-width 4; replace-tabs on; 
